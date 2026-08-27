# Routed Skill Context Preflight Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill: **activate it by name and follow its Execute flow and Critical Rules.** Do not search for skill files by filesystem path. The skill is the source of truth for the full flow (per-task cycle, sub-agent delegation, adequacy review, Verifier, discrimination sensor).

**If the skill cannot be activated, STOP and tell the user - do not proceed without it.**

---

**Design**: none - the change replicates a pattern already established by `discover-project-context`.
**Status**: Done

---

## Test Coverage Matrix

> Generated from codebase, project guidelines, and spec - confirm before Execute. Guidelines found: `AGENTS.md`, `scripts/test-workspace.sh`.

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| --- | --- | --- | --- | --- |
| Skill contracts (`.agents/skills/*/SKILL.md`) | contract | Every routed skill asserted against the manifest, plus each declared failure mode | `scripts/test-workspace-context.py` | `python3 scripts/test-workspace-context.py` |
| Workspace instructions (`AGENTS.md`) | integration | Clause asserted by the resilience suite | `scripts/test-session-resilience-contract.sh` | `bash scripts/test-session-resilience-contract.sh` |

## Gate Check Commands

| Gate Level | When to Use | Canonical Command | Resource-Aware Equivalent (if needed) |
| --- | --- | --- | --- |
| Quick | After a task touching skills or the route contract | `python3 scripts/test-workspace-context.py` | N/A |
| Full | After the declarations and the detector agree | `bash scripts/test-workspace.sh` | N/A - pure Python/bash suite |
| Build | Before declaring the feature done | `python3 scripts/workspace-gate-evidence.py run --profile workspace` | N/A |
| Diff integrity | At feature validation, against the evidence range | `git diff --check <evidence-base>..<evidence-head>` | N/A |

## Value Increment Plan

| Value Increment | Outcome | Requirements | Tasks | Terminal Gate | Rollback Boundary | Proposed Commit |
| --- | --- | --- | --- | --- | --- | --- |
| VI-001 | A routed skill bounds its own context at the moment it starts, and losing that step fails the gate | RCP-01..RCP-07 | T1, T2, T3 | Build | Declarations, detector and instruction clause revert together; a partial revert would leave the detector failing against the skills | `feat(workspace): declare the context preflight inside routed skills` |

---

## Execution Plan

### Phase 1: Declaration and detection

```
T1 → T2 → T3
```

---

## Task Breakdown

### T1: Declare the preflight in every routed skill

**What:** Add the route-specific preflight as the first workflow step of the five routed skills that lack it, renumbering the remaining steps.
**Where:** `.agents/skills/`
**Depends on:** None
**Reuses:** The wording already established as step 1 of `discover-project-context`
**Requirement:** RCP-01, RCP-02, RCP-03, RCP-04
**Value Increment:** VI-001
**Tools:** shell; skill `tlc-spec-driven`
**Done when:**

- [ ] `portal-task-context`, `assistants-task-context`, `review-pull-request`, `triage-project-cycle` and `advance-delivery-front` declare the preflight as workflow step 1
- [ ] Each `--route` value matches the route whose manifest references that skill
- [ ] Remaining steps keep their original order and text, renumbered by one
- [ ] `create-review-bundle` and `tlc-spec-driven` are untouched
- [ ] Gate check passes: `python3 scripts/test-workspace-context.py`

**Tests:** contract
**Gate:** quick

---

### T2: Detect a missing or mismatched declaration

**What:** Assert from the manifest that every routed skill declares its own preflight as the first workflow step.
**Where:** `scripts/test-workspace-context.py`
**Depends on:** T1
**Reuses:** The manifest loading already performed by that suite
**Requirement:** RCP-05, RCP-06
**Value Increment:** VI-001
**Tools:** shell; skill `tlc-spec-driven`
**Done when:**

- [ ] The routed set is derived from the manifest, not hardcoded
- [ ] A missing command, a wrong route, or a demoted step each fail with a message naming the skill
- [ ] A vendored skill referenced by a route is exempt
- [ ] Gate check passes: `python3 scripts/test-workspace-context.py`
- [ ] Test count: existing assertions plus the new contract case, none removed

**Tests:** contract
**Gate:** quick

---

### T3: Point the instructions at the operative location

**What:** State in the workspace instructions that the preflight is a declared first step of each routed skill, keeping the exit semantics.
**Where:** `AGENTS.md`
**Depends on:** T2
**Reuses:** The existing route clause and its assertion in the resilience suite
**Requirement:** RCP-07
**Value Increment:** VI-001
**Tools:** shell
**Done when:**

- [ ] The clause names the routed skills as the point of invocation
- [ ] Exit `1` and exit `2` semantics are preserved
- [ ] Gate check passes: `bash scripts/test-workspace.sh`

**Tests:** integration
**Gate:** full

---

## Phase Execution Map

```
Phase 1:  T1 ------→ T2 ------→ T3
```

Three tasks pack into a single batch, so execution happens inline with no sub-agents.

---

## Task Granularity Check

| Task | Semantic scope | Revert/verification unit | Status |
| --- | --- | --- | --- |
| T1: Declare the preflight | One invariant across five skill files | Contract suite + one revert | Granular - mechanical, one rollback reason |
| T2: Detect regressions | One assertion block | Its own failure cases + one revert | Granular |
| T3: Instruction clause | One documented clause | Resilience suite + one revert | Granular |

---

## Diagram-Definition Cross-Check

| Task | Depends On (task body) | Diagram Shows | Status |
| --- | --- | --- | --- |
| T1 | None | no inbound arrow | Match |
| T2 | T1 | T1 → T2 | Match |
| T3 | T2 | T2 → T3 | Match |

---

## Test Co-location Validation

| Task | Code Layer Created/Modified | Matrix Requires | Task Says | Status |
| --- | --- | --- | --- | --- |
| T1 | Skill contracts | contract | contract | OK |
| T2 | Skill contracts | contract | contract | OK |
| T3 | Workspace instructions | integration | integration | OK |
