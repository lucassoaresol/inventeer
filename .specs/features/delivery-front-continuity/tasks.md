# Delivery Front Continuity Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill: **activate it by name and follow its Execute
flow and Critical Rules.** Do not search for skill files by filesystem path. The skill is the source
of truth for the per-task cycle, commits, adequacy review, Verifier and discrimination sensor.

**If the skill cannot be activated, STOP and tell the user — do not proceed without it.**

---

**Design**: `.specs/features/delivery-front-continuity/design.md`
**Status**: Complete — implementation and independent verification passed

---

## Execution Preconditions

After task approval and before T1:

1. Read `tlc-spec-driven` `implement.md` completely and reconfirm AD-022.
2. Confirm the worktree contains only the approved planning artifacts.
3. Commit `spec.md`, `design.md`, `tasks.md` and the section-scoped `.specs/STATE.md` update as the
   planning baseline `docs(spec): plan delivery front continuity`. This is a phase-transition record,
   not an implementation task, and must contain no skill implementation files.
4. Initialize the new local skill with the `skill-creator` initializer, resources `scripts,references`,
   the approved interface values and output path `.agents/skills`. Do not use example placeholders.
5. Keep initializer placeholders uncommitted until their owning task replaces them. Stage and commit
   only the files named by the current task.

No precondition authorizes changes to product repositories, Linear, GitHub or remote Git state.

## Test Coverage Matrix

> Generated from codebase, project guidelines, and spec — confirm before Execute. Guidelines found:
> `AGENTS.md`, `README.md`, `.specs/STATE.md`, `skill-creator/SKILL.md`; existing style sampled from
> `.agents/skills/create-review-bundle/scripts/test-create-review-bundle.sh`. No numeric coverage
> threshold exists, so strong defaults apply to the workflow and executable branches.

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| --- | --- | --- | --- | --- |
| Agent workflow (`SKILL.md` + policy consumption) | forward-test | All DFC-01..22 outcomes and every spec edge/failure case through raw synthetic delivery snapshots; no live mutations | Fresh-agent runs recorded by the TLC Verifier in `.specs/features/delivery-front-continuity/validation.md` | Fresh-agent forward-test via collaboration, followed by the TLC Verifier |
| Git inspector CLI | integration | All argument/output branches, independent/dependent ancestry, dirty/unusual paths, linked worktrees, invalid refs and before/after immutability | `.agents/skills/advance-delivery-front/scripts/test-inspect-git-front.sh` | `bash .agents/skills/advance-delivery-front/scripts/test-inspect-git-front.sh` |
| Policy/reference documentation | none | Build gate; behavior is exercised when the workflow consumes the reference | `.agents/skills/advance-delivery-front/references/*.md` | Build gate only |
| Skill interface metadata | none | Generated fields match approved design; YAML/frontmatter validation passes | `.agents/skills/advance-delivery-front/agents/openai.yaml` | Build gate only |
| Workspace routing documentation | none | Inventory, trigger route, handoff and read-only boundary remain consistent | `README.md`, `AGENTS.md` | Build gate only |

## Gate Check Commands

> Generated from existing workspace scripts and installed tools — confirm before Execute. Run each
> command separately; a gate passes only if every listed command exits zero.

| Gate Level | When to Use | Commands |
| --- | --- | --- |
| Quick | Reference or documentation-only task | `git diff --check` |
| Full | Git inspector implementation | `bash .agents/skills/advance-delivery-front/scripts/test-inspect-git-front.sh`<br>`shellcheck .agents/skills/advance-delivery-front/scripts/inspect-git-front.sh .agents/skills/advance-delivery-front/scripts/test-inspect-git-front.sh`<br>`git diff --check` |
| Build | Skill, metadata or phase completion | `python3 /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/advance-delivery-front`<br>`bash .agents/skills/advance-delivery-front/scripts/test-inspect-git-front.sh`<br>`shellcheck .agents/skills/advance-delivery-front/scripts/inspect-git-front.sh .agents/skills/advance-delivery-front/scripts/test-inspect-git-front.sh`<br>`git diff --check` |
| Verification | Agent workflow task and final feature gate | Fresh-agent forward-tests against the five fixture groups below; after T6, automatic TLC Verifier with spec-anchored check and discrimination sensor |

The five forward-test fixture groups are:

