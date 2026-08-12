#!/usr/bin/env python3
"""Behavioral contract for recoverable root-workspace gate evidence."""

from __future__ import annotations

import importlib.util
import json
import os
import pathlib
import stat
import subprocess
import sys
import tempfile
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[1]
SUBJECT = ROOT / "scripts/workspace-gate-evidence.py"
STORE_RELATIVE = pathlib.Path("session-context/runtime/workspace-gate-evidence-v1.json")
RECEIPT_FIELDS = {
    "schema",
    "profile",
    "result",
    "exit_code",
    "duration_ms",
    "completed_at",
    "state_sha256",
    "contract_sha256",
}


def git(repo: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=repo, text=True, capture_output=True, check=False)


def initialize(repo: pathlib.Path) -> None:
    (repo / "scripts").mkdir(parents=True)
    (repo / ".gitignore").write_text("/session-context/\n", encoding="utf-8")
    (repo / "tracked.txt").write_text("stable\n", encoding="utf-8")
    (repo / "scripts/cache_subject.py").write_text("VALUE = 1\n", encoding="utf-8")
    (repo / "scripts/test-workspace.sh").write_text(
        "#!/usr/bin/env bash\n"
        "python3 -c 'import scripts.cache_subject'\n"
        "echo CHILD_OUTPUT_MUST_NOT_APPEAR\n"
        "control=session-context/control\n"
        "[[ -f \"$control\" ]] && exit \"$(cat \"$control\")\"\n"
        "exit 0\n",
        encoding="utf-8",
    )
    assert git(repo, "init", "--quiet").returncode == 0
    assert git(repo, "config", "user.email", "fixture@example.invalid").returncode == 0
    assert git(repo, "config", "user.name", "Fixture").returncode == 0
    assert git(
        repo,
        "add",
        ".gitignore",
        "tracked.txt",
        "scripts/cache_subject.py",
        "scripts/test-workspace.sh",
    ).returncode == 0
    assert git(repo, "commit", "--quiet", "-m", "fixture").returncode == 0


def cli(repo: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SUBJECT), "--root", str(repo), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def receipt(repo: pathlib.Path) -> dict[str, object]:
    return json.loads((repo / STORE_RELATIVE).read_text(encoding="utf-8"))


with tempfile.TemporaryDirectory() as temporary:
    repo = pathlib.Path(temporary)
    initialize(repo)
    passed = cli(repo, "run", "--profile", "workspace")
    assert passed.returncode == 0, passed.stderr
    assert json.loads(passed.stdout) == {"profile": "workspace", "result": "passed", "schema": 1}
    stored = receipt(repo)
    assert set(stored) == RECEIPT_FIELDS
    assert stored["schema"] == 1 and stored["profile"] == "workspace"
    assert stored["result"] == "passed" and stored["exit_code"] == 0
    assert isinstance(stored["duration_ms"], int) and stored["duration_ms"] >= 0
    assert isinstance(stored["completed_at"], str) and stored["completed_at"].endswith("Z")
    assert all(
        isinstance(stored[field], str) and len(stored[field]) == 64
        for field in ("state_sha256", "contract_sha256")
    )
    serialized = json.dumps(stored)
    for forbidden in (
        "CHILD_OUTPUT_MUST_NOT_APPEAR",
        str(repo),
        "tracked.txt",
        "test-workspace.sh",
        "session",
        "command",
    ):
        assert forbidden not in serialized + passed.stdout + passed.stderr
    store_path = repo / STORE_RELATIVE
    assert stat.S_IMODE(store_path.stat().st_mode) == 0o600
    assert stat.S_IMODE(store_path.parent.stat().st_mode) == 0o700
    assert git(repo, "check-ignore", "-q", str(STORE_RELATIVE)).returncode == 0
    assert not (repo / "scripts/__pycache__").exists()
print("ok 1 - a clean passing gate writes private evidence without mutating the workspace")

