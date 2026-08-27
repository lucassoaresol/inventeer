# Symmetric Session Audit Contract Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill: **activate it by name and follow its Execute flow and Critical Rules.** Do not search for skill files by filesystem path. The skill is the source of truth for the full flow (per-task cycle, sub-agent delegation, adequacy review, Verifier, discrimination sensor).

**If the skill cannot be activated, STOP and tell the user - do not proceed without it.**

---

**Design**: none - the change extends an existing report schema; no new component or boundary.
**Status**: Done

---

## Test Coverage Matrix

> Generated from codebase, project guidelines, and spec - confirm before Execute. Guidelines found: `AGENTS.md`, `scripts/test-workspace.sh`.

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| --- | --- | --- | --- | --- |
| Python tooling (`scripts/audit-session-history.py`) | unit + integration | All branches; 1:1 to spec ACs; every listed edge case has a fixture | `scripts/test-session-history-audit.py` | `python3 scripts/test-session-history-audit.py` |
| Workspace instructions (`AGENTS.md`) | integration | Contract clause asserted by the resilience suite | `scripts/test-session-resilience-contract.sh` | `bash scripts/test-session-resilience-contract.sh` |

## Gate Check Commands

| Gate Level | When to Use | Canonical Command | Resource-Aware Equivalent (if needed) |
| --- | --- | --- | --- |
| Quick | After a task touching the auditor | `python3 scripts/test-session-history-audit.py` | N/A |
| Full | After the schema and surfaces agree | `bash scripts/test-workspace.sh` | N/A - pure Python/bash suite |
| Build | Before declaring the feature done | `python3 scripts/workspace-gate-evidence.py run --profile workspace` | N/A |
| Diff integrity | At feature validation, against the evidence range | `git diff --check <evidence-base>..<evidence-head>` | N/A |

## Value Increment Plan

| Value Increment | Outcome | Requirements | Tasks | Terminal Gate | Rollback Boundary | Proposed Commit |
| --- | --- | --- | --- | --- | --- | --- |
| VI-001 | A cohort can be compared field by field across engines, with unmeasurable signals stated as such instead of read as zero | SSA-01..SSA-09 | T1, T2, T3, T4 | Build | Auditor, its suite, and the instruction clause revert as one unit; a partial revert would leave the schema and its renderer disagreeing | `feat(workspace): make the session audit contract symmetric` |

---

## Execution Plan

### Phase 1: Contract and measurement

```
T1 → T2 → T3 → T4
```

---

## Task Breakdown

### T1: Emit a symmetric metric schema

**What:** Give both engine blocks the same metric keys, `null` for unmeasurable ones, plus an `unsupported_metrics` reason map, and bump `contract_version` to 4.
**Where:** `scripts/audit-session-history.py`
**Depends on:** None
**Reuses:** Existing `empty_codex` / `empty_claude` builders and `CONTRACT_VERSION`
**Requirement:** SSA-01, SSA-02, SSA-03
**Value Increment:** VI-001
**Tools:** shell; skill `tlc-spec-driven`
**Done when:**

- [ ] `contract_version` is 4
- [ ] `sorted(codex)` equals `sorted(claude)` for the metric keys
- [ ] Every `null` metric has a non-empty reason; no measured metric appears in the map
- [ ] The empty blocks carry the full key set, so the schema does not depend on data
- [ ] Gate check passes: `python3 scripts/test-session-history-audit.py`
- [ ] Test count: existing assertions plus the new schema cases, none removed

**Tests:** unit
**Gate:** quick

---

### T2: Measure Claude aborts and subagents

**What:** Count aborted turns from exact sentinel text blocks and subagents from the session's `subagents/*.meta.json`, with the derived per-session statistics.
**Where:** `scripts/audit-session-history.py`
**Depends on:** T1
**Reuses:** The Codex derivation of `sessions_with_*`, `max_*_per_session` and percentages
**Requirement:** SSA-04, SSA-05, SSA-06
**Value Increment:** VI-001
**Tools:** shell; skill `tlc-spec-driven`
**Done when:**

- [ ] Only a text block equal to a sentinel counts; substring occurrences and tool results do not
- [ ] `sessions_with_aborts`, `max_aborts_per_session` and the percentage derive from accepted sessions
- [ ] A session without a `subagents` directory counts zero without failing
- [ ] Percentages are 0.0 when no session is accepted
- [ ] Gate check passes: `python3 scripts/test-session-history-audit.py`
- [ ] Test count: existing assertions plus the new measurement cases, none removed

**Tests:** unit
**Gate:** quick

---

### T3: Keep the text and receipt surfaces honest

**What:** Render `n/a` plus the stated reason for unmeasurable metrics and carry the same keys into the receipt.
**Where:** `scripts/audit-session-history.py`
**Depends on:** T2
**Reuses:** `render_text` and `render_receipt`
**Requirement:** SSA-07, SSA-08
**Value Increment:** VI-001
**Tools:** shell; skill `tlc-spec-driven`
**Done when:**

- [ ] A `null` metric prints `n/a`, never `0` or `None`
- [ ] Each unsupported key prints with its reason
- [ ] The receipt carries the same metric keys and reason map
- [ ] The receipt still excludes physical paths and session identifiers
- [ ] Gate check passes: `python3 scripts/test-session-history-audit.py`
- [ ] Test count: existing assertions plus the new surface cases, none removed

**Tests:** unit
**Gate:** quick

---

### T4: Name contract v4 in the workspace instructions

**What:** Update the retrospective clause so the documented contract version matches the emitted one.
**Where:** `AGENTS.md`
**Depends on:** T3
**Reuses:** The existing retrospective clause and its assertion in `scripts/test-session-resilience-contract.sh`
**Requirement:** SSA-09
**Value Increment:** VI-001
**Tools:** shell
**Done when:**

- [ ] The clause names contract v4 and the reason map
- [ ] Gate check passes: `bash scripts/test-workspace.sh`

**Tests:** integration
**Gate:** full

---

## Phase Execution Map

```
Phase 1:  T1 ------→ T2 ------→ T3 ------→ T4
```

Four tasks pack into a single batch, so execution happens inline with no sub-agents.

---

## Task Granularity Check

| Task | Semantic scope | Revert/verification unit | Status |
| --- | --- | --- | --- |
| T1: Symmetric schema | One report contract | Schema assertions + one revert | Granular |
| T2: Claude measurement | Two counters in one scanner | Measurement assertions + one revert | Granular |
| T3: Output surfaces | Two renderers | Surface assertions + one revert | Granular |
| T4: Instruction clause | One documented clause | Resilience suite + one revert | Granular |

---

## Diagram-Definition Cross-Check

| Task | Depends On (task body) | Diagram Shows | Status |
| --- | --- | --- | --- |
| T1 | None | no inbound arrow | Match |
| T2 | T1 | T1 → T2 | Match |
| T3 | T2 | T2 → T3 | Match |
| T4 | T3 | T3 → T4 | Match |

---

## Test Co-location Validation

| Task | Code Layer Created/Modified | Matrix Requires | Task Says | Status |
| --- | --- | --- | --- | --- |
| T1 | Python tooling | unit + integration | unit | OK |
| T2 | Python tooling | unit + integration | unit | OK |
| T3 | Python tooling | unit + integration | unit | OK |
| T4 | Workspace instructions | integration | integration | OK |

T1 to T3 declare `unit` because `test-session-history-audit.py` drives the module against synthetic
transcript fixtures, which is the integration level available for this layer.
