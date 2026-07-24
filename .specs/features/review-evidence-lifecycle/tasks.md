# Review Evidence Lifecycle Tasks

**Status:** Approved

## Test Coverage Matrix

> Generated from `AGENTS.md`, existing skill harnesses, TLC guidance, and the approved spec.

| Layer | Required test | Coverage expectation | Command |
| --- | --- | --- | --- |
| Delivery policy/skill | Fresh-agent/spec evidence | REL-01..06 exact lifecycle outcomes | Independent Verifier |
| Git inspector | Bash integration | REL-07..10 plus prior 12 cases; read-only fingerprint | `bash .agents/skills/advance-delivery-front/scripts/test-inspect-git-front.sh` |
| Bundle script | Bash integration | REL-11..15 plus existing safety cases | `bash .agents/skills/create-review-bundle/scripts/test-create-review-bundle.sh` |
| TLC references | Static contract + script probe | REL-16..21 exact wording/behavior | validator, `rg`, isolated lessons probe |

## Gate Check Commands

| Gate | Command |
| --- | --- |
| Quick | Relevant Bash harness or isolated lessons probe |
| Full | Both Bash harnesses plus three skill validators |
| Build | Full gate + ShellCheck + `git diff --check <evidence-base>..<evidence-head>` |

## Execution Plan

### T1 — Record approved plan

- **Deliverable:** Approved spec, design, and task plan.
- **Files:** `.specs/features/review-evidence-lifecycle/{spec,design,tasks}.md`
- **Tests:** Traceability review for REL-01..21.
- **Gate:** `git diff --check`
- **Commit:** `docs(spec): plan review evidence lifecycle`

### T2 — Make delivery fronts evidence-aware

- **Deliverable:** Lifecycle policy, typed surface, review-change invalidation, inspector schema v2,
  and regression harness.
- **Files:** `advance-delivery-front/SKILL.md`, policy, inspector, inspector harness, metadata if needed.
- **Tests:** Inspector harness and skill validator.
- **Gate:** Quick + ShellCheck.
- **Commit:** `feat(delivery): track review evidence maturity`

### T3 — Add bundle lineage

- **Deliverable:** Parent bundle lineage, stage, path delta, fail-closed checksum/parser behavior.
- **Files:** `create-review-bundle/SKILL.md`, script, harness, metadata if needed.
- **Tests:** Bundle harness and skill validator.
- **Gate:** Quick + ShellCheck.
- **Commit:** `feat(review): link review bundle generations`

### T4 — Refine the local TLC workflow

- **Deliverable:** Compatibility dimension, semantic atomicity, resource-aware gates, disposable-only
  mutations, delivery evidence block, and grounded external review lessons.
- **Files:** TLC references, `scripts/lessons.py`, and focused lessons test.
- **Tests:** Skill validator and isolated lessons probe.
- **Gate:** Quick.
- **Commit:** `feat(tlc-spec-driven): incorporate review lifecycle lessons`

### T5 — Record the transversal decision

- **Deliverable:** AD-023 and updated handoff after implementation.
- **Files:** `.specs/STATE.md`, optional route wording only if behavior changed materially.
- **Tests:** Decision/history integrity and diff check.
- **Gate:** `git diff --check`
- **Commit:** `docs(workspace): adopt review evidence lifecycle`

### T6 — Verify independently

- **Deliverable:** Fresh validation report over the complete commit range and any isolated corrective
  commit required by findings.
- **Files:** `.specs/features/review-evidence-lifecycle/validation.md`; lessons only on grounded signal.
- **Tests:** Build gate, forward-test, and discrimination sensor.
- **Gate:** Build.
- **Commit:** `docs(validation): verify review evidence lifecycle`

## Dependency Check

| Task | Depends on | Valid? |
| --- | --- | --- |
| T1 | none | Yes |
| T2 | T1 | Yes |
| T3 | T1 | Yes |
| T4 | T1 | Yes |
| T5 | T2, T3, T4 | Yes |
| T6 | T5 | Yes |

## Test Co-location Check

| Task | Behavioral change | Co-located test | Valid? |
| --- | --- | --- | --- |
| T2 | Inspector/policy | Inspector harness + verifier fixtures | Yes |
| T3 | Bundle script | Bundle harness | Yes |
| T4 | Lessons parser/reference contract | Focused lessons probe + static contract | Yes |

All tasks represent one reversible semantic increment. Broad mechanical edits within one invariant
remain one task even when they touch several files.

## Execution Record

| Task | Status | Commit / evidence |
| --- | --- | --- |
| T1 | Complete | `f32e75c`; 21/21 requirements traced; diff check passed |
| T2 | Complete | `2b2f94f`; inspector 14/14, ShellCheck and skill validator passed |
| T3 | Complete | `ed28e54` + `c94ca0d`; bundle harness 14/14, ShellCheck and skill validator passed |
| T4 | Complete | `79ac96b` + `b90ab1e`; TLC probes 3/3 and skill validator passed |
| T5 | Complete | `1bf0706`; AD-023, README, handoff, and execution record; whitespace correction `727de55` |
| T6 | Complete | Independent PASS at `aaa2343`; 21/21 requirements, 31/31 tests, 3/3 killed mutants |