1. ready PR + independent candidates + dirty worktree;
2. one dependent draft with squash boundary and promotion conditions;
3. base PR updated, then closed without merge;
4. missing source, cross-repo order and WIP-cap exhaustion;
5. unexpected base-task paths plus an out-of-contract local artifact.

Together they must exercise all DFC-01..22 outcomes. Each forward-test receives only the implemented
skill and raw fixture evidence, not the intended classification or expected answer.

## Execution Plan

Phases and tasks execute strictly in order.

### Phase 1: Policy and Deterministic Evidence

```text
T1 → T2
```

### Phase 2: Skill Contract and Interface

```text
T3 → T4
```

### Phase 3: Workspace Routing

```text
T5 → T6
```

Six tasks fit one TLC execution batch. Do not dispatch implementation workers. Fresh agents are used
only for T3 forward-testing and the mandatory final Verifier.

## Task Breakdown

### T1: Define the continuity policy reference

**What**: Create the single detailed policy reference for evidence, classifications, WIP, states,
delivery contracts, reconciliation and promotion guards.
**Where**: `.agents/skills/advance-delivery-front/references/continuity-policy.md`
**Depends on**: None
**Reuses**: Approved `spec.md`, `design.md`, AD-022 and the evidence vocabulary from
`.agents/skills/triage-project-cycle/SKILL.md`
**Requirements**: DFC-05..22

**Tools**:

- MCP: NONE
- Skill: `skill-creator`

**Done when**:

- [x] A table of contents is present because the reference exceeds 100 lines.
- [x] Classification precedence distinguishes `blocked`, `dependent`, `conflicting` and
  `independent` without turning code overlap into a formal dependency.
- [x] WIP ≤ 2 and stack depth ≤ 1 are explicit invariants.
- [x] All delivery states and invalid transitions from the spec are represented.
- [x] Independent and dependent contract templates contain every field in DFC-12.
- [x] Squash, stale-base, abandoned-base and task-only promotion rules cover DFC-14..22.
- [x] Mutating actions are described only as future approval boundaries, never executable steps.
- [x] Quick gate passes with zero errors.

**Tests**: none — reference/documentation layer; consumed by T3 forward-tests
**Gate**: Quick
**Commit**: `feat(skill): define delivery continuity policy`

### T2: Implement and test the read-only Git front inspector

**What**: Implement the Git snapshot CLI and its co-located functional test harness as one executable
component.
**Where**: `.agents/skills/advance-delivery-front/scripts/inspect-git-front.sh` and
`.agents/skills/advance-delivery-front/scripts/test-inspect-git-front.sh`
**Depends on**: T1
**Reuses**: Strict-mode, argument validation, temporary fixture and immutability patterns from
`.agents/skills/create-review-bundle/scripts/`
**Requirements**: DFC-02, DFC-04, DFC-11..12, DFC-15..16, DFC-20..22

**Tools**:

- MCP: NONE
- Skill: `skill-creator`

**Done when**:

- [x] CLI implements exactly the approved arguments and exit behavior.
- [x] Output is schema-versioned, stable, tab-separated and quotes all dynamic Git values safely.
- [x] It captures resolved SHAs, merge base, dirty paths, linked worktrees, changed paths and optional
  boundary-only commits without printing file contents or credential-bearing remote/config values.
- [x] It contains none of the forbidden Git commands/effects from the design.
- [x] Ten named TAP-style assertions cover independent refs, dirty/deleted/untracked/space paths,
  linked worktrees, boundary-only commits, deterministic timestamp, invalid repo, missing integration
  ref, missing work ref, missing boundary and success/failure immutability.
- [x] Tests compare source status, refs, config and tracked-tree fingerprints before/after.
- [x] Full gate passes with exactly 10 assertions and no silent deletion.

**Tests**: integration
**Gate**: Full
**Commit**: `feat(skill): add read-only git front inspector`

### T3: Implement and forward-test the skill orchestrator

**What**: Replace the initialized placeholder with the concise workflow that gathers sources,
consumes the policy and inspector, and emits the approved report contract.
**Where**: `.agents/skills/advance-delivery-front/SKILL.md`
**Depends on**: T2
**Reuses**: `continuity-policy.md`, `inspect-git-front.sh`, `triage-project-cycle`, product
task-context skills, AD-022 and `skill-creator` writing rules
**Requirements**: DFC-01..22

**Tools**:

