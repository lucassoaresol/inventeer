#!/usr/bin/env python3
"""Integration tests for the opt-in staged-content guard and hook installer."""

from __future__ import annotations

import os
import pathlib
import shutil
import subprocess
import tempfile


ROOT = pathlib.Path(__file__).resolve().parents[1]
GUARD = ROOT / "scripts/check-staged-content.py"
INSTALLER = ROOT / "scripts/install-git-hooks.sh"
HOOK = ROOT / ".githooks/pre-commit"


def run(*argv: str | bytes, cwd: pathlib.Path) -> subprocess.CompletedProcess:
    return subprocess.run(argv, cwd=cwd, capture_output=True, check=False)


def git(repo: pathlib.Path, *args: str | bytes) -> subprocess.CompletedProcess:
    return run("git", *args, cwd=repo)


def initialize(repo: pathlib.Path) -> None:
    assert git(repo, "init", "--quiet").returncode == 0
    assert git(repo, "config", "user.email", "fixture@example.invalid").returncode == 0
    assert git(repo, "config", "user.name", "Fixture").returncode == 0
    (repo / "baseline.txt").write_text("baseline\n", encoding="utf-8")
    assert git(repo, "add", "baseline.txt").returncode == 0
    assert git(repo, "commit", "--quiet", "-m", "baseline").returncode == 0


def fingerprint(repo: pathlib.Path) -> tuple[bytes, bytes]:
    tree = git(repo, "write-tree")
    status = git(repo, "status", "--porcelain=v1", "-z")
    assert tree.returncode == status.returncode == 0
    return tree.stdout, status.stdout


def guard(repo: pathlib.Path) -> subprocess.CompletedProcess:
    return run("python3", str(GUARD), "--repo", str(repo), cwd=ROOT)


with tempfile.TemporaryDirectory() as temporary:
    repo = pathlib.Path(temporary)
    initialize(repo)
    safe = repo / "safe.txt"
    safe.write_text("ordinary staged text\n", encoding="utf-8")
    assert git(repo, "add", safe.name).returncode == 0
    before = fingerprint(repo)
    result = guard(repo)
    assert result.returncode == 0, result.stderr.decode()
    assert result.stdout == b"staged-content: PASS (1 file)\n"
    assert fingerprint(repo) == before
print("ok 1 - safe staged text passes without index or worktree mutation")

forbidden_cases = (
    (".env", b"placeholder=true\n", "forbidden-path"),
    ("private.pem", b"placeholder\n", "forbidden-path"),
    ("backup.dump", b"placeholder\n", "forbidden-path"),
    ("ordinary.txt", b"-----BEGIN " + b"PRIVATE KEY-----\n", "private-key"),
    ("ordinary.txt", b"token=" + b"github_" + b"pat_" + b"A" * 40 + b"\n", "credential-token"),
    ("ordinary.bin", b"text\x00binary", "binary"),
    ("ordinary.txt", b"x" * (5 * 1024 * 1024 + 1), "oversized"),
)

with tempfile.TemporaryDirectory() as temporary:
    repo = pathlib.Path(temporary)
    initialize(repo)
    for name, content, reason in forbidden_cases:
        path = repo / name
        path.write_bytes(content)
        assert git(repo, "add", name).returncode == 0
        before = fingerprint(repo)
        result = guard(repo)
        assert result.returncode == 1, (name, result.stdout, result.stderr)
        diagnostic = result.stderr.decode("utf-8")
        assert diagnostic == f"staged-content: {name} [{reason}]\n"
        assert content[:32] not in result.stderr
        assert fingerprint(repo) == before
        assert git(repo, "reset", "--quiet", "HEAD", "--", name).returncode == 0
        path.unlink()
print(f"ok 2 - {len(forbidden_cases)} forbidden staged signals fail with path-only diagnostics")

with tempfile.TemporaryDirectory() as temporary:
    repo = pathlib.Path(temporary)
    initialize(repo)
    invalid_name = os.fsencode(repo) + b"/invalid-\xff.txt"
    descriptor = os.open(invalid_name, os.O_WRONLY | os.O_CREAT, 0o600)
    os.write(descriptor, b"unsafe filename\n")
    os.close(descriptor)
    assert git(repo, "add", b"invalid-\xff.txt").returncode == 0
    before = fingerprint(repo)
    result = guard(repo)
    assert result.returncode == 1
    assert result.stderr == b"staged-content: staged path is unsafe [unsafe-path]\n"
    assert b"unsafe filename" not in result.stderr
    assert fingerprint(repo) == before
print("ok 3 - unsafe staged filenames fail closed without content or lossy paths")

with tempfile.TemporaryDirectory() as temporary:
    repo = pathlib.Path(temporary)
    initialize(repo)
    unsafe = repo / "line\nbreak.txt"
    unsafe.write_text("unsafe control path\n", encoding="utf-8")
    assert git(repo, "add", unsafe.name).returncode == 0
    before = fingerprint(repo)
    result = guard(repo)
    assert result.returncode == 1
    assert result.stderr == b"staged-content: staged path is unsafe [unsafe-path]\n"
    assert b"line" not in result.stderr and b"break" not in result.stderr
    assert fingerprint(repo) == before
print("ok 4 - control characters in staged paths fail without terminal injection")

with tempfile.TemporaryDirectory() as temporary:
    not_repo = pathlib.Path(temporary)
    result = guard(not_repo)
    assert result.returncode == 1
    assert result.stderr == b"staged-content: could not inspect Git index [git-error]\n"
print("ok 5 - Git inspection failures fail closed")

with tempfile.TemporaryDirectory() as temporary:
    repo = pathlib.Path(temporary)
    initialize(repo)
    (repo / "scripts").mkdir()
    (repo / ".githooks").mkdir()
    shutil.copy2(INSTALLER, repo / "scripts/install-git-hooks.sh")
    shutil.copy2(HOOK, repo / ".githooks/pre-commit")
    before = git(repo, "config", "--local", "--list").stdout.splitlines()
    first = run("bash", "scripts/install-git-hooks.sh", cwd=repo)
    second = run("bash", "scripts/install-git-hooks.sh", cwd=repo)
    assert first.returncode == second.returncode == 0
    after = git(repo, "config", "--local", "--list").stdout.splitlines()
    assert sorted(set(after) - set(before)) == [b"core.hookspath=.githooks"]
    assert after.count(b"core.hookspath=.githooks") == 1
print("ok 6 - explicit hook installation changes only core.hooksPath and is idempotent")

with tempfile.TemporaryDirectory() as temporary:
    fixture = pathlib.Path(temporary)
    (fixture / "scripts").mkdir()
    shutil.copy2(INSTALLER, fixture / "scripts/install-git-hooks.sh")
    result = run("bash", "scripts/install-git-hooks.sh", cwd=fixture)
    assert result.returncode != 0
print("ok 7 - hook installation outside a Git worktree fails without configuration")

hook_text = HOOK.read_text(encoding="utf-8")
assert "scripts/check-staged-content.py" in hook_text
assert "diff --cached --check" in hook_text
assert "test-staged-content-guard.py" in (ROOT / "scripts/test-workspace.sh").read_text(encoding="utf-8")
print("ok 8 - the versioned hook and aggregate gate invoke the staged checks")
