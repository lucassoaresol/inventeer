#!/usr/bin/env python3
"""Contract tests for update-tlc-checkpoint.py."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SUBJECT = ROOT / "scripts" / "update-tlc-checkpoint.py"
ISSUE = "INV-3145"


def args_for(workspace: Path, **overrides: object) -> list[str]:
    values: dict[str, object] = {
        "workspace_root": str(workspace),
        "issue": ISSUE,
        "feature": "Resilient TLC checkpoints",
        "phase_task": "Execute / helper gate",
        "event": "gate",
        "validated_sha": "abc1234",
        "validated_surface": ["scripts/update-tlc-checkpoint.py", "scripts/test-tlc-checkpoint.py"],
        "completed": ["spec", "helper"],
        "process": "focused test complete",
        "next_step": "record the workspace contract",
        "blocker": [],
        "uncommitted_file": ["AGENTS.md", "README.md"],
        "branch": "main",
        "validation_state": "in-progress",
    }
    values.update(overrides)
    result = [
        "--workspace-root",
        str(values["workspace_root"]),
        "--issue",
        str(values["issue"]),
        "--feature",
        str(values["feature"]),
        "--phase-task",
        str(values["phase_task"]),
        "--event",
        str(values["event"]),
        "--validated-sha",
        str(values["validated_sha"]),
        "--process",
        str(values["process"]),
        "--next-step",
        str(values["next_step"]),
        "--branch",
        str(values["branch"]),
        "--validation-state",
        str(values["validation_state"]),
    ]
    for option in ("validated_surface", "completed", "blocker", "uncommitted_file"):
        for value in values[option]:  # type: ignore[union-attr]
            result.extend((f"--{option.replace('_', '-')}", str(value)))
    return result


def invoke(workspace: Path, **overrides: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SUBJECT), *args_for(workspace, **overrides)],
        capture_output=True,
        text=True,
    )


def target_for(workspace: Path) -> Path:
    return workspace / "session-context" / "portal" / ISSUE / "tlc" / "STATE.md"


def expected_handoff() -> str:
    return """## Handoff
