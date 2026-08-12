#!/usr/bin/env python3
"""Write a deterministic Portal + Codex + TLC execution checkpoint."""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Sequence


ISSUE_PATTERN = re.compile(r"INV-[1-9][0-9]*")
HANDOFF_HEADER = re.compile(r"(?m)^## Handoff\r?$")
NEXT_SECTION = re.compile(r"(?m)^## [^\r\n]+\r?$")
EVENTS = ("gate", "commit", "bundle", "pr", "validation", "pre-heavy")
VALIDATION_STATES = ("not-started", "in-progress", "passed", "failed", "blocked")


class CheckpointError(ValueError):
    """A checkpoint request violates the workspace contract."""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Update the issue-local Portal TLC handoff at a stable transition."
    )
    parser.add_argument("--workspace-root", required=True)
    parser.add_argument("--issue", required=True)
    parser.add_argument("--feature", required=True)
    parser.add_argument("--phase-task", required=True)
    parser.add_argument("--completed", action="append", default=[])
    parser.add_argument("--event", choices=EVENTS, required=True)
    parser.add_argument("--validated-sha", required=True)
    parser.add_argument("--validated-surface", action="append", required=True)
    parser.add_argument("--process", required=True)
    parser.add_argument("--next-step", required=True)
    parser.add_argument("--blocker", action="append", default=[])
    parser.add_argument("--uncommitted-file", action="append", default=[])
    parser.add_argument("--branch", required=True)
    parser.add_argument("--validation-state", choices=VALIDATION_STATES, required=True)
    return parser


def validate_line(label: str, value: str) -> str:
    if not value or "\n" in value or "\r" in value:
        raise CheckpointError(f"{label} must be a non-empty single-line value")
    return value


def validate_path_label(value: str) -> str:
    validate_line("uncommitted-file", value)
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or value == ".":
        raise CheckpointError("uncommitted-file must be a relative path label without '..'")
    return value


def display(values: Sequence[str]) -> str:
    return ", ".join(values) if values else "none"


def render_handoff(args: argparse.Namespace) -> str:
    validated = f"{args.validated_sha} — {display(args.validated_surface)}"
    fields = (
        ("Feature", args.feature),
        ("Phase / Task", args.phase_task),
        ("Completed", display(args.completed)),
        ("Checkpoint event", args.event),
        ("Validated SHA / surface", validated),
        ("In-progress process", args.process),
        ("Next step", args.next_step),
        ("Blockers", display(args.blocker)),
        ("Uncommitted files", display(args.uncommitted_file)),
        ("Branch", args.branch),
        ("Validation state", args.validation_state),
    )
    return "".join(f"- **{label}**: {value}\n" for label, value in fields)


def replace_handoff(source: str, body: str) -> str:
    headers = list(HANDOFF_HEADER.finditer(source))
    if len(headers) != 1:
        raise CheckpointError("state file must contain exactly one '## Handoff' section")

    header = headers[0]
    newline = source.find("\n", header.end())
    body_start = len(source) if newline == -1 else newline + 1
    following = NEXT_SECTION.search(source, body_start)
    body_end = following.start() if following else len(source)
    prefix = source[:body_start]
    suffix = source[body_end:]
    separator = "" if prefix.endswith("\n") else "\n"
    following_separator = "\n" if suffix else ""
    return prefix + separator + body + following_separator + suffix


def resolve_target(workspace_root: str, issue: str) -> tuple[Path, Path]:
    if not ISSUE_PATTERN.fullmatch(issue):
        raise CheckpointError("issue must match INV-[1-9][0-9]*")

    supplied_root = Path(workspace_root)
    try:
        root = supplied_root.resolve(strict=True)
    except OSError as error:
        raise CheckpointError(f"workspace root is unavailable: {error}") from error
    if not root.is_dir():
        raise CheckpointError("workspace root must be a directory")

    target = root / "session-context" / "portal" / issue / "tlc" / "STATE.md"
    if target.is_symlink() or not target.resolve(strict=False).is_relative_to(root):
        raise CheckpointError("checkpoint target resolves outside the workspace")
    return root, target


def validate_args(args: argparse.Namespace) -> None:
    scalar_fields = (
        ("feature", args.feature),
        ("phase-task", args.phase_task),
        ("validated-sha", args.validated_sha),
        ("process", args.process),
        ("next-step", args.next_step),
        ("branch", args.branch),
    )
    for label, value in scalar_fields:
        validate_line(label, value)
    for label, values in (
        ("completed", args.completed),
        ("validated-surface", args.validated_surface),
        ("blocker", args.blocker),
    ):
        for value in values:
            validate_line(label, value)
    for value in args.uncommitted_file:
        validate_path_label(value)


def write_atomic(target: Path, content: bytes) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_symlink():
        raise CheckpointError("checkpoint target must not be a symlink")

    descriptor, temporary_name = tempfile.mkstemp(prefix=".STATE.md.", dir=target.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)


def update_checkpoint(args: argparse.Namespace) -> str:
    validate_args(args)
    root, target = resolve_target(args.workspace_root, args.issue)

    if target.exists():
        try:
            source_bytes = target.read_bytes()
            source = source_bytes.decode("utf-8")
        except UnicodeError as error:
            raise CheckpointError("state file must be valid UTF-8") from error
    else:
        source_bytes = b""
        source = "# TLC State\n\n## Decisions\n\n## Handoff\n"

    candidate = replace_handoff(source, render_handoff(args)).encode("utf-8")
    if target.exists() and candidate == source_bytes:
        return "unchanged"

    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.resolve(strict=False).is_relative_to(root):
        raise CheckpointError("checkpoint target resolves outside the workspace")
    write_atomic(target, candidate)
    return "updated"


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        status = update_checkpoint(args)
    except CheckpointError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    except OSError as error:
        print(f"error: checkpoint write failed: {error}", file=sys.stderr)
        return 1
    print(status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
