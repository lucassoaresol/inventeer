#!/usr/bin/env python3

import pathlib


ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / ".agents/skills/review-pull-request"


def ok(number: int, message: str) -> None:
    print(f"ok {number} - {message}")


skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
skill_flat = " ".join(skill.split())
assert skill.startswith("---\nname: review-pull-request\n")
assert "[TODO" not in skill
assert "especially another developer's work" in skill
ok(1, "skill metadata targets reviews of another developer's PR")

for phrase in (
    "base ref/SHA, head ref/SHA",
    "Immediately before the verdict",
    "current base SHA and head SHA",
    "If either SHA changed",
    "Never modify product files, branches, worktrees, GitHub, or Linear",
    "Do not post comments, request changes, approve, merge",
):
    assert phrase in skill_flat, f"SKILL.md omits guardrail: {phrase}"
ok(2, "skill binds evidence to immutable identity and remains read-only")

for phrase in (
    "read the target issue once",
    "expand to a parent or related issue only when",
    "Do not run full task preparation by default",
    "Do not use Linear's PR mirror",
    "reuse the previously fetched ancestry and dependencies when it is unchanged",
):
    assert phrase in skill_flat, f"SKILL.md omits progressive Linear rule: {phrase}"
ok(3, "skill loads Linear context progressively and reuses unchanged ancestry")

contract = (SKILL_DIR / "references/review-contract.md").read_text(encoding="utf-8")
for phrase in (
    "Evidence: path and line",
    "accepted-fixed",
    "withdrawn-false-positive",
    "indeterminate",
    "no-confirmed-escape",
    "Never report `no-confirmed-escape` as proven zero escaped defects",
):
    assert phrase in contract, f"review contract omits outcome rule: {phrase}"
assert "Linear issue reads per review" in contract
assert "target-only versus expanded reviews" in contract
assert "Unresolved `P0` or `P1`" in contract
assert "Unresolved `P2`" in contract
assert "base or head changed" in contract
ok(4, "review contract distinguishes outcomes and measures Linear expansion")

metadata = (SKILL_DIR / "agents/openai.yaml").read_text(encoding="utf-8")
assert 'value: "github"' in metadata
assert 'url: "https://api.githubcopilot.com/mcp/"' in metadata
assert "$review-pull-request" in metadata
ok(5, "skill metadata declares its GitHub MCP dependency")

claude_link = ROOT / ".claude/skills/review-pull-request"
assert claude_link.is_symlink(), "Claude skill exposure is not a symlink"
assert claude_link.resolve(strict=True) == SKILL_DIR.resolve(strict=True)
ok(6, "Claude discovers the same skill source through a relative symlink")

agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
assert "Use `review-pull-request` para revisar ou re-revisar uma PR existente" in agents
assert "a skill não corrige código, comenta, aprova nem faz merge" in agents
assert "leia primeiro somente a issue Linear alvo" in agents
ok(7, "workspace instructions route review and constrain Linear traversal")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
assert "| `review-pull-request` | Local |" in readme
assert "thread resolvida ou ausência de correção" in readme
assert "O contexto Linear dessa rota é progressivo" in readme
ok(8, "README documents the review route, Linear scope, and metric limitations")

portal_context = (ROOT / ".agents/skills/portal-task-context/SKILL.md").read_text(encoding="utf-8")
assistants_context = (
    ROOT / ".agents/skills/assistants-task-context/SKILL.md"
).read_text(encoding="utf-8")
for product_skill in (portal_context, assistants_context):
    assert "For review or re-review of an existing GitHub pull request" in product_skill
    assert "preserve `review-pull-request` as the owner of progressive Linear scope" in product_skill
    assert "Resolve its complete parent chain" in product_skill

triage = (ROOT / ".agents/skills/triage-project-cycle/SKILL.md").read_text(encoding="utf-8")
advance = (ROOT / ".agents/skills/advance-delivery-front/SKILL.md").read_text(encoding="utf-8")
assert "Retrieve each selected issue once per timestamped snapshot" in triage
assert "record every expanded identifier and reason" in triage
assert "Read each issue once per timestamped snapshot" in advance
assert "record every additional issue identifier and" in advance
ok(9, "other Linear-aware skills preserve progressive reads or explicit full preparation")

state = (ROOT / ".specs/STATE.md").read_text(encoding="utf-8")
ad_038 = state.split("### AD-038", 1)[1].split("## Handoff", 1)[0]
ad_038_flat = " ".join(ad_038.split())
for phrase in (
    "5–10 reviews reais",
    "7/7",
    "0/7",
    "0 escapes confirmados",
    "24 das 41 reviews estreitas",
    "215 leituras de issue",
    "**Status**: active",
):
    assert phrase in ad_038_flat, f"AD-038 omits pilot evidence: {phrase}"
ok(10, "AD-038 records review, Linear, and prospective pilot evidence")

pilot_helper = ROOT / "scripts/pr-review-pilot.py"
workspace_gate = ROOT / "scripts/test-workspace.sh"
assert pilot_helper.is_file()
assert workspace_gate.is_file()
assert "session-context/review-pilot" in skill
assert "pr-review-pilot.py record" in skill
assert "test-pr-review-pilot.py" in workspace_gate.read_text(encoding="utf-8")
ok(11, "review pilot has sanitized persistence and a unified workspace gate")

print("\n11 teste(s) passaram.")