with tempfile.TemporaryDirectory() as temporary:
    repo = pathlib.Path(temporary)
    initialize(repo)
    assert cli(repo, "run", "--profile", "workspace").returncode == 0
    reusable = cli(repo, "status", "--profile", "workspace")
    assert reusable.returncode == 0
    assert json.loads(reusable.stdout) == {
        "profile": "workspace",
        "reason": "match",
        "schema": 1,
        "state": "reusable",
    }
    fresh = cli(repo, "status", "--profile", "workspace", "--require-fresh")
    assert fresh.returncode == 1
    assert json.loads(fresh.stdout)["reason"] == "fresh-required"
print("ok 2 - unchanged evidence is reusable but never satisfies an explicit fresh requirement")

with tempfile.TemporaryDirectory() as temporary:
    repo = pathlib.Path(temporary)
    initialize(repo)
    missing = cli(repo, "status", "--profile", "workspace")
    assert missing.returncode == 1 and json.loads(missing.stdout)["reason"] == "evidence-missing"

    assert cli(repo, "run", "--profile", "workspace").returncode == 0
    store_path = repo / STORE_RELATIVE
    valid_bytes = store_path.read_bytes()
    invalid_payloads = (b"not-json\n", b'{"schema":1,"unexpected":true}\n')
    for payload in invalid_payloads:
        store_path.write_bytes(payload)
        invalid = cli(repo, "status", "--profile", "workspace")
        assert invalid.returncode == 2 and json.loads(invalid.stdout)["reason"] == "evidence-invalid"

    store_path.write_bytes(valid_bytes)
    store_path.chmod(0o644)
    permissive = cli(repo, "status", "--profile", "workspace")
    assert permissive.returncode == 2 and json.loads(permissive.stdout)["reason"] == "evidence-invalid"

    store_path.unlink()
    outside = repo / "outside-receipt"
    outside.write_bytes(valid_bytes)
    store_path.symlink_to(outside)
    linked = cli(repo, "status", "--profile", "workspace")
    assert linked.returncode == 2 and json.loads(linked.stdout)["reason"] == "evidence-invalid"

    store_path.unlink()
    runtime = store_path.parent
    runtime.rmdir()
    outside_runtime = repo / "outside-runtime"
    outside_runtime.mkdir()
    outside_store = outside_runtime / STORE_RELATIVE.name
    outside_store.write_bytes(valid_bytes)
    outside_store.chmod(0o600)
    runtime.symlink_to(outside_runtime, target_is_directory=True)
    linked_directory = cli(repo, "status", "--profile", "workspace")
    assert linked_directory.returncode == 2
    assert json.loads(linked_directory.stdout)["reason"] == "evidence-invalid"
print("ok 3 - missing, malformed, permissive, and symlinked evidence fail closed")

with tempfile.TemporaryDirectory() as temporary:
    repo = pathlib.Path(temporary)
    initialize(repo)
    assert cli(repo, "run", "--profile", "workspace").returncode == 0

    (repo / "tracked.txt").write_text("changed\n", encoding="utf-8")
    changed = cli(repo, "status", "--profile", "workspace")
    assert changed.returncode == 1 and json.loads(changed.stdout)["reason"] == "state-changed"
    (repo / "tracked.txt").write_text("stable\n", encoding="utf-8")

    (repo / "untracked.txt").write_text("new\n", encoding="utf-8")
    untracked = cli(repo, "status", "--profile", "workspace")
    assert untracked.returncode == 1 and json.loads(untracked.stdout)["reason"] == "state-changed"
    (repo / "untracked.txt").unlink()

    gate = repo / "scripts/test-workspace.sh"
    gate.write_text(gate.read_text(encoding="utf-8") + "# contract change\n", encoding="utf-8")
    contract = cli(repo, "status", "--profile", "workspace")
    assert contract.returncode == 1 and json.loads(contract.stdout)["reason"] == "contract-changed"
