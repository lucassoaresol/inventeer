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
CONTRACT_VERSION = 2


def parse_timestamp(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
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


def codex_subagent(metadata: dict[str, Any]) -> bool:
    if metadata.get("thread_source") == "subagent":
        return True
    source = metadata.get("source")
    return isinstance(source, dict) and "subagent" in source


def empty_codex(*, root_available: bool = False) -> dict[str, Any]:
    return {
        "history_root_available": root_available,
        "matching_history_found": False,
        "files": 0,
        "main_sessions": 0,
        "primary_sessions": 0,
        "continuations": 0,
        "subagents": 0,
        "copies": 0,
        "logical_work_streams": 0,
        "compactions": 0,
        "aborted_turns": 0,
        "sessions_with_aborts": 0,
        "sessions_with_compactions": 0,
        "max_aborts_per_session": 0,
        "max_compactions_per_session": 0,
        "sessions_with_aborts_percent": 0.0,
        "sessions_with_compactions_percent": 0.0,
        "apex_tool_success_sessions": 0,
        "apex_tool_attempt_sessions": 0,
        "apex_tool_successes": {},
        "apex_tool_failures": {},
        "apex_tool_denials": {},
        "apex_tool_unresolved": {},
    }


def scan_codex(
    root: pathlib.Path,
    cwd: str,
    since: dt.datetime,
    until: dt.datetime | None,
    excluded: set[str],
) -> dict[str, Any]:
    if not root.is_dir():
        return empty_codex()

    accepted: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*.jsonl")):
        metadata = None
        parent = None
        apex_calls: collections.Counter[str] = collections.Counter()
        failed_calls: collections.Counter[str] = collections.Counter()
        compacted_records = 0
        context_compactions = 0
        aborted_turns = 0
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
            if record.get("type") == "compacted":
                compacted_records += 1
            if record.get("type") == "event_msg":
                event_type = payload.get("type")
                if event_type == "context_compacted":
                    context_compactions += 1
                elif event_type == "turn_aborted":
                    aborted_turns += 1
                elif event_type == "mcp_tool_call_end":
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
        session_id = metadata.get("id") or metadata.get("session_id")
        timestamp = parse_timestamp(metadata.get("timestamp"))
        if not isinstance(session_id, str):
            continue
        session_id = session_id.lower()
        if session_id in excluded:
            continue
        if timestamp is None or timestamp < since:
            continue
        if until is not None and timestamp >= until:
            continue
        accepted.append(
            {
                "session_id": session_id,
                "subagent": codex_subagent(metadata),
                "continuation": bool(parent),
                "compactions": max(compacted_records, context_compactions),
                "aborted_turns": aborted_turns,
                "apex_successes": apex_calls,
                "apex_failures": failed_calls,
            }
        )

    by_session: dict[str, dict[str, Any]] = {}
    copies = 0
    for item in accepted:
        session_id = item["session_id"]
        if session_id in by_session:
            copies += 1
            continue
        # Sorted path traversal makes the first observation canonical; later files
        # are counted as copies but contribute no session evidence.
        by_session[session_id] = {
            "subagent": item["subagent"],
            "continuation": item["continuation"],
            "compactions": item["compactions"],
            "aborted_turns": item["aborted_turns"],
            "apex_successes": item["apex_successes"].copy(),
            "apex_failures": item["apex_failures"].copy(),
        }

    primary = [item for item in by_session.values() if not item["subagent"]]
    primary_sessions = len(primary)
    continuations = sum(item["continuation"] for item in primary)
    sessions_with_aborts = sum(item["aborted_turns"] > 0 for item in primary)
    sessions_with_compactions = sum(item["compactions"] > 0 for item in primary)

    def primary_percent(count: int) -> float:
        if primary_sessions == 0:
            return 0.0
        return round(count * 100 / primary_sessions, 2)

    apex_totals: collections.Counter[str] = collections.Counter()
    apex_failures: collections.Counter[str] = collections.Counter()
    for item in by_session.values():
        apex_totals.update(item["apex_successes"])
        apex_failures.update(item["apex_failures"])

    return {
        "history_root_available": True,
        "matching_history_found": bool(accepted),
        "files": len(accepted),
        "main_sessions": primary_sessions,
        "primary_sessions": primary_sessions,
        "continuations": continuations,
        "subagents": sum(item["subagent"] for item in by_session.values()),
        "copies": copies,
        "logical_work_streams": primary_sessions - continuations,
        "compactions": sum(item["compactions"] for item in by_session.values()),
        "aborted_turns": sum(item["aborted_turns"] for item in by_session.values()),
        "sessions_with_aborts": sessions_with_aborts,
        "sessions_with_compactions": sessions_with_compactions,
        "max_aborts_per_session": max(
            (item["aborted_turns"] for item in primary), default=0
        ),
        "max_compactions_per_session": max(
            (item["compactions"] for item in primary), default=0
        ),
        "sessions_with_aborts_percent": primary_percent(sessions_with_aborts),
        "sessions_with_compactions_percent": primary_percent(sessions_with_compactions),
        "apex_tool_success_sessions": sum(
            bool(item["apex_successes"]) for item in by_session.values()
        ),
        "apex_tool_attempt_sessions": sum(
            bool(item["apex_successes"] or item["apex_failures"])
            for item in by_session.values()
        ),
        "apex_tool_successes": dict(sorted(apex_totals.items())),
        "apex_tool_failures": dict(sorted(apex_failures.items())),
        "apex_tool_denials": {},
        "apex_tool_unresolved": {},
    }


def empty_claude(*, root_available: bool = False) -> dict[str, Any]:
    return {
        "history_root_available": root_available,
        "matching_history_found": False,
        "files": 0,
        "primary_sessions": 0,
        "sidechains": 0,
        "copies": 0,
        "logical_sessions": 0,
        "apex_tool_success_sessions": 0,
        "apex_tool_attempt_sessions": 0,
        "apex_tool_successes": {},
        "apex_tool_failures": {},
        "apex_tool_denials": {},
        "apex_tool_unresolved": {},
    }


def scan_claude(
    project: pathlib.Path,
    cwd: str,
    since: dt.datetime,
    until: dt.datetime | None,
    excluded: set[str],
) -> dict[str, Any]:
    if not project.is_dir():
        return empty_claude()

    accepted: list[dict[str, Any]] = []
    for path in sorted(project.glob("*.jsonl")):
        session_id = None
        session_origin_cwd = None
        timestamps = []
        is_sidechain = False
        apex_attempts: dict[str, str] = {}
        apex_outcomes: dict[str, str] = {}
        for record in json_lines(path):
            if session_id is None and isinstance(record.get("sessionId"), str):
                session_id = record["sessionId"].lower()
            record_cwd = record.get("cwd")
            if session_origin_cwd is None and isinstance(record_cwd, str) and record_cwd:
                session_origin_cwd = record_cwd
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
                    tool = None
                    if (
                        isinstance(tool_id, str)
                        and isinstance(name, str)
                        and name.startswith("mcp__apex__")
                    ):
                        tool = name.removeprefix("mcp__apex__")
                    elif isinstance(tool_id, str) and name == "ReadMcpResourceTool":
                        tool_input = item.get("input", {})
                        if isinstance(tool_input, dict) and tool_input.get("server") == "apex":
                            tool = "read_mcp_resource"
                    if isinstance(tool_id, str) and tool:
                        apex_attempts[tool_id] = tool
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

        if session_origin_cwd != cwd or not session_id or session_id in excluded:
            continue
        if not timestamps:
            continue
        origin = min(timestamps)
        if origin < since or (until is not None and origin >= until):
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

        accepted.append(
            {
                "session_id": session_id,
                "sidechain": is_sidechain,
                "successes": session_successes,
                "failures": session_failures,
                "denials": session_denials,
                "unresolved": session_unresolved,
            }
        )

    by_session: dict[str, dict[str, Any]] = {}
    copies = 0
    for item in accepted:
        session_id = item["session_id"]
        if session_id in by_session:
            copies += 1
            continue
        by_session[session_id] = {
            "sidechain": item["sidechain"],
            "successes": item["successes"].copy(),
            "failures": item["failures"].copy(),
            "denials": item["denials"].copy(),
            "unresolved": item["unresolved"].copy(),
        }

    apex_totals: collections.Counter[str] = collections.Counter()
    failure_totals: collections.Counter[str] = collections.Counter()
    denial_totals: collections.Counter[str] = collections.Counter()
    unresolved_totals: collections.Counter[str] = collections.Counter()
    for item in by_session.values():
        apex_totals.update(item["successes"])
        failure_totals.update(item["failures"])
        denial_totals.update(item["denials"])
        unresolved_totals.update(item["unresolved"])

    sidechains = sum(item["sidechain"] for item in by_session.values())
    primary_sessions = len(by_session) - sidechains
    return {
        "history_root_available": True,
        "matching_history_found": bool(accepted),
        "files": len(accepted),
        "primary_sessions": primary_sessions,
        "sidechains": sidechains,
        "copies": copies,
        "logical_sessions": primary_sessions,
        "apex_tool_success_sessions": sum(
            bool(item["successes"]) for item in by_session.values()
        ),
        "apex_tool_attempt_sessions": sum(
            bool(
                item["successes"]
                or item["failures"]
                or item["denials"]
                or item["unresolved"]
            )
            for item in by_session.values()
        ),
        "apex_tool_successes": dict(sorted(apex_totals.items())),
        "apex_tool_failures": dict(sorted(failure_totals.items())),
        "apex_tool_denials": dict(sorted(denial_totals.items())),
        "apex_tool_unresolved": dict(sorted(unresolved_totals.items())),
    }


def render_text(report: dict[str, Any]) -> str:
    lines = [
        f"Contract version: {report['contract_version']}",
        f"Since (inclusive, UTC): {report['since']}",
        f"Until (exclusive, UTC): {report['until'] or 'unbounded'}",
        f"Excluded sessions: {report['excluded_sessions']}",
        "",
        "Codex",
    ]
    codex = report["codex"]
    for key in (
        "history_root_available",
        "matching_history_found",
        "files",
        "main_sessions",
        "primary_sessions",
        "continuations",
        "subagents",
        "copies",
        "logical_work_streams",
        "compactions",
        "aborted_turns",
        "sessions_with_aborts",
        "sessions_with_compactions",
        "max_aborts_per_session",
        "max_compactions_per_session",
        "sessions_with_aborts_percent",
        "sessions_with_compactions_percent",
        "apex_tool_success_sessions",
        "apex_tool_attempt_sessions",
    ):
        lines.append(f"  {key}: {codex[key]}")
    lines.append("  apex_tool_successes:")
    lines.extend(
        f"    {tool}: {count}" for tool, count in codex["apex_tool_successes"].items()
    )
    for key in ("apex_tool_failures", "apex_tool_denials", "apex_tool_unresolved"):
        lines.append(f"  {key}:")
        lines.extend(f"    {tool}: {count}" for tool, count in codex[key].items())

    lines.extend(("", "Claude"))
    claude = report["claude"]
    for key in (
        "history_root_available",
        "matching_history_found",
        "files",
        "primary_sessions",
        "sidechains",
        "copies",
        "logical_sessions",
        "apex_tool_success_sessions",
        "apex_tool_attempt_sessions",
    ):
        lines.append(f"  {key}: {claude[key]}")
    lines.append("  apex_tool_successes:")
    lines.extend(
        f"    {tool}: {count}" for tool, count in claude["apex_tool_successes"].items()
    )
    for key in ("apex_tool_failures", "apex_tool_denials", "apex_tool_unresolved"):
        lines.append(f"  {key}:")
        lines.extend(f"    {tool}: {count}" for tool, count in claude[key].items())
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Aggregate session metadata without emitting transcript content."
    )
    parser.add_argument("--cwd", required=True, help="Exact workspace origin cwd to include")
    parser.add_argument("--since", default="1970-01-01", help="UTC ISO date or timestamp")
    parser.add_argument("--until", help="exclusive UTC ISO date or timestamp")
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
    until = parse_timestamp(args.until)
    if args.until is not None and until is None:
        raise SystemExit("--until must be an ISO date or timestamp")
    if until is not None and until <= since:
        raise SystemExit("--until must be later than --since")

    codex_root = args.codex_root or pathlib.Path.home() / ".codex/sessions"
    claude_project = args.claude_project or (
        pathlib.Path.home() / ".claude/projects" / args.cwd.replace("/", "-")
    )
    excluded = {session_id.lower() for session_id in args.exclude_session}
    report = {
        "contract_version": CONTRACT_VERSION,
        "since": since.isoformat().replace("+00:00", "Z"),
        "until": until.isoformat().replace("+00:00", "Z") if until else None,
        "excluded_sessions": len(excluded),
        "codex": scan_codex(codex_root, args.cwd, since, until, excluded),
        "claude": scan_claude(claude_project, args.cwd, since, until, excluded),
    }
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_text(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
