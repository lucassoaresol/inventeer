#!/usr/bin/env python3
"""Behavioral contracts for TLC Value Increment planning."""

from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/tlc-spec-driven"
VALIDATOR = SKILL / "scripts/validate_tasks.py"
COMMIT_VALIDATOR = SKILL / "scripts/check_commit.py"
FEATURE_TASKS = ROOT / ".specs/features/value-oriented-tlc-increments/tasks.md"
HISTORICAL_TASKS = ROOT / ".specs/features/workspace-process-hardening/tasks.md"
WORKSPACE_GATE = ROOT / "scripts/test-workspace.sh"
STATE = ROOT / ".specs/STATE.md"
DECISION_INDEX = ROOT / ".specs/DECISIONS.md"
FEATURE_INDEX = ROOT / ".specs/features/INDEX.md"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_module("validate_tasks", VALIDATOR)
commit_validator = load_module("check_commit", COMMIT_VALIDATOR)


def task_document(*, plan: str, assignments: tuple[str, ...]) -> str:
    task_bodies = []
    for index, assignment in enumerate(assignments, start=1):
        dependency = "None" if index == 1 else f"T{index - 1}"
        task_bodies.append(
            f"""### T{index}: Deliver part {index}

**What:** Produce a bounded part.
**Where:** `src/part{index}.py`
**Depends on:** {dependency}
**Requirement:** VIC-{index:02d}
**Value Increment:** {assignment}
**Tests:** contract
**Gate:** quick
"""
        )
    chain = " -> ".join(f"T{index}" for index in range(1, len(assignments) + 1))
    return f"""# Fixture Tasks

## Test Coverage Matrix

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| --- | --- | --- | --- | --- |
| Contract | contract | Exact outcomes | `scripts/test.py` | `python3 scripts/test.py` |

## Gate Check Commands

| Gate Level | When to Use | Canonical Command | Resource-Aware Equivalent (if needed) |
| --- | --- | --- | --- |
| Quick | Iteration | `python3 scripts/test.py` | N/A |
| Build | Increment close | `bash scripts/test-workspace.sh` | N/A |

## Value Increment Plan

{plan}

## Execution Plan

### Phase 1: Delivery

```text
{chain}
```

## Task Breakdown

{"".join(task_bodies)}
"""


VALID_PLAN = """| Value Increment | Outcome | Requirements | Tasks | Terminal Gate | Rollback Boundary | Proposed Commit |
| --- | --- | --- | --- | --- | --- | --- |
| VI-001 | A complete value is observable. | VIC-01..02 | T1, T2 | Build | Revert the bounded value. | `feat(flow): deliver complete value` |"""


def validate_fixture(content: str) -> tuple[list[str], list[str]]:
    with tempfile.TemporaryDirectory(prefix="inventeer-tlc-vi-") as directory:
        path = Path(directory) / "tasks.md"
        path.write_text(content, encoding="utf-8")
        return validator.check(str(path))


errors, warnings = validate_fixture(task_document(plan=VALID_PLAN, assignments=("VI-001", "VI-001")))
assert not errors, errors
assert not warnings, warnings
print("ok 1 - multiple atomic tasks may belong to one validated value increment")

single_task_plan = VALID_PLAN.replace("VIC-01..02", "VIC-01").replace("T1, T2", "T1")
errors, warnings = validate_fixture(task_document(plan=single_task_plan, assignments=("VI-001",)))
assert not errors, errors
assert not warnings, warnings
print("ok 2 - one atomic task may represent a complete value increment")

