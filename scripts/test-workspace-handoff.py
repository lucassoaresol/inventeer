#!/usr/bin/env python3
"""Behavioral contract for the workspace freshness-aware Handoff."""

from __future__ import annotations

import json
import pathlib
import subprocess
import tempfile


ROOT = pathlib.Path(__file__).resolve().parents[1]
SUBJECT = ROOT / "scripts/workspace-handoff.py"
RECORDED_AT = "2026-08-18T20:00:00Z"


def command(*args: str, cwd: pathlib.Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*args], cwd=cwd, capture_output=True, text=True, check=check
    )


def git(repo: pathlib.Path, *args: str) -> str:
    return command("git", *args, cwd=repo).stdout.strip()


def initialize(repo: pathlib.Path, *, remote: pathlib.Path | None = None) -> None:
    repo.mkdir(parents=True)
    git(repo, "init", "-b", "main")
    git(repo, "config", "user.name", "Workspace Test")
    git(repo, "config", "user.email", "workspace-test@example.invalid")
    state = repo / ".specs/STATE.md"
    state.parent.mkdir(parents=True)
    state.write_text(
        "# State\n\n## Decisions\n\n### AD-001\n- Decision: preserve me\n\n"
        "## Handoff\n\n- **Legacy**: stale\n",
        encoding="utf-8",
    )
    git(repo, "add", ".specs/STATE.md")
    git(repo, "commit", "-m", "docs: initialize state")
    if remote is not None:
        command("git", "init", "--bare", str(remote), cwd=repo)
        git(repo, "remote", "add", "origin", str(remote))
        git(repo, "push", "-u", "origin", "main")


def write_args(repo: pathlib.Path, valid_sha: str, publication: str) -> list[str]:
    return [
        str(SUBJECT),
        "--root",
        str(repo),
        "write",
        "--feature",
        "Retrospective Evidence Freshness",
        "--phase-task",
        "Validation complete",
        "--completed",
        "auditor v3",
        "--in-progress",
        "none",
        "--next-step",
        "Start the Value Increment workflow improvement",
        "--blocker",
        "none",
        "--branch",
        "main",
        "--contract-status",
        "PASS",
        "--operational-status",
        "UNPROVEN",
        "--recorded-at",
        RECORDED_AT,
        "--valid-at-sha",
        valid_sha,
        "--publication-state",
        publication,
        "--evidence-path",
        ".specs/STATE.md",
        "--evidence-path",
        ".specs/features/INDEX.md",
        "--evidence-path",
        ".specs/features/example/spec.md",
        "--evidence-path",
        ".specs/features/example/validation.md",
    ]


def status(repo: pathlib.Path) -> subprocess.CompletedProcess[str]:
    return command(str(SUBJECT), "--root", str(repo), "status", cwd=repo, check=False)


