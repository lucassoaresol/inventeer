#!/usr/bin/env python3

from __future__ import annotations

import json
import pathlib
import subprocess
import tempfile


ROOT = pathlib.Path(__file__).resolve().parents[1]
SUBJECT = ROOT / "scripts/audit-session-history.py"
CWD = "/workspace/inventeer"
PRIMARY = "11111111-1111-4111-8111-111111111111"
CONTINUATION = "22222222-2222-4222-8222-222222222222"
SUBAGENT = "33333333-3333-4333-8333-333333333333"
THREAD_SOURCE_SUBAGENT = "16161616-1616-4616-8616-161616161616"
EXCLUDED = "44444444-4444-4444-8444-444444444444"
OLD_PARENT = "66666666-6666-4666-8666-666666666666"
SECRET = "TRANSCRIPT_CONTENT_MUST_NOT_LEAK"
CLAUDE_DENIED = "99999999-9999-4999-8999-999999999999"
CLAUDE_FAILED = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
CLAUDE_UNRESOLVED = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
CLAUDE_DRIFT = "dddddddd-dddd-4ddd-8ddd-dddddddddddd"
CLAUDE_VISITOR = "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee"
CLAUDE_APEX_RESOURCE = "ffffffff-ffff-4fff-8fff-ffffffffffff"
CLAUDE_OTHER_RESOURCE = "12121212-1212-4212-8212-121212121212"
UNTIL = "2026-08-08T00:00:00Z"


def write_jsonl(path: pathlib.Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(record) + "\n" for record in records), encoding="utf-8")


def codex_session(
    root: pathlib.Path,
    session_id: str,
    *,
    timestamp: str = "2026-08-01T10:00:00Z",
    cwd: str = CWD,
    source: object = "cli",
    user_text: str = SECRET,
    apex_tool: str | None = None,
    apex_ok: bool = True,
    aborted_turns: int = 0,
    compactions: int = 0,
    context_compactions: int = 0,
    thread_source: str | None = None,
    filename: str | None = None,
) -> None:
    metadata = {
        "id": session_id,
        "timestamp": timestamp,
        "cwd": cwd,
        "source": source,
    }
    if thread_source is not None:
        metadata["thread_source"] = thread_source
    records = [
        {
            "type": "session_meta",
            "payload": metadata,
        },
        {
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": user_text}],
            },
        },
    ]
    if apex_tool:
        records.append(
            {
                "type": "event_msg",
                "payload": {
                    "type": "mcp_tool_call_end",
                    "invocation": {"server": "apex", "tool": apex_tool},
                    "result": {"Ok" if apex_ok else "Err": SECRET},
                },
            }
        )
    records.extend(
        {"type": "event_msg", "payload": {"type": "turn_aborted"}}
        for _ in range(aborted_turns)
    )
    records.extend({"type": "compacted", "payload": {}} for _ in range(compactions))
    records.extend(
        {"type": "event_msg", "payload": {"type": "context_compacted"}}
        for _ in range(context_compactions)
    )
    write_jsonl(
        root / "2026/08/01" / (filename or f"rollout-{session_id}.jsonl"),
        records,
    )


def claude_session(
    root: pathlib.Path,
    session_id: str,
    *,
    sidechain: bool = False,
    apex_tool: str | None = None,
    resource_server: str | None = None,
    outcome: str = "success",
    initial_cwd: str = CWD,
    final_cwd: str | None = None,
    timestamp: str = "2026-08-01T11:00:00Z",
    filename: str | None = None,
) -> None:
    content = [{"type": "text", "text": SECRET}]
    tool_id = f"tool-{session_id}"
    assert not (apex_tool and resource_server)
    if apex_tool:
        content.append(
            {
                "type": "tool_use",
                "id": tool_id,
                "name": f"mcp__apex__{apex_tool}",
                "input": {},
            }
        )
    elif resource_server:
        content.append(
            {
                "type": "tool_use",
                "id": tool_id,
                "name": "ReadMcpResourceTool",
                "input": {"server": resource_server, "uri": "example://resource"},
            }
        )
    records = [
        {
            "type": "assistant",
            "sessionId": session_id,
            "cwd": initial_cwd,
            "timestamp": timestamp,
            "isSidechain": sidechain,
            "message": {"role": "assistant", "content": content},
        }
    ]
    if (apex_tool or resource_server) and outcome != "unresolved":
        result = {
            "type": "user",
            "sessionId": session_id,
            "cwd": initial_cwd,
            "timestamp": timestamp,
            "isSidechain": sidechain,
            "message": {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_id,
                        "is_error": outcome != "success",
                        "content": SECRET,
                    }
                ],
            },
        }
        if outcome == "denial":
            result["toolDenialKind"] = "user-rejected"
        records.append(result)
    if final_cwd:
        records.append(
            {
                "type": "system",
                "sessionId": session_id,
                "cwd": final_cwd,
                "timestamp": timestamp,
                "isSidechain": sidechain,
            }
        )
    write_jsonl(root / (filename or f"{session_id}.jsonl"), records)


