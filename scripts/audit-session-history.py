#!/usr/bin/env python3

"""Summarize local Codex and Claude session history without emitting transcript content."""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import pathlib
import re
from typing import Any, Iterable


UUID_RE = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
    re.IGNORECASE,
)


def parse_timestamp(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    parsed = dt.datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def json_lines(path: pathlib.Path) -> Iterable[dict[str, Any]]:
    try:
        with path.open(encoding="utf-8") as stream:
            for line in stream:
                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(item, dict):
                    yield item
    except OSError:
        return


def message_text(payload: dict[str, Any]) -> str:
    content = payload.get("content", [])
    if not isinstance(content, list):
        return ""
    fragments = []
    for item in content:
        if not isinstance(item, dict):
            continue
        value = item.get("text") or item.get("input_text")
        if isinstance(value, str):
            fragments.append(value)
    return " ".join(fragments)


def continuation_parent(text: str) -> str | None:
    lowered = text.casefold()
    if "caiu" not in lowered or "continu" not in lowered:
        return None
    match = UUID_RE.search(text)
    return match.group(0).lower() if match else None


def empty_codex() -> dict[str, Any]:
    return {
        "files": 0,
        "main_sessions": 0,
        "continuations": 0,
        "subagents": 0,
        "logical_work_streams": 0,
        "apex_sessions": 0,
        "apex_attempt_sessions": 0,
        "apex_calls": {},
        "apex_failures": {},
        "apex_denials": {},
        "apex_unresolved": {},
    }


def scan_codex(
    root: pathlib.Path,
    cwd: str,
    since: dt.datetime,
    excluded: set[str],
) -> dict[str, Any]:
    if not root.is_dir():
        return empty_codex()

    accepted = []
    apex_totals: collections.Counter[str] = collections.Counter()
    apex_failures: collections.Counter[str] = collections.Counter()
    for path in sorted(root.rglob("*.jsonl")):
        metadata = None
        parent = None
        apex_calls: collections.Counter[str] = collections.Counter()
        failed_calls: collections.Counter[str] = collections.Counter()
        for record in json_lines(path):
            payload = record.get("payload", {})
            if not isinstance(payload, dict):
                continue
            if record.get("type") == "session_meta":
                metadata = payload
                continue
            if (
                record.get("type") == "response_item"
                and payload.get("type") == "message"
                and payload.get("role") == "user"
            ):
                parent = parent or continuation_parent(message_text(payload))
                continue
            if record.get("type") == "event_msg" and payload.get("type") == "mcp_tool_call_end":
                invocation = payload.get("invocation", {})
                if isinstance(invocation, dict) and invocation.get("server") == "apex":
                    tool = invocation.get("tool")
                    if isinstance(tool, str) and tool:
                        result = payload.get("result", {})
                        if isinstance(result, dict) and "Ok" in result:
                            apex_calls[tool] += 1
                        else:
                            failed_calls[tool] += 1

        if not metadata or metadata.get("cwd") != cwd:
            continue
        session_id = metadata.get("id")
        timestamp = parse_timestamp(metadata.get("timestamp"))
        if not isinstance(session_id, str) or session_id in excluded:
            continue
        if timestamp is None or timestamp < since:
            continue
        source = metadata.get("source")
        is_subagent = isinstance(source, dict) and "subagent" in source
        accepted.append(
            (
                is_subagent,
                bool(parent) and not is_subagent,
                bool(apex_calls),
                bool(apex_calls or failed_calls),
            )
        )
        apex_totals.update(apex_calls)
        apex_failures.update(failed_calls)

    subagents = sum(is_subagent for is_subagent, _, _, _ in accepted)
    continuations = sum(is_continuation for _, is_continuation, _, _ in accepted)
    main_sessions = len(accepted) - subagents
    return {
        "files": len(accepted),
        "main_sessions": main_sessions,
        "continuations": continuations,
        "subagents": subagents,
        "logical_work_streams": main_sessions - continuations,
        "apex_sessions": sum(has_success for _, _, has_success, _ in accepted),
        "apex_attempt_sessions": sum(has_attempt for _, _, _, has_attempt in accepted),
        "apex_calls": dict(sorted(apex_totals.items())),
        "apex_failures": dict(sorted(apex_failures.items())),
        "apex_denials": {},
        "apex_unresolved": {},
    }


def empty_claude() -> dict[str, Any]:
    return {
        "files": 0,
        "sidechains": 0,
        "logical_sessions": 0,
        "apex_sessions": 0,
        "apex_attempt_sessions": 0,
        "apex_calls": {},
        "apex_failures": {},
        "apex_denials": {},
        "apex_unresolved": {},
    }


def scan_claude(
    project: pathlib.Path,
    cwd: str,
    since: dt.datetime,
    excluded: set[str],
) -> dict[str, Any]:
    if not project.is_dir():
        return empty_claude()

    accepted = []
    apex_totals: collections.Counter[str] = collections.Counter()
    failure_totals: collections.Counter[str] = collections.Counter()
    denial_totals: collections.Counter[str] = collections.Counter()
    unresolved_totals: collections.Counter[str] = collections.Counter()
    for path in sorted(project.glob("*.jsonl")):
        session_id = None
        session_cwd = None
        timestamps = []
        is_sidechain = False
        apex_attempts: dict[str, str] = {}
        apex_outcomes: dict[str, str] = {}
        for record in json_lines(path):
            if isinstance(record.get("sessionId"), str):
                session_id = record["sessionId"]
            if isinstance(record.get("cwd"), str):
                session_cwd = record["cwd"]
            timestamp = parse_timestamp(record.get("timestamp"))
            if timestamp:
                timestamps.append(timestamp)
            is_sidechain = is_sidechain or record.get("isSidechain") is True

            message = record.get("message", {})
            content = message.get("content", []) if isinstance(message, dict) else []
            if not isinstance(content, list):
                continue
            for item in content:
                if not isinstance(item, dict):
                    continue
                if record.get("type") == "assistant" and item.get("type") == "tool_use":
                    tool_id = item.get("id")
                    name = item.get("name")
                    if (
                        isinstance(tool_id, str)
                        and isinstance(name, str)
                        and name.startswith("mcp__apex__")
                    ):
                        apex_attempts[tool_id] = name.removeprefix("mcp__apex__")
                    continue
                if record.get("type") == "user" and item.get("type") == "tool_result":
                    tool_id = item.get("tool_use_id")
                    if not isinstance(tool_id, str) or tool_id not in apex_attempts:
                        continue
                    if record.get("toolDenialKind"):
                        apex_outcomes[tool_id] = "denial"
                    elif item.get("is_error") is True:
                        apex_outcomes[tool_id] = "failure"
                    else:
                        apex_outcomes[tool_id] = "success"

        if session_cwd != cwd or not session_id or session_id in excluded:
            continue
        if not timestamps or min(timestamps) < since:
            continue
        session_successes: collections.Counter[str] = collections.Counter()
        session_failures: collections.Counter[str] = collections.Counter()
        session_denials: collections.Counter[str] = collections.Counter()
        session_unresolved: collections.Counter[str] = collections.Counter()
        for tool_id, tool in apex_attempts.items():
            outcome = apex_outcomes.get(tool_id, "unresolved")
            {
                "success": session_successes,
                "failure": session_failures,
                "denial": session_denials,
                "unresolved": session_unresolved,
            }[outcome][tool] += 1

        accepted.append((is_sidechain, bool(session_successes), bool(apex_attempts)))
        apex_totals.update(session_successes)
        failure_totals.update(session_failures)
        denial_totals.update(session_denials)
        unresolved_totals.update(session_unresolved)

    sidechains = sum(is_sidechain for is_sidechain, _, _ in accepted)
    return {
        "files": len(accepted),
        "sidechains": sidechains,
        "logical_sessions": len(accepted) - sidechains,
        "apex_sessions": sum(has_success for _, has_success, _ in accepted),
        "apex_attempt_sessions": sum(has_attempt for _, _, has_attempt in accepted),
        "apex_calls": dict(sorted(apex_totals.items())),
        "apex_failures": dict(sorted(failure_totals.items())),
        "apex_denials": dict(sorted(denial_totals.items())),
        "apex_unresolved": dict(sorted(unresolved_totals.items())),
    }


def render_text(report: dict[str, Any]) -> str:
    lines = [
        f"Cutoff (UTC): {report['since']}",
        f"Excluded sessions: {report['excluded_sessions']}",
        "",
        "Codex",
    ]
    codex = report["codex"]
    for key in (
        "files",
        "main_sessions",
        "continuations",
        "subagents",
        "logical_work_streams",
        "apex_sessions",
        "apex_attempt_sessions",
    ):
        lines.append(f"  {key}: {codex[key]}")
    lines.append("  apex_calls:")
    lines.extend(f"    {tool}: {count}" for tool, count in codex["apex_calls"].items())
    for key in ("apex_failures", "apex_denials", "apex_unresolved"):
        lines.append(f"  {key}:")
        lines.extend(f"    {tool}: {count}" for tool, count in codex[key].items())

    lines.extend(("", "Claude"))
    claude = report["claude"]
    for key in (
        "files",
        "sidechains",
        "logical_sessions",
        "apex_sessions",
        "apex_attempt_sessions",
    ):
        lines.append(f"  {key}: {claude[key]}")
    lines.append("  apex_calls:")
    lines.extend(f"    {tool}: {count}" for tool, count in claude["apex_calls"].items())
    for key in ("apex_failures", "apex_denials", "apex_unresolved"):
        lines.append(f"  {key}:")
        lines.extend(f"    {tool}: {count}" for tool, count in claude[key].items())
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Aggregate session metadata without emitting transcript content."
    )
    parser.add_argument("--cwd", required=True, help="Exact workspace cwd to include")
    parser.add_argument("--since", default="1970-01-01", help="UTC ISO date or timestamp")
    parser.add_argument("--codex-root", type=pathlib.Path)
    parser.add_argument("--claude-project", type=pathlib.Path)
    parser.add_argument("--exclude-session", action="append", default=[])
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    since = parse_timestamp(args.since)
    if since is None:
        raise SystemExit("--since must be an ISO date or timestamp")

    codex_root = args.codex_root or pathlib.Path.home() / ".codex/sessions"
    claude_project = args.claude_project or (
        pathlib.Path.home() / ".claude/projects" / args.cwd.replace("/", "-")
    )
    excluded = set(args.exclude_session)
    report = {
        "since": since.isoformat().replace("+00:00", "Z"),
        "excluded_sessions": len(excluded),
        "codex": scan_codex(codex_root, args.cwd, since, excluded),
        "claude": scan_claude(claude_project, args.cwd, since, excluded),
    }
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_text(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
