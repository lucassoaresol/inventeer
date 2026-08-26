#!/usr/bin/env python3
"""Validate the versioned cycle task-clarification contract."""

from __future__ import annotations

import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parents[1]
TASK_ROOT = ROOT / "cycles/10/portal/tasks"
EXPECTED_TASKS = {
    "INV-3828",
    "INV-3830",
    "INV-3831",
    "INV-3832",
    "INV-3833",
    "INV-3834",
    "INV-3847",
    "INV-3875",
    "INV-3941",
}
REQUIRED_HEADINGS = {
    "## Autoridade e atualidade",
    "## Clarificação durável",
    "## Decisões preservadas",
    "## Limites e dependências",
    "## Fontes canônicas a revalidar",
}
FORBIDDEN_PATTERNS = {
    "session-context dependency": re.compile(r"session-context/portal/", re.I),
    "session identifier": re.compile(
        r"\b(?:session|sessão)\s+(?:Codex|Claude\s+)?[0-9a-f]{8}-[0-9a-f-]{20,}", re.I
    ),
    "TLC handoff state": re.compile(
        r"\*\*(?:Phase / Task|Next step|Blockers|Fase / Tarefa|Próximo passo|Bloqueios)\*\*"
    ),
    "review bundle": re.compile(r"\.zip\b|/review/", re.I),
    "raw log path": re.compile(r"(?:api|web)\.log\b", re.I),
    "runtime or branch instruction": re.compile(
        r"\b(?:git\s+(?:push|checkout|merge|rebase)|gh\s+pr|npm\s+run|docker\s+compose)\b",
        re.I,
    ),
    "credential material": re.compile(
        r"\b(?:password|passwd|api[_-]?key|access[_-]?token|bearer)\s*[:=]\s*\S+",
        re.I,
    ),
    "customer data": re.compile(
        r"\b(?:customer|cliente)[_-]?(?:email|name|nome|cpf|cnpj)\s*[:=]\s*\S+",
        re.I,
    ),
    "production output": re.compile(
        r"\bproduction[_-]?(?:response|output|payload|dump)\s*[:=]",
        re.I,
    ),
}


def fail(message: str) -> None:
    raise AssertionError(message)


task_files = sorted(TASK_ROOT.glob("INV-*.md"))
actual_tasks = {path.stem for path in task_files}
if actual_tasks != EXPECTED_TASKS:
    fail(
        "Cycle 10 task set mismatch: "
        f"missing={sorted(EXPECTED_TASKS - actual_tasks)}, "
        f"extra={sorted(actual_tasks - EXPECTED_TASKS)}"
    )
print(f"ok 1 - Cycle 10 indexes the exact {len(EXPECTED_TASKS)} initial Portal tasks")

index_text = (TASK_ROOT / "README.md").read_text(encoding="utf-8")
for task in sorted(EXPECTED_TASKS):
    if f"[{task}](./{task}.md)" not in index_text:
        fail(f"Cycle 10 task index does not link {task}")
print("ok 2 - every promoted task is linked from the Cycle 10 Portal index")

for path in task_files:
    text = path.read_text(encoding="utf-8")
    sections = {
        match.group(1): match.group(2).strip()
        for match in re.finditer(r"^(## [^\n]+)$\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    }
    missing = sorted(REQUIRED_HEADINGS - set(sections))
    if missing:
        fail(f"{path.relative_to(ROOT)} is missing headings: {missing}")
    if not re.search(r"Linear.{0,120}canônic", text, re.S):
        fail(f"{path.relative_to(ROOT)} does not preserve Linear authority")
    if "- **Snapshot:** 2026-" not in text:
        fail(f"{path.relative_to(ROOT)} does not declare a dated snapshot")
    canonical_sources = sections["## Fontes canônicas a revalidar"]
    if not re.search(r"^- Linear:", canonical_sources, re.M):
        fail(f"{path.relative_to(ROOT)} does not name Linear in its canonical sources")
    if not re.search(r"^- .*(?:`repos/|Intenção do Portal|intenção de produto)", canonical_sources, re.M):
        fail(f"{path.relative_to(ROOT)} does not name an applicable product or repository source")
    for label, pattern in FORBIDDEN_PATTERNS.items():
        if pattern.search(text):
            fail(f"{path.relative_to(ROOT)} contains forbidden {label}")
print("ok 3 - task records declare authority, freshness, decisions, boundaries, and sources")

gitignore_lines = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
if "/session-context/" not in gitignore_lines:
    fail(".gitignore no longer ignores the complete session-context tree")
if any(line.startswith("!/session-context/") for line in gitignore_lines):
    fail(".gitignore contains a session-context tracking exception")
print("ok 4 - session-context remains wholly ignored without tracking exceptions")

agents_text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
if not re.search(
    r"cycles/<ciclo>/<produto>/tasks/.*snapshots versionados de clarificação, não\n"
    r"\s+estado operacional nem fonte canônica\. Antes de usá-los, revalide Linear e as fontes do produto\.",
    agents_text,
):
    fail("AGENTS.md does not require canonical revalidation for historical cycle records")
if not re.search(
    r"Se uma INV for materialmente reclarificada em outro ciclo, preserve o snapshot anterior\n"
    r"\s+e crie outro no novo ciclo; Linear continua canônico para o ciclo e estado atuais\.",
    agents_text,
):
    fail("AGENTS.md does not preserve the cross-cycle snapshot lifecycle")
print("ok 5 - agent instructions enforce historical status and canonical revalidation")

cycles_readme = (ROOT / "cycles/README.md").read_text(encoding="utf-8")
if "clarificação materialmente nova" not in cycles_readme:
    fail("cycles lifecycle does not preserve cross-cycle clarification history")
if "O Linear, não" not in cycles_readme:
    fail("cycles lifecycle does not distinguish directory history from current Linear cycle")
if "copie um handoff bruto" not in cycles_readme:
    fail("cycles lifecycle does not forbid raw handoff promotion")
print("ok 6 - promotion and cross-cycle lifecycle are explicit")