- **Feature**: Resilient TLC checkpoints
- **Phase / Task**: Execute / helper gate
- **Completed**: spec, helper
- **Checkpoint event**: gate
- **Validated SHA / surface**: abc1234 — scripts/update-tlc-checkpoint.py, scripts/test-tlc-checkpoint.py
- **In-progress process**: focused test complete
- **Next step**: record the workspace contract
- **Blockers**: none
- **Uncommitted files**: AGENTS.md, README.md
- **Branch**: main
- **Validation state**: in-progress
"""


with tempfile.TemporaryDirectory() as temp:
    fixture = Path(temp)

    creation_root = fixture / "creation"
    creation_root.mkdir()
    created = invoke(creation_root)
    assert created.returncode == 0, created.stderr
    assert created.stdout == "updated\n"
    target = target_for(creation_root)
    assert target.is_file()
    assert target.read_text(encoding="utf-8") == (
        "# TLC State\n\n## Decisions\n\n" + expected_handoff()
    )

    for event in ("gate", "commit", "bundle", "pr", "validation", "pre-heavy"):
        event_root = fixture / f"event-{event}"
        event_root.mkdir()
        event_result = invoke(event_root, event=event)
        assert event_result.returncode == 0, (event, event_result.stderr)
        event_text = target_for(event_root).read_text(encoding="utf-8")
        assert f"- **Checkpoint event**: {event}\n" in event_text

    preservation_root = fixture / "preservation"
    state = target_for(preservation_root)
    state.parent.mkdir(parents=True)
    original = (
        "# TLC State\n\n## Decisions\n\n### TD-001\nkeep: exact\n\n"
        "## Handoff\nold body\n\n## Notes\nkeep this too\n"
    )
    state.write_text(original, encoding="utf-8")
    updated = invoke(preservation_root)
    assert updated.returncode == 0, updated.stderr
    assert state.read_text(encoding="utf-8") == (
        "# TLC State\n\n## Decisions\n\n### TD-001\nkeep: exact\n\n"
        + expected_handoff()
        + "\n## Notes\nkeep this too\n"
    )

    before_bytes = state.read_bytes()
    before_inode = state.stat().st_ino
    unchanged = invoke(preservation_root)
    assert unchanged.returncode == 0, unchanged.stderr
    assert unchanged.stdout == "unchanged\n"
    assert state.read_bytes() == before_bytes
    assert state.stat().st_ino == before_inode

    spec = importlib.util.spec_from_file_location("tlc_checkpoint", SUBJECT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    failure_args = args_for(preservation_root, next_step="changed but replace fails")
    stderr = io.StringIO()
    atomic_events: list[str] = []

    def fail_replace(source: object, destination: object) -> None:
        atomic_events.append("replace")
        assert Path(source).parent == state.parent
        assert Path(destination) == state
        raise OSError("injected replace failure")

    def record_fsync(_descriptor: object) -> None:
        atomic_events.append("fsync")

    with mock.patch.object(module.os, "fsync", side_effect=record_fsync):
        with mock.patch.object(module.os, "replace", side_effect=fail_replace):
            with contextlib.redirect_stderr(stderr):
                return_code = module.main(failure_args)
    assert return_code == 1
    assert atomic_events == ["fsync", "replace"]
    assert "injected replace failure" in stderr.getvalue()
    assert state.read_bytes() == before_bytes
    assert not list(state.parent.glob(".STATE.md.*"))

    invalid_issue_root = fixture / "invalid-issue"
    invalid_issue_root.mkdir()
    invalid_issue = invoke(invalid_issue_root, issue="INV-0")
    assert invalid_issue.returncode != 0
    assert not (invalid_issue_root / "session-context").exists()

    previous = state.read_bytes()
    for unsafe_text in ("bad\nmarkdown", ""):
        invalid_text = invoke(preservation_root, next_step=unsafe_text)
        assert invalid_text.returncode != 0
        assert state.read_bytes() == previous

    for override in ({"event": "push"}, {"validation_state": "done"}):
        invalid_choice = invoke(preservation_root, **override)
        assert invalid_choice.returncode != 0
        assert state.read_bytes() == previous

    escape_root = fixture / "escape"
    escape_root.mkdir()
    outside = fixture / "outside"
    outside.mkdir()
    (escape_root / "session-context").symlink_to(outside, target_is_directory=True)
    escaped = invoke(escape_root)
    assert escaped.returncode != 0
    assert not (outside / "portal").exists()

    for malformed in (
        "# TLC State\n\n## Decisions\n",
        "# TLC State\n\n## Handoff\none\n\n## Handoff\ntwo\n",
    ):
        malformed_root = fixture / f"malformed-{len(malformed)}"
        malformed_state = target_for(malformed_root)
        malformed_state.parent.mkdir(parents=True)
        malformed_state.write_text(malformed, encoding="utf-8")
        malformed_result = invoke(malformed_root)
        assert malformed_result.returncode != 0
        assert malformed_state.read_text(encoding="utf-8") == malformed

    for unsafe_path in ("../secret.txt", "/tmp/secret.txt"):
        unsafe = invoke(preservation_root, uncommitted_file=[unsafe_path])
        assert unsafe.returncode != 0
        assert state.read_bytes() == previous

    empty_lists_root = fixture / "empty-lists"
    empty_lists_root.mkdir()
    empty_lists = invoke(
        empty_lists_root,
        completed=[],
        blocker=[],
        uncommitted_file=[],
    )
    assert empty_lists.returncode == 0, empty_lists.stderr
    empty_text = target_for(empty_lists_root).read_text(encoding="utf-8")
    assert "- **Completed**: none\n" in empty_text
    assert "- **Blockers**: none\n" in empty_text
    assert "- **Uncommitted files**: none\n" in empty_text

print("ok 1 - checkpoint creation uses the exact Portal TLC state path and schema")
print("ok 2 - decisions and following sections are preserved byte for byte")
print("ok 3 - identical input is an inode-preserving no-op")
print("ok 4 - replacement failure preserves prior state and cleans temporary files")
print("ok 5 - invalid issue identifiers create no state")
print("ok 6 - empty and multiline values are rejected without changing prior state")
print("ok 7 - event and validation state enums are enforced")
print("ok 8 - resolved paths cannot escape the workspace")
print("ok 9 - missing or duplicate handoff sections are rejected")
print("ok 10 - uncommitted-file values are relative path labels")
print("ok 11 - empty repeatable fields render as none")
print("ok 12 - all six successful transition events render the exact handoff field")
print("\n12 teste(s) passaram.")