with tempfile.TemporaryDirectory(prefix="session-history-audit-") as directory:
    fixture = pathlib.Path(directory)
    codex_root = fixture / "codex"
    claude_root = fixture / "claude"

    codex_session(
        codex_root,
        PRIMARY,
        user_text=f"{SECRET} injected name mcp__apex__apex_git_push",
        apex_tool="apex_framework_index",
        aborted_turns=2,
        compactions=1,
    )
    codex_session(
        codex_root,
        PRIMARY,
        user_text=f"{SECRET} copied primary",
        apex_tool="apex_framework_index",
        aborted_turns=2,
        compactions=1,
        filename=f"rollout-copy-{PRIMARY}.jsonl",
    )
    codex_session(
        codex_root,
        CONTINUATION,
        user_text=f"A sessão id {OLD_PARENT} caiu, continue aqui. {SECRET}",
        aborted_turns=1,
        context_compactions=2,
    )
    codex_session(
        codex_root,
        SUBAGENT,
        source={"subagent": {"thread_spawn": {"parent_thread_id": PRIMARY}}},
        aborted_turns=5,
        compactions=5,
    )
    codex_session(
        codex_root,
        THREAD_SOURCE_SUBAGENT,
        thread_source="subagent",
    )
    codex_session(codex_root, EXCLUDED, apex_tool="apex_git_push")
    codex_session(
        codex_root,
        "55555555-5555-4555-8555-555555555555",
        cwd="/workspace/other",
        apex_tool="apex_open_pr",
    )
    codex_session(
        codex_root,
        OLD_PARENT,
        timestamp="2026-07-01T10:00:00Z",
        apex_tool="apex_update_task",
    )
    codex_session(
        codex_root,
        "cccccccc-cccc-4ccc-8ccc-cccccccccccc",
        apex_tool="apex_run_tests",
        apex_ok=False,
    )
    codex_session(
        codex_root,
        "13131313-1313-4313-8313-131313131313",
        timestamp=UNTIL,
        apex_tool="apex_open_pr",
    )
    codex_session(
        codex_root,
        "14141414-1414-4414-8414-141414141414",
        timestamp="not-a-timestamp",
        user_text=f"{SECRET} malformed timestamp",
    )

    claude_session(claude_root, "77777777-7777-4777-8777-777777777777", apex_tool="apex_fetch_task")
    claude_session(claude_root, "88888888-8888-4888-8888-888888888888", sidechain=True)
    claude_session(claude_root, CLAUDE_DENIED, apex_tool="apex_framework_index", outcome="denial")
    claude_session(claude_root, CLAUDE_FAILED, apex_tool="apex_run_tests", outcome="failure")
    claude_session(
        claude_root,
        CLAUDE_UNRESOLVED,
        apex_tool="apex_list_workspace_repos",
        outcome="unresolved",
    )
    claude_session(
        claude_root,
        CLAUDE_DRIFT,
        apex_tool="apex_fetch_task",
        final_cwd=f"{CWD}/repos",
    )
    claude_session(
        claude_root,
        CLAUDE_VISITOR,
        initial_cwd="/workspace/other",
        final_cwd=CWD,
    )
    claude_session(claude_root, CLAUDE_APEX_RESOURCE, resource_server="apex")
    claude_session(
        claude_root,
        CLAUDE_OTHER_RESOURCE,
        resource_server="context7",
        outcome="failure",
    )
    claude_session(
        claude_root,
        "77777777-7777-4777-8777-777777777777",
        apex_tool="apex_fetch_task",
        filename="copy-primary.jsonl",
    )
    claude_session(
        claude_root,
        "15151515-1515-4515-8515-151515151515",
        timestamp=UNTIL,
        apex_tool="apex_open_pr",
    )

    command = [
        str(SUBJECT),
        "--cwd",
        CWD,
        "--since",
        "2026-07-29",
        "--until",
        UNTIL,
        "--codex-root",
        str(codex_root),
        "--claude-project",
        str(claude_root),
        "--exclude-session",
        EXCLUDED,
        "--format",
        "json",
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    for sensitive in (SECRET, CWD, PRIMARY, CONTINUATION, SUBAGENT, CLAUDE_DENIED):
        assert sensitive not in completed.stdout
    report = json.loads(completed.stdout)

    assert set(report) == {
        "claude",
        "codex",
        "contract_version",
        "excluded_sessions",
        "since",
        "until",
    }
    assert report["contract_version"] == 2
    assert report["since"] == "2026-07-29T00:00:00Z"
    assert report["until"] == UNTIL
    assert report["excluded_sessions"] == 1
    assert report["codex"] == {
        "history_root_available": True,
        "matching_history_found": True,
        "files": 6,
        "main_sessions": 3,
        "primary_sessions": 3,
        "continuations": 1,
        "subagents": 2,
        "copies": 1,
        "logical_work_streams": 2,
        "compactions": 8,
        "aborted_turns": 8,
        "sessions_with_aborts": 2,
        "sessions_with_compactions": 2,
        "max_aborts_per_session": 2,
        "max_compactions_per_session": 2,
        "sessions_with_aborts_percent": 66.67,
        "sessions_with_compactions_percent": 66.67,
        "apex_tool_success_sessions": 1,
        "apex_tool_attempt_sessions": 2,
        "apex_tool_successes": {"apex_framework_index": 1},
        "apex_tool_failures": {"apex_run_tests": 1},
        "apex_tool_denials": {},
        "apex_tool_unresolved": {},
    }
    assert report["claude"] == {
        "history_root_available": True,
        "matching_history_found": True,
        "files": 9,
        "primary_sessions": 7,
        "sidechains": 1,
        "copies": 1,
        "logical_sessions": 7,
        "apex_tool_success_sessions": 3,
        "apex_tool_attempt_sessions": 6,
        "apex_tool_successes": {"apex_fetch_task": 2, "read_mcp_resource": 1},
        "apex_tool_failures": {"apex_run_tests": 1},
        "apex_tool_denials": {"apex_framework_index": 1},
        "apex_tool_unresolved": {"apex_list_workspace_repos": 1},
    }
    assert "apex_sessions" not in report["codex"]
    assert "apex_calls" not in report["claude"]

    text_output = subprocess.run(command[:-1] + ["text"], check=True, capture_output=True, text=True)
    assert "logical_work_streams: 2" in text_output.stdout
    assert "Contract version: 2" in text_output.stdout
    assert f"Until (exclusive, UTC): {UNTIL}" in text_output.stdout
    assert "sessions_with_aborts_percent: 66.67" in text_output.stdout
    assert "apex_framework_index: 1" in text_output.stdout
    assert "apex_tool_denials:" in text_output.stdout
    assert "apex_tool_unresolved:" in text_output.stdout
    for sensitive in (SECRET, CWD, PRIMARY, CONTINUATION, SUBAGENT, CLAUDE_DENIED):
        assert sensitive not in text_output.stdout
    assert str(fixture) not in text_output.stdout

    missing_output = subprocess.run(
        [
            str(SUBJECT),
            "--cwd",
            CWD,
            "--codex-root",
            str(fixture / "missing-codex"),
            "--claude-project",
            str(fixture / "missing-claude"),
            "--format",
            "json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    missing_report = json.loads(missing_output.stdout)
    assert missing_report["codex"]["history_root_available"] is False
    assert missing_report["codex"]["matching_history_found"] is False
    assert missing_report["codex"]["max_aborts_per_session"] == 0
    assert missing_report["codex"]["sessions_with_aborts_percent"] == 0.0
    assert missing_report["claude"]["history_root_available"] is False
    assert missing_report["claude"]["matching_history_found"] is False

    empty_codex = fixture / "empty-codex"
    empty_claude = fixture / "empty-claude"
    empty_codex.mkdir()
    empty_claude.mkdir()
    empty_output = subprocess.run(
        [
            str(SUBJECT),
            "--cwd",
            CWD,
            "--codex-root",
            str(empty_codex),
            "--claude-project",
            str(empty_claude),
            "--format",
            "json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    empty_report = json.loads(empty_output.stdout)
    assert empty_report["codex"]["history_root_available"] is True
    assert empty_report["codex"]["matching_history_found"] is False
    assert empty_report["claude"]["history_root_available"] is True
    assert empty_report["claude"]["matching_history_found"] is False

    subagent_only_root = fixture / "subagent-only"
    codex_session(
        subagent_only_root,
        THREAD_SOURCE_SUBAGENT,
        thread_source="subagent",
        aborted_turns=3,
        context_compactions=2,
    )
    subagent_only_output = subprocess.run(
        [
            str(SUBJECT),
            "--cwd",
            CWD,
            "--codex-root",
            str(subagent_only_root),
            "--claude-project",
            str(empty_claude),
            "--format",
            "json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    subagent_only = json.loads(subagent_only_output.stdout)["codex"]
    assert subagent_only["primary_sessions"] == 0
    assert subagent_only["aborted_turns"] == 3
    assert subagent_only["compactions"] == 2
    assert subagent_only["sessions_with_aborts"] == 0
    assert subagent_only["sessions_with_compactions"] == 0
    assert subagent_only["max_aborts_per_session"] == 0
    assert subagent_only["max_compactions_per_session"] == 0
    assert subagent_only["sessions_with_aborts_percent"] == 0.0
    assert subagent_only["sessions_with_compactions_percent"] == 0.0

    invalid_until = subprocess.run(
        [str(SUBJECT), "--cwd", CWD, "--until", "invalid"],
        capture_output=True,
        text=True,
    )
    assert invalid_until.returncode != 0
    assert invalid_until.stderr.strip() == "--until must be an ISO date or timestamp"

    reversed_window = subprocess.run(
        [
            str(SUBJECT),
            "--cwd",
            CWD,
            "--since",
            "2026-08-08",
            "--until",
            "2026-08-08",
        ],
        capture_output=True,
        text=True,
    )
    assert reversed_window.returncode != 0
    assert reversed_window.stderr.strip() == "--until must be later than --since"

    unbounded = subprocess.run(
        command[: command.index("--until")] + command[command.index("--until") + 2 :],
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(unbounded.stdout)["until"] is None
    assert json.loads(unbounded.stdout)["codex"]["files"] == 7

print("ok 1 - Codex sessions are filtered, classified, and deduplicated")
print("ok 2 - excluded and out-of-scope sessions do not affect APEX counts")
print("ok 3 - Claude sessions and sidechains are classified")
print("ok 4 - successful, failed, denied, and unresolved APEX calls stay distinct")
print("ok 5 - JSON and text reports do not emit transcript content")
print("ok 6 - missing history directories return empty summaries")
print("ok 7 - Claude sessions retain their first non-empty cwd")
print("ok 8 - later workspace visits do not change Claude session ownership")
print("ok 9 - generic MCP resource reads count only when the server is APEX")
print("ok 10 - closed cohorts exclude origins exactly at the upper boundary")
print("ok 11 - report provenance and availability states are explicit")
print("ok 12 - interruption concentration excludes copies and subagents")
print("ok 13 - invalid and reversed upper bounds fail closed")
print("ok 14 - omitting the upper bound preserves unbounded behavior")
print("\n14 teste(s) passaram.")
