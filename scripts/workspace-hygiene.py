#!/usr/bin/env python3
"""Inventory lesson and ephemeral workspace hygiene without deleting content."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sys
from typing import Any


ISSUE_RE = re.compile(r"^INV-[1-9][0-9]*$")
RUNTIME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class HygieneError(ValueError):
    """The requested inventory cannot be proven safely."""


def parse_day(value: str, label: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value[:10])
    except (TypeError, ValueError) as error:
        raise HygieneError(f"{label} must start with an ISO date") from error


def load_lessons(root: pathlib.Path, as_of: dt.date) -> dict[str, Any]:
    path = root / ".specs/lessons.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise HygieneError(".specs/lessons.json is unavailable or invalid") from error
    lessons = payload.get("lessons")
    if not isinstance(lessons, list):
        raise HygieneError("lessons must be an array")
    window = payload.get("window_days")
    threshold = payload.get("promote_threshold")
    if not isinstance(window, int) or window <= 0 or not isinstance(threshold, int) or threshold <= 0:
        raise HygieneError("lesson retention settings are invalid")

    counts = {"candidate": 0, "confirmed": 0, "quarantined": 0}
    stale: list[str] = []
    cutoff = as_of - dt.timedelta(days=window)
    for index, lesson in enumerate(lessons):
        if not isinstance(lesson, dict):
            raise HygieneError(f"lessons[{index}] must be an object")
        identifier = lesson.get("id")
        status = lesson.get("status")
        recurrence = lesson.get("recurrence")
        if not isinstance(identifier, str) or status not in counts or not isinstance(recurrence, int):
            raise HygieneError(f"lessons[{index}] has invalid metadata")
        counts[status] += 1
        if status == "candidate" and recurrence < threshold:
            last_seen = parse_day(lesson.get("last_seen"), f"lessons[{index}].last_seen")
            if last_seen < cutoff:
                stale.append(identifier)
    return {
        "status_counts": counts,
        "window_days": window,
        "stale_candidate_ids": sorted(stale),
    }


def validate_issue_evidence(root: pathlib.Path, values: list[str], label: str) -> set[str]:
    result: set[str] = set()
    for value in values:
        if not ISSUE_RE.fullmatch(value):
            raise HygieneError(f"{label} contains an invalid issue identifier")
        target = root / "session-context/portal" / value
        if not target.is_dir() or target.is_symlink():
            raise HygieneError(f"{label} references a missing or unsafe issue directory")
        result.add(value)
    return result


def validate_runtime_evidence(root: pathlib.Path, values: list[str]) -> set[str]:
    result: set[str] = set()
    prefix = pathlib.PurePosixPath("runtime/omc")
    for value in values:
        relative = pathlib.PurePosixPath(value)
        if (
            relative.parent != prefix
            or not RUNTIME_RE.fullmatch(relative.name)
            or value != relative.as_posix()
        ):
            raise HygieneError("ended-runtime must be runtime/omc/<safe-name>")
        target = root / "session-context" / relative
        if not target.is_dir() or target.is_symlink():
            raise HygieneError("ended-runtime references a missing or unsafe runtime directory")
        result.add(relative.name)
    return result


def classify_portal(root: pathlib.Path, merged: set[str], closed: set[str]) -> list[dict[str, str]]:
    portal = root / "session-context/portal"
    if not portal.exists():
        return []
    rows: list[dict[str, str]] = []
    for path in sorted(portal.iterdir(), key=lambda item: item.name):
        relative = f"portal/{path.name}"
        if path.is_symlink():
            state = "protected-symlink"
        elif path.is_dir() and ISSUE_RE.fullmatch(path.name):
            state = "eligible" if path.name in merged and path.name in closed else "external-confirmation-required"
        else:
            state = "protected-unclassified"
        rows.append({"path": relative, "state": state})
    return rows


def classify_runtimes(root: pathlib.Path, ended: set[str]) -> list[dict[str, str]]:
    runtime = root / "session-context/runtime/omc"
    if not runtime.exists():
        return []
    rows: list[dict[str, str]] = []
    for path in sorted(runtime.iterdir(), key=lambda item: item.name):
        relative = f"runtime/omc/{path.name}"
        if path.is_symlink() or not path.is_dir():
            state = "protected-unclassified"
        elif path.name in ended:
            state = "eligible"
        else:
            state = "liveness-confirmation-required"
        rows.append({"path": relative, "state": state})
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=pathlib.Path, default=pathlib.Path(__file__).resolve().parents[1])
    parser.add_argument("--as-of", default=dt.datetime.now(dt.timezone.utc).date().isoformat())
    parser.add_argument("--merged-issue", action="append", default=[])
    parser.add_argument("--closed-issue", action="append", default=[])
    parser.add_argument("--ended-runtime", action="append", default=[])
    return parser.parse_args()


def main() -> int:
    try:
        args = parse_args()
        root = args.root.resolve(strict=True)
        as_of = parse_day(args.as_of, "as-of")
        merged = validate_issue_evidence(root, args.merged_issue, "merged-issue")
        closed = validate_issue_evidence(root, args.closed_issue, "closed-issue")
        ended = validate_runtime_evidence(root, args.ended_runtime)
        report = {
            "schema": 1,
            "as_of": as_of.isoformat(),
            "lessons": load_lessons(root, as_of),
            "session_context": {
                "portal": classify_portal(root, merged, closed),
                "runtimes": classify_runtimes(root, ended),
            },
            "mutation": "none",
        }
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except (HygieneError, OSError) as error:
        print(f"workspace-hygiene: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