- MCP: NONE for implementation and synthetic tests
- Skill: `skill-creator`
- Validation: fresh collaboration agent with raw fixtures

**Done when**:

- [x] Frontmatter contains only `name` and a trigger-complete `description` under 1024 characters.
- [x] Body is imperative, under 500 lines, and links directly to the policy reference at the exact
  point where detailed classification/reconciliation rules are required.
- [x] Workflow gathers Linear, GitHub, local Git and inherited rules read-only, timestamps each source
  and blocks affected transitions on unavailable or stale evidence.
- [x] It preserves the ownership boundary: triage compares waves, continuity owns active topology,
  product context prepares one issue and TLC executes one issue.
- [x] Every result follows the seven-section report contract and recommends exactly one next action.
- [x] No instruction creates or modifies branches, worktrees, PRs, Linear issues or remote state.
- [x] The five raw fixture groups exercise every DFC-01..22 outcome in a fresh-agent forward-test;
  expected safe/blocked transitions are evidenced from the spec rather than leaked in prompts.
- [x] Build and Verification gates pass: five fixture results, 22 mapped AC outcomes, zero unsafe
  mutations and no silent test omission.

**Tests**: forward-test
**Gate**: Build + Verification
**Commit**: `feat(skill): orchestrate continuous delivery fronts`

### T4: Generate the skill interface metadata

**What**: Generate the approved UI metadata from the final `SKILL.md` using the skill-creator helper.
**Where**: `.agents/skills/advance-delivery-front/agents/openai.yaml`
**Depends on**: T3
**Reuses**: Approved interface values from `design.md` and
`skill-creator/references/openai_yaml.md`
**Requirement**: DFC-01

**Tools**:

- MCP: NONE
- Skill: `skill-creator`

**Done when**:

- [x] `display_name`, `short_description` and `default_prompt` are generated deterministically and
  exactly match the approved design.
- [x] `default_prompt` explicitly contains `$advance-delivery-front`.
- [x] No icons, colors or fixed MCP dependencies are introduced.
- [x] Build gate passes with zero errors.

**Tests**: none — interface metadata/configuration layer
**Gate**: Build
**Commit**: `feat(skill): add delivery front interface metadata`

### T5: Register the continuity route in the workspace README

**What**: Add the new skill to the inventory and intention-routing table, documenting its handoff
without copying the policy.
**Where**: `README.md`
**Depends on**: T4
**Reuses**: Existing skill inventory and routing sections
**Requirements**: DFC-01, DFC-13

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] Skill inventory describes active PR/task continuity in one concise row.
- [x] Routing distinguishes cycle comparison, active delivery-front coordination, task preparation
  and TLC execution.
- [x] Handoff states that the new skill is read-only and returns one next action/contract.
- [x] Quick gate passes with zero errors.

**Tests**: none — workspace documentation layer
**Gate**: Quick
**Commit**: `docs: register delivery front continuity route`

### T6: Add the skill routing rule to workspace instructions

**What**: Add a concise mandatory routing instruction and read-only boundary for the new skill.
**Where**: `AGENTS.md`
**Depends on**: T5
**Reuses**: Existing Skills and Security sections
**Requirements**: DFC-01, DFC-13

**Tools**:

- MCP: NONE
- Skill: NONE

**Done when**:

- [x] The Skills section routes continuity requests involving pending PRs to
  `advance-delivery-front`.
- [x] The instruction keeps triage, task-context and TLC responsibilities distinct.
- [x] The Security section preserves the no-mutation boundary for Linear, GitHub and product repos.
- [x] Build gate passes with exactly 10 inspector assertions and zero validation errors.
- [x] The mandatory final TLC Verifier runs after this task and writes `validation.md` with per-AC
  evidence, forward-test results and discrimination-sensor verdict.

**Tests**: none — workspace instructions layer
**Gate**: Build, then automatic final Verification
**Commit**: `docs: route pending-pr continuity through skill`

## Phase Execution Map

```text
Phase 1 → Phase 2 → Phase 3

Phase 1: T1 ──→ T2
Phase 2: T3 ──→ T4
Phase 3: T5 ──→ T6
```

Execution is strictly sequential. Each arrow is the only direct dependency of its target; phase
boundaries preserve the same chain.

## Requirement Traceability