invalid_cases = {
    "missing plan": (
        task_document(plan="", assignments=("VI-001", "VI-001")),
        "must contain a header and at least one increment",
    ),
    "missing task assignment": (
        task_document(plan=VALID_PLAN, assignments=("VI-001", "")),
        "T2: missing `Value Increment` field",
    ),
    "unknown task assignment": (
        task_document(plan=VALID_PLAN, assignments=("VI-001", "VI-002")),
        "T2: references unknown value increment VI-002",
    ),
    "malformed increment ID": (
        task_document(
            plan=VALID_PLAN.replace("VI-001", "VI-1"),
            assignments=("VI-1", "VI-1"),
        ),
        "invalid value increment ID: VI-1",
    ),
    "missing outcome": (
        task_document(
            plan=VALID_PLAN.replace("A complete value is observable.", ""),
            assignments=("VI-001", "VI-001"),
        ),
        "VI-001: empty `Outcome`",
    ),
    "missing requirements": (
        task_document(
            plan=VALID_PLAN.replace("VIC-01..02", ""),
            assignments=("VI-001", "VI-001"),
        ),
        "VI-001: empty `Requirements`",
    ),
    "missing terminal gate": (
        task_document(
            plan=VALID_PLAN.replace("| Build |", "|  |"),
            assignments=("VI-001", "VI-001"),
        ),
        "VI-001: empty `Terminal Gate`",
    ),
    "missing rollback boundary": (
        task_document(
            plan=VALID_PLAN.replace("Revert the bounded value.", ""),
            assignments=("VI-001", "VI-001"),
        ),
        "VI-001: empty `Rollback Boundary`",
    ),
    "invalid proposed message": (
        task_document(
            plan=VALID_PLAN.replace(
                "`feat(flow): deliver complete value`",
                "`Deliver complete value.`",
            ),
            assignments=("VI-001", "VI-001"),
        ),
        "VI-001: invalid Conventional Commit proposal",
    ),
    "unknown planned task": (
        task_document(
            plan=VALID_PLAN.replace("T1, T2", "T1, T2, T3"),
            assignments=("VI-001", "VI-001"),
        ),
        "VI-001: references unknown task T3",
    ),
    "task omitted from plan": (
        task_document(
            plan=VALID_PLAN.replace("VIC-01..02", "VIC-01").replace("T1, T2", "T1"),
            assignments=("VI-001", "VI-001"),
        ),
        "T2: is not listed in the Value Increment Plan",
    ),
}
for label, (document, expected_error) in invalid_cases.items():
    errors, _warnings = validate_fixture(document)
    assert any(expected_error in error for error in errors), (label, expected_error, errors)
print("ok 3 - incomplete and inconsistent increment contracts fail closed")

duplicate_plan = VALID_PLAN + "\n| VI-002 | Another value. | VIC-02 | T2 | Build | Revert it. | `fix(flow): correct value` |"
errors, _warnings = validate_fixture(
    task_document(plan=duplicate_plan, assignments=("VI-001", "VI-001"))
)
assert any("multiple value increments" in error for error in errors), errors
print("ok 4 - a task cannot be owned by multiple value increments")

errors, warnings = validator.check(str(FEATURE_TASKS))
assert not errors, errors
assert not warnings, warnings
print("ok 5 - the approved feature plan satisfies its own value-increment schema")

errors, warnings = commit_validator.check("feat(workflow): adopt value-oriented increments")
assert not errors, errors
assert not warnings, warnings
errors, _warnings = commit_validator.check("Adopt value-oriented increments.")
assert errors
print("ok 6 - the commit validator accepts the predominant outcome message")

assert "Value Increment Plan" not in HISTORICAL_TASKS.read_text(encoding="utf-8")
print("ok 7 - prospective adoption leaves a completed historical plan unchanged")

live_files = [
    SKILL / "SKILL.md",
    SKILL / "references/tasks.md",
    SKILL / "references/implement.md",
    SKILL / "references/memory.md",
    SKILL / "references/sub-agents.md",
    SKILL / "references/validate.md",
]
forbidden_task_commit = (
    "one atomic commit per task",
    "each task gets its own commit",
    "one task = one commit",
    "one commit per task",
    "commit per task",
    "never batch multiple tasks into one commit",
    "implement → gate → atomic commit",
)
for path in live_files:
    normalized = " ".join(path.read_text(encoding="utf-8").casefold().split())
    for phrase in forbidden_task_commit:
        assert phrase not in normalized, f"{path.relative_to(ROOT)} retains {phrase!r}"