print("ok 4 - tracked, untracked, and contract changes invalidate reuse deterministically")

with tempfile.TemporaryDirectory() as temporary:
    repo = pathlib.Path(temporary)
    initialize(repo)
    assert cli(repo, "run", "--profile", "workspace").returncode == 0
    control = repo / "session-context/control"
    control.parent.mkdir(parents=True, exist_ok=True)
    control.write_text("7\n", encoding="utf-8")
    failed = cli(repo, "run", "--profile", "workspace")
    assert failed.returncode == 7
    assert receipt(repo)["result"] == "failed" and receipt(repo)["exit_code"] == 7
    latest = cli(repo, "status", "--profile", "workspace")
    assert latest.returncode == 1 and json.loads(latest.stdout)["reason"] == "latest-not-passed"
print("ok 5 - a newer failed gate replaces and invalidates an earlier success")

spec = importlib.util.spec_from_file_location("workspace_gate_evidence", SUBJECT)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

with tempfile.TemporaryDirectory() as temporary:
    repo = pathlib.Path(temporary)
    initialize(repo)

    def interrupt(_root: pathlib.Path) -> int:
        raise KeyboardInterrupt

    interrupted = module.execute_gate(repo, run_child=interrupt)
    assert interrupted == 130
    assert receipt(repo)["result"] == "interrupted"

    def mutate(_root: pathlib.Path) -> int:
        (repo / "tracked.txt").write_text("changed during gate\n", encoding="utf-8")
        return 0

    state_changed = module.execute_gate(repo, run_child=mutate)
    assert state_changed == 1
    assert receipt(repo)["result"] == "state-changed"
print("ok 6 - interruption and in-flight state changes persist non-reusable terminal outcomes")

with tempfile.TemporaryDirectory() as temporary:
    repo = pathlib.Path(temporary)
    initialize(repo)
    assert module.execute_gate(repo, run_child=lambda _root: 0) == 0
    store_path = repo / STORE_RELATIVE
    before = store_path.read_bytes()
    with mock.patch.object(module.os, "replace", side_effect=OSError("injected")):
        try:
            module.execute_gate(repo, run_child=lambda _root: 7)
        except module.EvidenceError:
            pass
        else:
            raise AssertionError("atomic write failure unexpectedly passed")
    assert store_path.read_bytes() == before
    assert not list(store_path.parent.glob(".workspace-gate-evidence.*"))
print("ok 7 - atomic receipt failure preserves the prior complete receipt")

with tempfile.TemporaryDirectory() as temporary:
    repo = pathlib.Path(temporary)
    initialize(repo)
    gate = repo / "scripts/test-workspace.sh"
    gate.write_text(
        "#!/usr/bin/env bash\nprintf changed-during-run > tracked.txt\nexit 0\n",
        encoding="utf-8",
    )
    raced = cli(repo, "run", "--profile", "workspace")
    assert raced.returncode == 1
    assert receipt(repo)["result"] == "state-changed"
print("ok 8 - the CLI records state-changed when the workspace mutates during the gate")

unknown = subprocess.run(
    [sys.executable, str(SUBJECT), "status", "--profile", "unknown"],
    cwd=ROOT,
    text=True,
    capture_output=True,
    check=False,
)
assert unknown.returncode == 2
print("ok 9 - profiles outside the root workspace allowlist are rejected")

agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
readme = (ROOT / "README.md").read_text(encoding="utf-8")
for required in (
    "workspace-gate-evidence.py run --profile workspace",
    "workspace-gate-evidence.py status --profile workspace",
    "não substitui validação terminal fresca",
):
    assert required in agents
    assert required in readme
assert "test-workspace-gate-evidence.py" in (ROOT / "scripts/test-workspace.sh").read_text(encoding="utf-8")
print("ok 10 - workspace instructions bound reuse and keep fresh validation mandatory")
