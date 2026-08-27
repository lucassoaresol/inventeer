#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import hashlib
import pathlib
import subprocess
import sys
import tempfile


ROOT = pathlib.Path(__file__).resolve().parents[1]
SUBJECT = ROOT / "scripts/audit-session-history.py"
CWD = "/workspace/inventeer"
PRIMARY = "11111111-1111-4111-8111-111111111111"
CONTINUATION = "22222222-2222-4222-8222-222222222222"
SUBAGENT = "33333333-3333-4333-8333-333333333333"
THREAD_SOURCE_SUBAGENT = "16161616-1616-4616-8616-161616161616"
EXCLUDED = "44444444-4444-4444-8444-444444444444"
SHARED_EXCLUDED = "17171717-1717-4717-8717-171717171717"
OUTSIDE_EXCLUSION = "18181818-1818-4818-8818-181818181818"
BACKFILLED = "19191919-1919-4919-8919-191919191919"
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
    aborts: int = 0,
    decoy_aborts: int = 0,
    subagents: int = 0,
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
    for index in range(aborts):
        records.append(
            {
                "type": "user",
                "sessionId": session_id,
                "cwd": initial_cwd,
                "timestamp": timestamp,
                "isSidechain": sidechain,
                "message": {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "[Request interrupted by user]"
                                if index % 2 == 0
                                else "[Request interrupted by user for tool use]"
                            ),
                        }
                    ],
                },
            }
        )
    for _ in range(decoy_aborts):
        # A transcript that merely quotes the sentinel, and a tool result that echoes it. Neither is
        # an abort; substring matching would count both.
        records.append(
            {
                "type": "user",
                "sessionId": session_id,
                "cwd": initial_cwd,
                "timestamp": timestamp,
                "isSidechain": sidechain,
                "message": {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "the log shows [Request interrupted by user] in context",
                        },
                        {
                            "type": "tool_result",
                            "tool_use_id": "decoy",
                            "content": "[Request interrupted by user]",
                        },
                    ],
                },
            }
        )
    if subagents:
        directory = root / session_id / "subagents"
        directory.mkdir(parents=True, exist_ok=True)
        for index in range(subagents):
            (directory / f"agent-{index}.meta.json").write_text("{}", encoding="utf-8")
        (directory / "notes.txt").write_text("not a subagent record", encoding="utf-8")
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
        apex_tool="apex_git_push",
        aborted_turns=9,
        compactions=9,
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
    codex_session(codex_root, SHARED_EXCLUDED)
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

    claude_session(
        claude_root,
        "77777777-7777-4777-8777-777777777777",
        apex_tool="apex_fetch_task",
        aborts=3,
        decoy_aborts=2,
        subagents=4,
    )
    # A sidechain is excluded from the derived population, exactly as in the Codex block.
    claude_session(
        claude_root, "88888888-8888-4888-8888-888888888888", sidechain=True, aborts=5
    )
    claude_session(claude_root, CLAUDE_DENIED, apex_tool="apex_framework_index", outcome="denial")
    claude_session(
        claude_root, CLAUDE_FAILED, apex_tool="apex_run_tests", outcome="failure", aborts=1
    )
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
    claude_session(claude_root, SHARED_EXCLUDED)
    claude_session(
        claude_root,
        CLAUDE_OTHER_RESOURCE,
        resource_server="context7",
        outcome="failure",
    )
    claude_session(
        claude_root,
        "77777777-7777-4777-8777-777777777777",
        apex_tool="apex_open_pr",
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
        "--exclude-session",
        SHARED_EXCLUDED,
        "--exclude-session",
        OUTSIDE_EXCLUSION,
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
        "exclusions_by_engine",
        "exclusions_matched",
        "exclusions_requested",
        "exclusions_unmatched",
        "since",
        "until",
    }
    assert report["contract_version"] == 4
    assert report["since"] == "2026-07-29T00:00:00Z"
    assert report["until"] == UNTIL
    assert report["exclusions_requested"] == 3
    assert report["exclusions_matched"] == 2
    assert report["exclusions_unmatched"] == 1
    assert report["exclusions_by_engine"] == {"codex": 2, "claude": 1}
    assert report["codex"] == {
        "history_root_available": True,
        "matching_history_found": True,
        "files": 6,
        "session_instances": 3,
        "continuations": 1,
        "sidechains": None,
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
        "unsupported_metrics": {
            "sidechains": (
                "Codex writes a subagent to its own session file, so there is no inline sidechain"
                " to count"
            )
        },
    }
    assert report["claude"] == {
        "history_root_available": True,
        "matching_history_found": True,
        "files": 9,
        "session_instances": 7,
        "continuations": None,
        "sidechains": 1,
        "subagents": 4,
        "copies": 1,
        "logical_work_streams": 7,
        "compactions": None,
        "aborted_turns": 4,
        "sessions_with_aborts": 2,
        "sessions_with_compactions": None,
        "max_aborts_per_session": 3,
        "max_compactions_per_session": None,
        "sessions_with_aborts_percent": 28.57,
        "sessions_with_compactions_percent": None,
        "apex_tool_success_sessions": 3,
        "apex_tool_attempt_sessions": 6,
        "apex_tool_successes": {"apex_fetch_task": 2, "read_mcp_resource": 1},
        "apex_tool_failures": {"apex_run_tests": 1},
        "apex_tool_denials": {"apex_framework_index": 1},
        "apex_tool_unresolved": {"apex_list_workspace_repos": 1},
        "unsupported_metrics": {
            "compactions": "no compaction marker appears in this engine's transcript format",
            "continuations": (
                "a resumed Claude session appends to its original transcript, so no second"
                " instance exists"
            ),
            "max_compactions_per_session": (
                "derived from compactions, which this engine does not expose"
            ),
            "sessions_with_compactions": (
                "derived from compactions, which this engine does not expose"
            ),
            "sessions_with_compactions_percent": (
                "derived from compactions, which this engine does not expose"
            ),
        },
    }

    # --- Contrato simétrico -------------------------------------------------
    # A comparação entre engines só é válida se os dois blocos carregarem as mesmas chaves.
    assert sorted(report["codex"]) == sorted(report["claude"])
    for engine in ("codex", "claude"):
        block = report[engine]
        reasons = block["unsupported_metrics"]
        for key, reason in reasons.items():
            assert key in block, f"{engine}: {key} has a reason but is not a field"
            assert block[key] is None, f"{engine}: {key} has a reason but reports {block[key]!r}"
            assert reason.strip(), f"{engine}: {key} has an empty reason"
        for key, value in block.items():
            if value is None:
                assert key in reasons, f"{engine}: {key} is null with no stated reason"
    # A sidechain contributes 5 sentinel records that must not reach the derived population, and
    # the decoy session quotes the sentinel twice without being interrupted.
    assert report["claude"]["aborted_turns"] == 4
    assert report["claude"]["subagents"] == 4
    assert "apex_sessions" not in report["codex"]
    assert "apex_calls" not in report["claude"]

    text_output = subprocess.run(command[:-1] + ["text"], check=True, capture_output=True, text=True)
    assert "logical_work_streams: 2" in text_output.stdout
    assert "Contract version: 4" in text_output.stdout
    assert "Exclusions requested: 3" in text_output.stdout
    assert "Exclusions matched: 2" in text_output.stdout
    assert "Exclusions unmatched: 1" in text_output.stdout
    assert f"Until (exclusive, UTC): {UNTIL}" in text_output.stdout
    assert "sessions_with_aborts_percent: 66.67" in text_output.stdout
    assert "compactions: n/a" in text_output.stdout
    assert "continuations: n/a" in text_output.stdout
    assert "unsupported_metrics:" in text_output.stdout
    assert "no compaction marker appears" in text_output.stdout
    assert "subagents: 4" in text_output.stdout
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
    # --- Guardas do construtor de bloco -------------------------------------
    # engine_block é o único ponto onde as duas engines podem divergir; suas guardas precisam de
    # teste próprio, porque nenhum caminho de dados as exercita.
    # Importing the auditor would drop a __pycache__ next to it; the staged-content guard rejects
    # binaries, so the import must not leave one behind.
    previous_bytecode_setting = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec_module = importlib.util.spec_from_file_location("audit_module", SUBJECT)
        audit = importlib.util.module_from_spec(spec_module)
        spec_module.loader.exec_module(audit)
    finally:
        sys.dont_write_bytecode = previous_bytecode_setting

    try:
        audit.engine_block(
            {"compactions": "unsupported"},
            root_available=True,
            matching_history_found=True,
            compactions=7,
        )
    except ValueError as error:
        assert "unsupported but also measured" in str(error), error
    else:
        raise AssertionError("measuring an unsupported metric must fail closed")

    try:
        audit.engine_block(
            {}, root_available=True, matching_history_found=True, invented_metric=1
        )
    except ValueError as error:
        assert "outside the canonical key set" in str(error), error
    else:
        raise AssertionError("a metric outside the canonical key set must fail closed")

    both = (
        audit.engine_block(audit.CODEX_UNSUPPORTED, root_available=False, matching_history_found=False),
        audit.engine_block(audit.CLAUDE_UNSUPPORTED, root_available=False, matching_history_found=False),
    )
    assert sorted(both[0]) == sorted(both[1])
    print("ok - engine_block guards reject measured-but-unsupported and unknown metrics")

    zero_interruption_metrics = {
        "aborted_turns": 0,
        "compactions": 0,
        "max_aborts_per_session": 0,
        "max_compactions_per_session": 0,
        "sessions_with_aborts": 0,
        "sessions_with_aborts_percent": 0.0,
        "sessions_with_compactions": 0,
        "sessions_with_compactions_percent": 0.0,
    }
    assert missing_report["codex"]["history_root_available"] is False
    assert missing_report["codex"]["matching_history_found"] is False
    assert {
        key: missing_report["codex"][key] for key in zero_interruption_metrics
    } == zero_interruption_metrics
    assert missing_report["claude"]["history_root_available"] is False
    assert missing_report["claude"]["matching_history_found"] is False
    # The schema must not depend on the data: an absent root still carries every key and reason.
    assert sorted(missing_report["claude"]) == sorted(missing_report["codex"])
    assert {
        key: missing_report["claude"][key]
        for key in ("aborted_turns", "subagents", "sessions_with_aborts", "max_aborts_per_session")
    } == {
        "aborted_turns": 0,
        "subagents": 0,
        "sessions_with_aborts": 0,
        "max_aborts_per_session": 0,
    }
    assert missing_report["claude"]["sessions_with_aborts_percent"] == 0.0
    for engine, unsupported in (("codex", {"sidechains"}), ("claude", {
        "compactions",
        "continuations",
        "max_compactions_per_session",
        "sessions_with_compactions",
        "sessions_with_compactions_percent",
    })):
        block = missing_report[engine]
        assert set(block["unsupported_metrics"]) == unsupported
        for key in unsupported:
            assert block[key] is None

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
    assert {
        key: empty_report["codex"][key] for key in zero_interruption_metrics
    } == zero_interruption_metrics
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
    assert subagent_only["session_instances"] == 0
    assert subagent_only["aborted_turns"] == 3
    assert subagent_only["compactions"] == 2
    assert subagent_only["sessions_with_aborts"] == 0
    assert subagent_only["sessions_with_compactions"] == 0
    assert subagent_only["max_aborts_per_session"] == 0
    assert subagent_only["max_compactions_per_session"] == 0
    assert subagent_only["sessions_with_aborts_percent"] == 0.0
    assert subagent_only["sessions_with_compactions_percent"] == 0.0

    portable_receipts = []
    for label in ("machine-a", "machine-b"):
        portable_cwd = f"/{label}/inventeer"
        portable_codex = fixture / label / "codex"
        portable_claude = fixture / label / "claude"
        codex_session(portable_codex, PRIMARY, cwd=portable_cwd)
        claude_session(portable_claude, CLAUDE_DRIFT, initial_cwd=portable_cwd)
        receipt_output = subprocess.run(
            [
                str(SUBJECT),
                "--cwd",
                portable_cwd,
                "--since",
                "2026-07-29",
                "--until",
                UNTIL,
                "--codex-root",
                str(portable_codex),
                "--claude-project",
                str(portable_claude),
                "--workspace-id",
                "inventeer-personal-engineering",
                "--format",
                "receipt-json",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        assert portable_cwd not in receipt_output.stdout
        assert str(portable_codex) not in receipt_output.stdout
        assert PRIMARY not in receipt_output.stdout
        assert CLAUDE_DRIFT not in receipt_output.stdout
        portable_receipts.append(json.loads(receipt_output.stdout))

    assert portable_receipts[0] == portable_receipts[1]
    receipt = portable_receipts[0]
    assert set(receipt) == {
        "auditor_sha256",
        "normalized_arguments",
        "receipt_version",
        "report",
        "report_sha256",
        "source_availability",
        "workspace_id",
        "workspace_root",
    }
    assert receipt["receipt_version"] == 1
    assert receipt["workspace_root"] == "<workspace-root>"
    assert receipt["workspace_id"] == "inventeer-personal-engineering"
    assert receipt["normalized_arguments"] == {
        "cwd": "<workspace-root>",
        "exclude_session_count": 0,
        "format": "receipt-json",
        "since": "2026-07-29T00:00:00Z",
        "until": UNTIL,
    }
    canonical_report = json.dumps(
        receipt["report"], sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    assert receipt["report_sha256"] == hashlib.sha256(canonical_report).hexdigest()
    assert len(receipt["auditor_sha256"]) == 64

    codex_session(portable_codex, BACKFILLED, cwd=portable_cwd)
    backfilled_output = subprocess.run(
        [
            str(SUBJECT),
            "--cwd",
            portable_cwd,
            "--since",
            "2026-07-29",
            "--until",
            UNTIL,
            "--codex-root",
            str(portable_codex),
            "--claude-project",
            str(portable_claude),
            "--workspace-id",
            "inventeer-personal-engineering",
            "--format",
            "receipt-json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    backfilled_receipt = json.loads(backfilled_output.stdout)
    assert backfilled_receipt["report_sha256"] != receipt["report_sha256"]
    assert backfilled_receipt["report"]["since"] == receipt["report"]["since"]
    assert backfilled_receipt["report"]["until"] == receipt["report"]["until"]
    assert "exclusions_matched" in backfilled_receipt["report"]
    assert "exclusions_unmatched" in backfilled_receipt["report"]

    invalid_workspace = subprocess.run(
        [
            str(SUBJECT),
            "--cwd",
            CWD,
            "--workspace-id",
            "",
            "--format",
            "receipt-json",
        ],
        capture_output=True,
        text=True,
    )
    assert invalid_workspace.returncode != 0
    assert invalid_workspace.stderr.strip().startswith("--workspace-id must match")

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
print("ok 15 - exclusion outcomes distinguish requested, matched, and unmatched IDs")
print("ok 16 - cross-engine exclusion totals deduplicate shared IDs")
print("ok 17 - portable receipts bind normalized provenance and report checksums")
print("ok 18 - equivalent cohorts under different roots emit identical receipts")
print("ok 19 - receipt workspace identity fails closed")
print("ok 20 - historical backfill changes the checksum without hiding cohort bounds")
print("\n20 teste(s) passaram.")
