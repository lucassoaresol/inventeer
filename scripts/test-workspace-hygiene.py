#!/usr/bin/env python3
"""Exercise sanitized, evidence-gated workspace hygiene inventory."""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import subprocess
import tempfile


ROOT = pathlib.Path(__file__).resolve().parents[1]
SUBJECT = ROOT / "scripts/workspace-hygiene.py"
SECRET = "LESSON_PROSE_MUST_NOT_APPEAR"


def run(root: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(SUBJECT), "--root", str(root), "--as-of", "2026-08-27", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def fingerprint(root: pathlib.Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix().encode()
        digest.update(relative)
        if path.is_symlink():
            digest.update(b"L" + os.readlink(path).encode())
        elif path.is_file():
            digest.update(b"F" + path.read_bytes())
        elif path.is_dir():
            digest.update(b"D")
    return digest.hexdigest()


with tempfile.TemporaryDirectory() as temporary:
    fixture = pathlib.Path(temporary)
    (fixture / ".specs").mkdir()
    lessons = {
        "promote_threshold": 2,
        "window_days": 45,
        "lessons": [
            {"id": "L-001", "status": "candidate", "recurrence": 1, "last_seen": "2026-06-01T00:00:00Z", "text": SECRET},
            {"id": "L-002", "status": "candidate", "recurrence": 1, "last_seen": "2026-08-20T00:00:00Z", "evidence": [SECRET]},
            {"id": "L-003", "status": "confirmed", "recurrence": 2, "last_seen": "2026-07-01T00:00:00Z"},
        ],
    }
    (fixture / ".specs/lessons.json").write_text(json.dumps(lessons), encoding="utf-8")
    portal = fixture / "session-context/portal"
    (portal / "INV-100").mkdir(parents=True)
    (portal / "INV-200").mkdir()
    (portal / "cycle-local").mkdir()
    os.symlink("INV-100", portal / "INV-300")
    runtimes = fixture / "session-context/runtime/omc"
    (runtimes / "active-runtime").mkdir(parents=True)
    (runtimes / "ended-runtime").mkdir()

    before = fingerprint(fixture)
    result = run(
        fixture,
        "--merged-issue", "INV-100",
        "--closed-issue", "INV-100",
        "--merged-issue", "INV-200",
        "--ended-runtime", "runtime/omc/ended-runtime",
    )
    assert result.returncode == 0, result.stderr
    assert SECRET not in result.stdout
    report = json.loads(result.stdout)
    assert report["mutation"] == "none"
    assert report["lessons"] == {
        "status_counts": {"candidate": 2, "confirmed": 1, "quarantined": 0},
        "stale_candidate_ids": ["L-001"],
        "window_days": 45,
    }
    portal_states = {row["path"]: row["state"] for row in report["session_context"]["portal"]}
    assert portal_states == {
        "portal/INV-100": "eligible",
        "portal/INV-200": "external-confirmation-required",
        "portal/INV-300": "protected-symlink",
        "portal/cycle-local": "protected-unclassified",
    }
    runtime_states = {row["path"]: row["state"] for row in report["session_context"]["runtimes"]}
    assert runtime_states == {
        "runtime/omc/active-runtime": "liveness-confirmation-required",
        "runtime/omc/ended-runtime": "eligible",
    }
    assert fingerprint(fixture) == before
    print("ok 1 - inventory is sanitized, evidence-gated, and byte-identical read-only")

    for args in (
        ("--merged-issue", "INV-0"),
        ("--closed-issue", "INV-999"),
        ("--ended-runtime", "../ended-runtime"),
        ("--ended-runtime", "runtime/omc/missing"),
    ):
        failed = run(fixture, *args)
        assert failed.returncode == 2, (args, failed.stdout, failed.stderr)
        assert fingerprint(fixture) == before
    print("ok 2 - invalid or unprovable lifecycle evidence fails without mutation")

    partial = run(fixture, "--closed-issue", "INV-200")
    assert partial.returncode == 0, partial.stderr
    partial_states = {
        row["path"]: row["state"]
        for row in json.loads(partial.stdout)["session_context"]["portal"]
    }
    assert partial_states["portal/INV-200"] == "external-confirmation-required"
    print("ok 3 - issue eligibility requires merged and closed evidence together")

print("\n3 teste(s) passaram.")