print("ok 8 - no live TLC instruction requires task-to-commit fragmentation")

required_contracts = {
    SKILL / "SKILL.md": (
        "Tasks stay atomic",
        "one or more tasks that share a verifiable outcome and rollback boundary",
        "commit code, tests, task status, and traceability together only after the increment's terminal gate passes",
        "increment's terminal gate passes",
        "Do not split a `Value Increment` across workers",
    ),
    SKILL / "references/tasks.md": (
        "Value Increment Plan",
        "Rollback Boundary",
        "Every task belongs to exactly one `VI-NNN`",
        "A value increment may contain one task or several sequential tasks",
        "may not split a `Value Increment`",
    ),
    SKILL / "references/implement.md": (
        "Status travels with value",
        "Commit per Value Increment",
        "If the increment remains open, update Handoff with the verified task and exact next task",
        "All tasks in that increment, their tests, and status updates belong to this commit",
        "If a correction is found before the increment is published",
        "If the increment is already published, create a new auditable value increment",
        "local history rewrite has an unclear target",
    ),
    SKILL / "references/memory.md": (
        "inside an open increment",
        "complete increment with a green terminal gate",
    ),
    SKILL / "references/sub-agents.md": (
        "Never split a phase or Value Increment",
        "Value Increments closed",
        "final feature increment is committed",
    ),
    SKILL / "references/validate.md": ("After all Value Increments",),
}
for path, snippets in required_contracts.items():
    text = " ".join(path.read_text(encoding="utf-8").split())
    for snippet in snippets:
        assert snippet in text, f"{path.relative_to(ROOT)} omits {snippet!r}"
print("ok 9 - planning, execution, recovery, batching, and validation share one boundary")

sub_agents = (SKILL / "references/sub-agents.md").read_text(encoding="utf-8")
assert "Standalone fallback" in sub_agents
assert "evidence-or-zero" in sub_agents
assert "discrimination sensor" in sub_agents
for edren_only in ("Never spawn or offer another agent", "same primary session", "single-agent.md"):
    assert edren_only not in "\n".join(path.read_text(encoding="utf-8") for path in live_files)
claude_link = ROOT / ".claude/skills/tlc-spec-driven"
assert claude_link.is_symlink()
assert claude_link.resolve() == SKILL.resolve()
print("ok 10 - dual-engine, opt-in delegation, and standalone verification remain intact")

vendor = (ROOT / ".agents/vendor.json").read_text(encoding="utf-8")
assert "value-oriented increments" in vendor
assert "task-to-commit regression sensor" in vendor
print("ok 11 - vendored customization and its regression sensor are registered")

workspace_gate = WORKSPACE_GATE.read_text(encoding="utf-8")
assert workspace_gate.count('run_suite "TLC value increments"') == 1
assert workspace_gate.count("python3 scripts/test-tlc-value-increments.py") == 1
print("ok 12 - the Value Increment suite is integrated exactly once")

state = STATE.read_text(encoding="utf-8")
decision_index = DECISION_INDEX.read_text(encoding="utf-8")
feature_index = FEATURE_INDEX.read_text(encoding="utf-8")
assert "### AD-047" in state
assert "Planejar e registrar commits TLC por `Value Increment`" in state
assert "Preserva artifacts históricos" in state
assert "Preserva" in state and "AD-040" in state and "AD-045" in state and "AD-046" in state
assert "| [AD-047](STATE.md#ad-047) | active |" in decision_index
assert (
    "| [value-oriented-tlc-increments](./value-oriented-tlc-increments/) | Active |"
    in feature_index
)
print("ok 13 - AD-047 and workspace indexes adopt the prospective dual-engine contract")

print("\n13 contract checks passed.")