with tempfile.TemporaryDirectory(prefix="workspace-handoff-") as directory:
    fixture = pathlib.Path(directory)
    repo = fixture / "repo"
    remote = fixture / "origin.git"
    initialize(repo, remote=remote)

    behavior = repo / "scripts/behavior.py"
    behavior.parent.mkdir()
    behavior.write_text("VALUE = 1\n", encoding="utf-8")
    git(repo, "add", "scripts/behavior.py")
    git(repo, "commit", "-m", "feat: add behavior")
    behavioral_sha = git(repo, "rev-parse", "HEAD")

    state = repo / ".specs/STATE.md"
    original = state.read_bytes()
    updated = command(*write_args(repo, behavioral_sha, "unpublished"), cwd=repo)
    assert updated.stdout.strip() == "updated"
    rendered = state.read_text(encoding="utf-8")
    assert rendered.split("## Handoff", 1)[0] == original.decode("utf-8").split("## Handoff", 1)[0]
    for expected in (
        f"- **Recorded at**: {RECORDED_AT}",
        f"- **Valid at SHA**: {behavioral_sha}",
        "- **Publication state**: unpublished",
        "- **Invalidated by**: behavioral SHA ancestry break; non-evidence descendant; publication state change",
        "- **Contract status**: PASS",
        "- **Operational status**: UNPROVEN",
    ):
        assert expected in rendered

    fresh_dirty = status(repo)
    assert fresh_dirty.returncode == 0
    assert json.loads(fresh_dirty.stdout) == {"schema": 1, "state": "fresh", "reason": "match"}
    print("ok 1 - write replaces only Handoff and records the complete freshness schema")

    before_rejection = state.read_bytes()
    transient_args = write_args(repo, behavioral_sha, "unpublished")
    transient_args[transient_args.index("--next-step") + 1] = "push the branch"
    rejected = command(*transient_args, cwd=repo, check=False)
    assert rejected.returncode == 2
    assert "transient external action" in rejected.stderr
    assert state.read_bytes() == before_rejection
    print("ok 2 - transient external actions fail before bytes change")

    git(repo, "add", ".specs/STATE.md")
    git(repo, "commit", "-m", "docs: record handoff")
    fresh_descendant = status(repo)
    assert fresh_descendant.returncode == 0
    assert json.loads(fresh_descendant.stdout)["state"] == "fresh"
    print("ok 3 - evidence-only descendant commits preserve behavioral freshness")

    git(repo, "push", "origin", "main")
    publication_changed = status(repo)
    assert publication_changed.returncode == 1
    assert json.loads(publication_changed.stdout) == {
        "schema": 1,
        "state": "stale",
        "reason": "publication-changed",
    }
    print("ok 4 - upstream publication drift invalidates the Handoff")

    command(*write_args(repo, behavioral_sha, "published"), cwd=repo)
    git(repo, "add", ".specs/STATE.md")
    git(repo, "commit", "-m", "docs: refresh publication state")
    assert status(repo).returncode == 0

    behavior.write_text("VALUE = 2\n", encoding="utf-8")
    git(repo, "add", "scripts/behavior.py")
    git(repo, "commit", "-m", "feat: change behavior")
    sha_changed = status(repo)
    assert sha_changed.returncode == 1
    assert json.loads(sha_changed.stdout)["reason"] == "sha-changed"
    print("ok 5 - behavioral descendants invalidate the Handoff")

    local = fixture / "local-only"
    initialize(local)
    local_sha = git(local, "rev-parse", "HEAD")
    command(*write_args(local, local_sha, "indeterminate"), cwd=local)
    indeterminate = status(local)
    assert indeterminate.returncode == 2
    assert json.loads(indeterminate.stdout) == {
        "schema": 1,
        "state": "indeterminate",
        "reason": "upstream-unavailable",
    }
    print("ok 6 - absent upstream returns indeterminate instead of fresh")

    missing = fixture / "missing-state"
    missing.mkdir()
    git(missing, "init", "-b", "main")
    git(missing, "config", "user.name", "Workspace Test")
    git(missing, "config", "user.email", "workspace-test@example.invalid")
    missing_status = status(missing)
    assert missing_status.returncode == 2
    assert json.loads(missing_status.stdout)["reason"] == "handoff-invalid"
    print("ok 7 - missing state fails closed")

    linked = fixture / "linked-state"
    initialize(linked)
    linked_state = linked / ".specs/STATE.md"
    real_state = linked / "real-state.md"
    linked_state.replace(real_state)
    linked_state.symlink_to(real_state)
    linked_status = status(linked)
    assert linked_status.returncode == 2
    assert json.loads(linked_status.stdout)["reason"] == "handoff-invalid"
    print("ok 8 - symlinked state fails closed")

    malformed = fixture / "malformed-state"
    initialize(malformed)
    malformed_state = malformed / ".specs/STATE.md"
    malformed_state.write_text(
        "# State\n\n## Decisions\n\n### AD-001\n- Decision: preserve me\n\n"
        "## Handoff\n\nnot a field\n",
        encoding="utf-8",
    )
    malformed_before = malformed_state.read_bytes()
    malformed_sha = git(malformed, "rev-parse", "HEAD")
    malformed_write = command(
        *write_args(malformed, malformed_sha, "indeterminate"), cwd=malformed, check=False
    )
    assert malformed_write.returncode == 2
    assert malformed_state.read_bytes() == malformed_before
    print("ok 9 - malformed Handoff rejects writes without changing bytes")

    nested = repo / "nested"
    nested.mkdir()
    root_before = state.read_bytes()
    outside_args = write_args(repo, behavioral_sha, "published")
    outside_args[outside_args.index(str(repo))] = str(nested)
    outside_root = command(*outside_args, cwd=repo, check=False)
    assert outside_root.returncode == 2
    assert state.read_bytes() == root_before
    print("ok 10 - a root outside the Git toplevel fails without changing the real state")

unified_validation = (
    ROOT / ".specs/features/unified-dual-engine-delivery/validation.md"
).read_text(encoding="utf-8")
assert "**Contract status**: PASS" in unified_validation
assert "**Operational status**: UNPROVEN" in unified_validation
assert "**Missing operational evidence**:" in unified_validation
assert "**Overall**: PASS" not in unified_validation
print("ok 11 - workflow validation separates contract from unproven operation")

agents_contract = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
readme_contract = (ROOT / "README.md").read_text(encoding="utf-8")
assert "--format receipt-json" in agents_contract
assert "scripts/workspace-handoff.py status" in agents_contract
assert "<workspace-root>" in readme_contract
assert "`stale`" in readme_contract and "`indeterminate`" in readme_contract
print("ok 12 - engine-facing docs expose receipt and freshness boundaries")

print("\n12 teste(s) passaram.")
