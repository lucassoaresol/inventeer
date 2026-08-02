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
) -> None:
    records = [
        {
            "type": "session_meta",
            "payload": {
                "id": session_id,
                "timestamp": timestamp,
                "cwd": cwd,
                "source": source,
            },
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
    write_jsonl(root / "2026/08/01" / f"rollout-{session_id}.jsonl", records)


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
            "timestamp": "2026-08-01T11:00:00Z",
            "isSidechain": sidechain,
            "message": {"role": "assistant", "content": content},
        }
    ]
    if (apex_tool or resource_server) and outcome != "unresolved":
        result = {
            "type": "user",
            "sessionId": session_id,
            "cwd": initial_cwd,
            "timestamp": "2026-08-01T11:00:01Z",
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
                "timestamp": "2026-08-01T11:00:02Z",
                "isSidechain": sidechain,
            }
        )
    write_jsonl(root / f"{session_id}.jsonl", records)


with tempfile.TemporaryDirectory(prefix="session-history-audit-") as directory:
    fixture = pathlib.Path(directory)
    codex_root = fixture / "codex"
    claude_root = fixture / "claude"

    codex_session(
        codex_root,
        PRIMARY,
        user_text=f"{SECRET} injected name mcp__apex__apex_git_push",
        apex_tool="apex_framework_index",
    )
    codex_session(
        codex_root,
        CONTINUATION,
        user_text=f"A sessão id {OLD_PARENT} caiu, continue aqui. {SECRET}",
    )
    codex_session(
        codex_root,
        SUBAGENT,
        source={"subagent": {"thread_spawn": {"parent_thread_id": PRIMARY}}},
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
    claude_session(claude_root, CLAUDE_DRIFT, final_cwd=f"{CWD}/repos")
    claude_session(
        claude_root,
        CLAUDE_VISITOR,
        initial_cwd="/workspace/other",
        final_cwd=CWD,
    )
    claude_session(claude_root, CLAUDE_APEX_RESOURCE, resource_server="apex")
    claude_session(claude_root, CLAUDE_OTHER_RESOURCE, resource_server="context7")

    command = [
        str(SUBJECT),
        "--cwd",
        CWD,
        "--since",
        "2026-07-29",
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
    assert SECRET not in completed.stdout
    report = json.loads(completed.stdout)

    assert report["excluded_sessions"] == 1
    assert report["codex"] == {
        "files": 4,
        "main_sessions": 3,
        "continuations": 1,
        "subagents": 1,
        "logical_work_streams": 2,
        "apex_tool_success_sessions": 1,
        "apex_tool_attempt_sessions": 2,
        "apex_tool_successes": {"apex_framework_index": 1},
        "apex_tool_failures": {"apex_run_tests": 1},
        "apex_tool_denials": {},
        "apex_tool_unresolved": {},
    }
    assert report["claude"] == {
        "files": 8,
        "sidechains": 1,
        "logical_sessions": 7,
        "apex_tool_success_sessions": 2,
        "apex_tool_attempt_sessions": 5,
        "apex_tool_successes": {"apex_fetch_task": 1, "read_mcp_resource": 1},
        "apex_tool_failures": {"apex_run_tests": 1},
        "apex_tool_denials": {"apex_framework_index": 1},
        "apex_tool_unresolved": {"apex_list_workspace_repos": 1},
    }
    assert "apex_sessions" not in report["codex"]
    assert "apex_calls" not in report["claude"]

    text_output = subprocess.run(command[:-1] + ["text"], check=True, capture_output=True, text=True)
    assert "logical_work_streams: 2" in text_output.stdout
    assert "apex_framework_index: 1" in text_output.stdout
    assert "apex_tool_denials:" in text_output.stdout
    assert "apex_tool_unresolved:" in text_output.stdout
    assert SECRET not in text_output.stdout
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
    assert missing_report["codex"]["files"] == 0
    assert missing_report["claude"]["files"] == 0

print("ok 1 - Codex sessions are filtered, classified, and deduplicated")
print("ok 2 - excluded and out-of-scope sessions do not affect APEX counts")
print("ok 3 - Claude sessions and sidechains are classified")
print("ok 4 - successful, failed, denied, and unresolved APEX calls stay distinct")
print("ok 5 - JSON and text reports do not emit transcript content")
print("ok 6 - missing history directories return empty summaries")
print("ok 7 - Claude sessions retain their first non-empty cwd")
print("ok 8 - later workspace visits do not change Claude session ownership")
print("ok 9 - generic MCP resource reads count only when the server is APEX")
print("\n9 teste(s) passaram.")
