#!/usr/bin/env python3
"""Write and query a freshness-aware handoff for this workspace root."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import stat
import subprocess
import sys
import tempfile
from collections.abc import Sequence


SCHEMA = 1
STATE_RELATIVE = pathlib.Path(".specs/STATE.md")
HANDOFF_HEADER = re.compile(r"(?m)^## Handoff\r?$")
NEXT_SECTION = re.compile(r"(?m)^## [^\r\n]+\r?$")
FIELD = re.compile(r"^- \*\*(?P<label>[^*]+)\*\*: (?P<value>.*)$")
SHA = re.compile(r"[0-9a-f]{40,64}")
PUBLICATION_STATES = ("published", "unpublished", "indeterminate")
TRANSIENT_ACTION = re.compile(
    r"\b(push|pull request|pr|publish|publication|publicar|publicação)\b",
    re.IGNORECASE,
)
REQUIRED_FIELDS = {
    "Feature",
    "Phase / Task",
    "Completed",
    "In progress",
    "Next durable step",
    "Blockers",
    "Uncommitted files",
    "Branch",
    "Contract status",
    "Operational status",
    "Recorded at",
    "Valid at SHA",
    "Publication state",
    "Evidence-only paths",
    "Invalidated by",
}


class HandoffError(RuntimeError):
    """The handoff request or stored state violates the closed contract."""


def run_git(root: pathlib.Path, *args: str, check: bool = True) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=False,
        )
    except OSError as error:
        raise HandoffError("git is unavailable") from error
    if check and result.returncode != 0:
        raise HandoffError("git state is unavailable")
    return result.stdout.strip()


def git_returncode(root: pathlib.Path, *args: str) -> int:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode
    except OSError as error:
        raise HandoffError("git is unavailable") from error


def resolve_root(value: pathlib.Path | str) -> pathlib.Path:
    try:
        root = pathlib.Path(value).resolve(strict=True)
    except OSError as error:
        raise HandoffError("workspace root is unavailable") from error
    if not root.is_dir():
        raise HandoffError("workspace root must be a directory")
    observed = pathlib.Path(run_git(root, "rev-parse", "--show-toplevel")).resolve()
    if observed != root:
        raise HandoffError("workspace root must be the Git toplevel")
    return root


def resolve_state(root: pathlib.Path, *, must_exist: bool = True) -> pathlib.Path:
    target = root / STATE_RELATIVE
    try:
        metadata = target.lstat()
    except FileNotFoundError:
        if must_exist:
            raise HandoffError("state file is missing")
        return target
    except OSError as error:
        raise HandoffError("state file is unavailable") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise HandoffError("state file must be a regular file")
    if not target.resolve(strict=True).is_relative_to(root):
        raise HandoffError("state file resolves outside the workspace")
    return target


def validate_line(label: str, value: str) -> str:
    if not value or "\n" in value or "\r" in value:
        raise HandoffError(f"{label} must be a non-empty single-line value")
    return value


def validate_recorded_at(value: str) -> str:
    validate_line("recorded-at", value)
    if not value.endswith("Z"):
        raise HandoffError("recorded-at must be a UTC ISO timestamp ending in Z")
    try:
        parsed = dt.datetime.fromisoformat(value.removesuffix("Z") + "+00:00")
    except ValueError as error:
        raise HandoffError("recorded-at must be a UTC ISO timestamp ending in Z") from error
    if parsed.utcoffset() != dt.timedelta(0):
        raise HandoffError("recorded-at must be UTC")
    return value


def validate_relative_path(value: str) -> str:
    validate_line("evidence-path", value)
    path = pathlib.PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or value == ".":
        raise HandoffError("evidence-path must be a safe relative path")
    if value != STATE_RELATIVE.as_posix() and not value.startswith(".specs/features/"):
        raise HandoffError("evidence-path must be workspace closure evidence")
    return value


def validate_uncommitted_path(value: str) -> str:
    validate_line("uncommitted-file", value)
    path = pathlib.PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or value == ".":
        raise HandoffError("uncommitted-file must be a safe relative path")
    return value


def display(values: Sequence[str]) -> str:
    return ", ".join(values) if values else "none"


def replace_handoff(source: str, body: str) -> str:
    headers = list(HANDOFF_HEADER.finditer(source))
    if len(headers) != 1:
        raise HandoffError("state file must contain exactly one '## Handoff' section")
    header = headers[0]
    newline = source.find("\n", header.end())
    start = len(source) if newline == -1 else newline + 1
    following = NEXT_SECTION.search(source, start)
    end = following.start() if following else len(source)
    previous_field = False
    labels: set[str] = set()
    for line in source[start:end].splitlines():
        if not line:
            continue
        if line.startswith("  ") and previous_field:
            continue
        match = FIELD.fullmatch(line)
        if match is None or match.group("label") in labels:
            raise HandoffError("existing Handoff is malformed")
        labels.add(match.group("label"))
        previous_field = True
    prefix = source[:start]
    suffix = source[end:]
    return prefix + ("" if prefix.endswith("\n") else "\n") + body + ("\n" if suffix else "") + suffix


def render_handoff(args: argparse.Namespace) -> str:
    fields = (
        ("Feature", args.feature),
        ("Phase / Task", args.phase_task),
        ("Completed", display(args.completed)),
        ("In progress", args.in_progress),
        ("Next durable step", args.next_step),
        ("Blockers", display(args.blocker)),
        ("Uncommitted files", display(args.uncommitted_file)),
        ("Branch", args.branch),
        ("Contract status", args.contract_status),
        ("Operational status", args.operational_status),
        ("Recorded at", args.recorded_at),
        ("Valid at SHA", args.valid_at_sha),
        ("Publication state", args.publication_state),
        ("Evidence-only paths", display(args.evidence_path)),
        (
            "Invalidated by",
            "behavioral SHA ancestry break; non-evidence descendant; publication state change",
        ),
    )
    return "".join(f"- **{label}**: {value}\n" for label, value in fields)


def parse_handoff(source: str) -> dict[str, str]:
    headers = list(HANDOFF_HEADER.finditer(source))
    if len(headers) != 1:
        raise HandoffError("state file must contain exactly one '## Handoff' section")
    header = headers[0]
    newline = source.find("\n", header.end())
    start = len(source) if newline == -1 else newline + 1
    following = NEXT_SECTION.search(source, start)
    end = following.start() if following else len(source)
    fields: dict[str, str] = {}
    for line in source[start:end].splitlines():
        if not line:
            continue
        match = FIELD.fullmatch(line)
        if match is None or match.group("label") in fields:
            raise HandoffError("handoff fields are malformed")
        fields[match.group("label")] = match.group("value")
    if set(fields) != REQUIRED_FIELDS:
        raise HandoffError("handoff fields do not match the freshness schema")
    return fields


def current_publication(root: pathlib.Path, valid_sha: str) -> str | None:
    upstream = run_git(root, "rev-parse", "--verify", "@{upstream}", check=False)
    if not upstream:
        return None
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", valid_sha, upstream],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode == 0:
        return "published"
    if result.returncode == 1:
        return "unpublished"
    return None


def committed_paths(root: pathlib.Path, valid_sha: str) -> set[str]:
    return set(
        filter(None, run_git(root, "diff", "--name-only", f"{valid_sha}..HEAD").splitlines())
    )


def worktree_paths(root: pathlib.Path) -> set[str]:
    worktree = set(
        filter(None, run_git(root, "diff", "--name-only", "HEAD").splitlines())
    )
    staged = set(
        filter(None, run_git(root, "diff", "--cached", "--name-only").splitlines())
    )
    untracked = set(
        filter(None, run_git(root, "ls-files", "--others", "--exclude-standard").splitlines())
    )
    return worktree | staged | untracked


def write_atomic(target: pathlib.Path, content: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=".STATE.md.", dir=target.parent)
    temporary = pathlib.Path(temporary_name)
    try:
        os.fchmod(descriptor, stat.S_IMODE(target.stat().st_mode))
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)


def write_handoff(args: argparse.Namespace) -> str:
    root = resolve_root(args.root)
    target = resolve_state(root)
    for label in (
        "feature",
        "phase-task",
        "in-progress",
        "next-step",
        "branch",
    ):
        validate_line(label, getattr(args, label.replace("-", "_")))
    if TRANSIENT_ACTION.search(args.next_step):
        raise HandoffError("next-step must not contain a transient external action")
    validate_recorded_at(args.recorded_at)
    if SHA.fullmatch(args.valid_at_sha) is None:
        raise HandoffError("valid-at-sha must be a full Git object ID")
    for values, label in ((args.completed, "completed"), (args.blocker, "blocker")):
        for value in values:
            validate_line(label, value)
    evidence_paths = sorted({validate_relative_path(value) for value in args.evidence_path})
    if not evidence_paths:
        raise HandoffError("at least one evidence-path is required")
    args.evidence_path = evidence_paths
    args.uncommitted_file = sorted(
        {validate_uncommitted_path(value) for value in args.uncommitted_file}
    )
    if git_returncode(root, "merge-base", "--is-ancestor", args.valid_at_sha, "HEAD") != 0:
        raise HandoffError("valid-at-sha must be an ancestor of HEAD")
    observed_publication = current_publication(root, args.valid_at_sha)
    if observed_publication is None:
        if args.publication_state != "indeterminate":
            raise HandoffError("publication state is indeterminate without an upstream")
    elif observed_publication != args.publication_state:
        raise HandoffError("publication-state does not match Git")
    source_bytes = target.read_bytes()
    try:
        source = source_bytes.decode("utf-8")
    except UnicodeError as error:
        raise HandoffError("state file must be valid UTF-8") from error
    candidate = replace_handoff(source, render_handoff(args)).encode("utf-8")
    if candidate == source_bytes:
        return "unchanged"
    write_atomic(target, candidate)
    return "updated"


def query_handoff(root_value: pathlib.Path | str) -> tuple[str, str, int]:
    try:
        root = resolve_root(root_value)
        target = resolve_state(root)
        fields = parse_handoff(target.read_text(encoding="utf-8"))
        valid_sha = fields["Valid at SHA"]
        if SHA.fullmatch(valid_sha) is None:
            raise HandoffError("stored valid SHA is malformed")
        if git_returncode(root, "merge-base", "--is-ancestor", valid_sha, "HEAD") != 0:
            return "stale", "sha-changed", 1
        evidence = set(filter(None, fields["Evidence-only paths"].split(", ")))
        recorded_uncommitted = set(
            filter(None, fields["Uncommitted files"].split(", "))
        ) - {"none"}
        if committed_paths(root, valid_sha) - evidence:
            return "stale", "sha-changed", 1
        if worktree_paths(root) - evidence - recorded_uncommitted:
            return "stale", "sha-changed", 1
        observed = current_publication(root, valid_sha)
        if observed is None:
            return "indeterminate", "upstream-unavailable", 2
        if observed != fields["Publication state"]:
            return "stale", "publication-changed", 1
        return "fresh", "match", 0
    except (HandoffError, OSError, UnicodeError):
        return "indeterminate", "handoff-invalid", 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=pathlib.Path, default=pathlib.Path(__file__).resolve().parents[1]
    )
    commands = parser.add_subparsers(dest="command", required=True)
    write = commands.add_parser("write")
    write.add_argument("--feature", required=True)
    write.add_argument("--phase-task", required=True)
    write.add_argument("--completed", action="append", default=[])
    write.add_argument("--in-progress", required=True)
    write.add_argument("--next-step", required=True)
    write.add_argument("--blocker", action="append", default=[])
    write.add_argument("--uncommitted-file", action="append", default=[])
    write.add_argument("--branch", required=True)
    write.add_argument("--contract-status", choices=("PASS", "FAIL", "UNPROVEN"), required=True)
    write.add_argument(
        "--operational-status", choices=("PASS", "FAIL", "UNPROVEN"), required=True
    )
    write.add_argument("--recorded-at", required=True)
    write.add_argument("--valid-at-sha", required=True)
    write.add_argument("--publication-state", choices=PUBLICATION_STATES, required=True)
    write.add_argument("--evidence-path", action="append", required=True)
    commands.add_parser("status")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "status":
        state, reason, exit_code = query_handoff(args.root)
        print(json.dumps({"schema": SCHEMA, "state": state, "reason": reason}, sort_keys=True))
        return exit_code
    try:
        result = write_handoff(args)
    except (HandoffError, OSError) as error:
        print(f"workspace-handoff: {error}", file=sys.stderr)
        return 2
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