| Requirements | Primary tasks | Verification surface |
| --- | --- | --- |
| DFC-01..04 | T2, T3, T4 | Git integration tests + forward fixtures 1 and 4 |
| DFC-05..09 | T1, T3 | Forward fixtures 1 and 4 |
| DFC-10..13 | T1, T2, T3, T5, T6 | Git integration tests + forward fixtures 1 and 2 |
| DFC-14..19 | T1, T2, T3 | Git integration tests + forward fixtures 2 and 3 |
| DFC-20..22 | T1, T2, T3 | Git integration tests + forward fixture 5 |

All 22 requirements have an implementation owner and an outcome-level verification surface.

## Task Granularity Check

| Task | Scope | Status |
| --- | --- | --- |
| T1 | One policy reference | ✅ Granular |
| T2 | One executable CLI component plus its required co-located tests | ✅ Granular |
| T3 | One skill orchestrator file plus its required behavioral tests | ✅ Granular |
| T4 | One generated metadata file | ✅ Granular |
| T5 | One README routing change | ✅ Granular |
| T6 | One workspace-instruction routing change | ✅ Granular |

## Diagram-Definition Cross-Check

| Task | Depends On (task body) | Diagram Shows | Status |
| --- | --- | --- | --- |
| T1 | None | No incoming arrow | ✅ Match |
| T2 | T1 | T1 → T2 | ✅ Match |
| T3 | T2 | T2 → T3 across phase boundary | ✅ Match |
| T4 | T3 | T3 → T4 | ✅ Match |
| T5 | T4 | T4 → T5 across phase boundary | ✅ Match |
| T6 | T5 | T5 → T6 | ✅ Match |

## Test Co-location Validation

| Task | Code Layer Created/Modified | Matrix Requires | Task Says | Status |
| --- | --- | --- | --- | --- |
| T1 | Policy/reference documentation | none | none | ✅ OK |
| T2 | Git inspector CLI | integration | integration, co-located harness | ✅ OK |
| T3 | Agent workflow | forward-test | forward-test in same task | ✅ OK |
| T4 | Skill interface metadata | none | none | ✅ OK |
| T5 | Workspace routing documentation | none | none | ✅ OK |
| T6 | Workspace instructions | none | none | ✅ OK |

## Tool Assignment Approval

Proposed execution assignment:

- Local filesystem, Git, Bash, Python and ShellCheck for all applicable tasks.
- `skill-creator` for T1–T4; `tlc-spec-driven` for the full Execute phase.
- Fresh collaboration agent only for T3 forward-tests and the mandatory final Verifier.
- No MCP calls during implementation or synthetic validation.
- Available future read surfaces for real skill use include Linear MCP, APEX read-only task/PR
  status tools and local `gh`; their write-capable operations remain forbidden in this MVP.
- Relevant available skills: `triage-project-cycle`, `portal-task-context`,
  `assistants-task-context`, `discover-project-context`, `create-review-bundle`,
  `tlc-spec-driven`, and `skill-creator`.

The user approved these tasks and this tool assignment before Execute on 2026-07-22.

## Execution Results

| Task | Commit | Gate result | Status |
| --- | --- | --- | --- |
| T1 | `0b2fdfe` | Quick: diff and policy contract clean | Complete |
| T2 | `1648eee` | Full: 10/10 initial integration assertions, ShellCheck and diff clean | Complete |
| T3 | `89cf20f` | Build + forward-test: skill valid, 10/10 inspector tests, five fixture groups covering DFC-01..22 | Complete |
| T4 | `b8cb6cd` | Build: generated metadata exact, skill valid, 10/10 tests and ShellCheck clean | Complete |
| T5 | `9d8d013` | Quick: README route and diff clean | Complete |
| T6 | `8dde283` | Build: skill valid, 10/10 tests, ShellCheck and AGENTS route clean | Complete |
| Verification fix | `757a3c1` | Full: 12/12 assertions; boundary/range mutants killed; ShellCheck and diff clean | Complete |

Implementation and verification are complete. The independent TLC Verifier persisted a PASS report
with DFC-01..22 at 22/22, five of five fresh-agent forward-tests, all Build gates green and three of
three targeted behavior mutants killed.

## Task Approval Record

Approved by the user on 2026-07-22 together with the proposed tool assignment. This authorizes the
planning baseline commit and execution of T1–T6 with one atomic commit per task, including synthetic
fresh-agent forward-tests and the mandatory final Verifier. It does not authorize product-repo
changes, live Linear/GitHub mutations, branch creation, rebase, push or PR operations.
