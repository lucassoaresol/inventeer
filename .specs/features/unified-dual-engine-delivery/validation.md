# Unified Dual-Engine Delivery Validation

**Overall**: PASS ✅
**Date**: 2026-08-17
**Spec**: `.specs/features/unified-dual-engine-delivery/spec.md`
**Diff range**: `bb07515..805165c`
**Verifier**: independent sub-agent (author != verifier)

---

## Delivery Evidence

- **Validation state**: `pass`
- **Evidence binding**: base `bb07515`, head/work SHA `805165c5f0e49ab1c0eea65e6fc9bb559f21a347`; commits `27a32b6`, `bea29b0`, `bd861c6`, and corrective commit `805165c`
- **Requirement contract**: `.specs/features/unified-dual-engine-delivery/spec.md` at `805165c`
- **Gate state**: green; root gate and complete-range diff-integrity gate returned zero
- **Pending delivery conditions**: none
- **High-risk paths**: `AGENTS.md`, `.agents/skills/portal-task-context/SKILL.md`, `.specs/STATE.md`, and the three feature contract test scripts; all received targeted review and mutation coverage

---

## Task Completion

No `tasks.md` exists in the feature directory. Validation was bound directly to the approved
specification and supplied commit range.

| Delivery commit | Status | Notes |
| --- | --- | --- |
| `27a32b6` | ✅ Present | Unified executor and APEX boundary |
| `bea29b0` | ✅ Present | Shared Portal continuation contract |
| `bd861c6` | ✅ Present | Workspace index and handoff updates |
| `805165c` | ✅ Present | Removed the range-gate whitespace defect without changing behavior |

---

## Spec-Anchored Acceptance Criteria

| Criterion | Spec-defined outcome | `file:line` + shell assertion expression | Result |
| --- | --- | --- | --- |
| Executor AC1: either engine specifies, implements, or validates work | TLC is the executor after the applicable context skill in both engines | `scripts/test-engine-routing.sh:32` — ``grep -Fq 'Use sempre `tlc-spec-driven` como executor' AGENTS.md``; `scripts/test-engine-routing.sh:34` — `grep -q 'no Codex e' AGENTS.md`; `scripts/test-engine-routing.sh:36` — `grep -q 'no Claude Code' AGENTS.md`; `scripts/test-engine-routing.sh:38` — `grep -q 'A preparação continua sendo das skills locais de' AGENTS.md` | ✅ PASS — all expressions returned zero and assert `AGENTS.md:94` |
| Executor AC2: either engine discovers an APEX surface | APEX remains diagnostic/experimental and is not supported delivery execution | `scripts/test-engine-routing.sh:42` — `grep -q 'não criam uma execução APEX suportada' AGENTS.md`; `scripts/test-engine-routing.sh:50` — `grep -q 'APEX permanece disponível para inspeção e diagnóstico' README.md`; `scripts/test-engine-routing.sh:58` — each wrapper must match `grep -q 'não use como executor de entrega'`; `scripts/test-engine-routing.sh:67` — `rg -q 'lê e executa\|Siga integralmente o workflow retornado' .agents/skills/apex-*` must be false; `scripts/test-engine-routing.sh:75` — `grep -q 'No Claude Code, trate também os workflows nativos' AGENTS.md` | ✅ PASS — positive assertions returned zero, the forbidden claim was absent, and the exact boundary is at `AGENTS.md:84` |
| Executor AC3: a future APEX pilot satisfies AD-034 | Changing executor still requires a new transversal decision | `scripts/test-engine-routing.sh:52` — `grep -q 'Uma chamada bem-sucedida isolada também não conclui um workflow' README.md`; `scripts/test-portal-tlc-session-artifacts.sh:88` — `grep -q 'APEX permanece diagnóstico até uma nova decisão' AGENTS.md`; `scripts/test-portal-tlc-session-artifacts.sh:90` — `grep -q 'futura adoção de APEX exige nova decisão' README.md` | ✅ PASS — all expressions returned zero and assert `README.md:317` |
| Portal AC1: either engine creates file-backed TLC artifacts | Store them under `session-context/portal/<INV-ID>/tlc/` | `scripts/test-portal-tlc-session-artifacts.sh:20` — `contract_path='session-context/portal/<INV-ID>/tlc/'`; `scripts/test-portal-tlc-session-artifacts.sh:30` — every engine-facing contract surface must satisfy `grep -Fq "$contract_path" "$file"`; `scripts/test-portal-tlc-session-artifacts.sh:36` and `:38` require both engines | ✅ PASS — all expressions returned zero and assert `AGENTS.md:98` |
| Portal AC2: either engine creates a review bundle | Group it under `session-context/portal/<INV-ID>/review/` | `scripts/test-portal-tlc-session-artifacts.sh:77` — `grep -Fq 'session-context/portal/<INV-ID>/review/' README.md` | ✅ PASS — expression returned zero and asserts `AGENTS.md:101` |
| Portal AC3: either engine completes a stable TLC transition | Run the checkpoint helper only after success; include all six declared events and both engines | `scripts/test-tlc-checkpoint-contract.sh:29` — collect the checkpoint contract; `scripts/test-tlc-checkpoint-contract.sh:30` — every `gate commit bundle PR validation pre-heavy` trigger must match; `scripts/test-tlc-checkpoint-contract.sh:34` — `grep -q 'somente depois.*sucesso'`; `scripts/test-tlc-checkpoint-contract.sh:36` — `grep -q 'Não avance.*falh'`; `scripts/test-tlc-checkpoint-contract.sh:44` and `:46` require both engines; `scripts/test-tlc-checkpoint-contract.sh:50` requires the helper path | ✅ PASS — all expressions returned zero and assert `AGENTS.md:107` |
| Portal AC4: resume on a machine without prior local state | Reconstruct from canonical sources or consume an explicitly transferred sanitized package | `scripts/test-portal-tlc-session-artifacts.sh:81` — `grep -q 'não sincroniza artifacts' README.md`; `scripts/test-portal-tlc-session-artifacts.sh:83` — `grep -q 'On another machine, reconstruct state from canonical sources' .agents/skills/portal-task-context/SKILL.md` | ✅ PASS — both expressions returned zero and assert `.agents/skills/portal-task-context/SKILL.md:67` |
| Portal AC5: local Portal task state is documented | It is ignored, local, ephemeral, non-canonical, non-durable, and not automatically portable | `scripts/test-portal-tlc-session-artifacts.sh:44` and `:46` require the local and ephemeral/non-canonical/non-durable classifications; `scripts/test-portal-tlc-session-artifacts.sh:101` requires `git ls-files 'session-context/**'` to be empty; `scripts/test-tlc-checkpoint-contract.sh:66` checks each lifecycle property; `scripts/test-tlc-checkpoint-contract.sh:95` requires no tracked session state; `scripts/test-tlc-checkpoint-contract.sh:97` runs `git check-ignore -q session-context/portal/INV-3145/tlc/STATE.md` | ✅ PASS — every expression returned the required outcome and asserts `AGENTS.md:100` |
| Portal AC6: issue is merged and closed | The issue-local directory becomes eligible for cleanup | `scripts/test-portal-tlc-session-artifacts.sh:79` — `grep -q 'merge.*encerr' README.md`; `scripts/test-tlc-checkpoint-contract.sh:70` — `grep -q 'merge.*issue encerrada' <<<"$checkpoint_docs"` | ✅ PASS — both expressions returned zero and assert `AGENTS.md:102` |

**Status**: ✅ 9/9 ACs have exact `file:line` evidence and assertions matching the spec-defined outcome; 0 spec-precision gaps.

---

## Edge Cases

| Edge case | Evidence and assertion | Result |
| --- | --- | --- |
| Same-machine Codex → Claude switch reuses the issue path after reconciliation | `scripts/test-portal-tlc-session-artifacts.sh:30` asserts one `contract_path` across engine-facing surfaces; `scripts/test-tlc-checkpoint-contract.sh:40` asserts `preflight de recursos.*reconciliação do estado atual` before `pre-heavy` | ✅ PASS |
| Another machine uses the convention without assuming local files | `scripts/test-portal-tlc-session-artifacts.sh:81` asserts no automatic artifact sync; `scripts/test-portal-tlc-session-artifacts.sh:83` asserts canonical reconstruction | ✅ PASS |
| An isolated successful APEX call stays diagnostic | `scripts/test-engine-routing.sh:52` asserts isolated success does not complete a workflow; `scripts/test-engine-routing.sh:50` asserts diagnostic availability | ✅ PASS |
| Durable product specifications stay canonical | `scripts/test-portal-tlc-session-artifacts.sh:50` rejects canonical/durable/official status for working TLC artifacts; `scripts/test-portal-tlc-session-artifacts.sh:60` asserts all three forbidden product roots; `scripts/test-portal-tlc-session-artifacts.sh:67` asserts the working-spec boundary | ✅ PASS |

---

## Gate Check

- **Resource preflight**: 12 CPUs online, load `0.37/0.32/0.34`, 2,192,175,104 bytes memory available, 26,640,384 bytes swap free, and 982,124,134,400 bytes filesystem available. Execution remained sequential because swap was nearly exhausted.
- **Root evidence command**: `python3 scripts/workspace-gate-evidence.py run --profile workspace`
- **Root evidence result**: exit 0, `{"profile":"workspace","result":"passed","schema":1}`.
- **Canonical build command**: `bash scripts/test-workspace.sh`
- **Build result**: exit 0, 24/24 suites passed, 0 failed, 0 skipped. The feature-specific scripts contribute 28/28 passing assertions: engine routing 9, Portal artifacts 10, and checkpoints 9.
- **Test-count comparison**: base `bb07515` also has 24 root suites. Feature-specific assertions increased from 26 (`9 + 9 + 8`) to 28 (`9 + 10 + 9`); no test was removed or weakened.
- **Diff-integrity command**: `git diff --check bb07515..805165c`
- **Diff-integrity result**: exit 0, no output.
- **Overall gate result**: ✅ green.

---

## Discrimination Sensor

All mutations ran sequentially in separate disposable Git worktrees at `805165c`. No stash was used.

| Mutation | Scratch file:line | Behavior-level fault | Focal command and asserted outcome | Result |
| --- | --- | --- | --- | --- |
| M1 | `AGENTS.md:94` | Changed the shared executor from TLC to APEX | `bash scripts/test-engine-routing.sh` exited 1 with `AGENTS.md does not declare TLC as the shared executor` | ✅ Killed |
| M2 | `.agents/skills/portal-task-context/SKILL.md:67` | Replaced canonical cross-machine reconstruction with an assumption that prior local files exist | `bash scripts/test-portal-tlc-session-artifacts.sh` exited 1 with `portal-task-context does not define cross-machine reconstruction` | ✅ Killed |
| M3 | `AGENTS.md:108` | Moved checkpoint recording from after successful transition to before its result | `bash scripts/test-tlc-checkpoint-contract.sh` exited 1 with `AGENTS.md does not require successful transitions` | ✅ Killed |

**Sensor depth**: lightweight, three mutations across the three highest-risk policy branches.

**Result**: ✅ 3/3 killed, 0 survived.

**Isolation**: real-worktree porcelain before and after the sensor was exactly
`?? .specs/features/unified-dual-engine-delivery/validation.md`. Final `git worktree list --porcelain`
contained only `/home/lucas/inventeer`; no scratch registration remained.

---

## Code Quality

| Principle | Status | Evidence |
| --- | --- | --- |
| No features beyond the approved contract | ✅ | Diff is limited to dual-engine routing, Portal continuation, decision/index updates, and their tests |
| No single-use abstraction or unnecessary flexibility | ✅ | Existing Markdown contracts, shell harnesses, and checkpoint helper were updated in place |
| Surgical changes only | ✅ | Corrective commit `805165c` removes one blank EOF line; no product repo changed |
| Existing style and patterns preserved | ✅ | AD supersession, context-skill handoff, shell `grep` assertions, and aggregate gate patterns are retained |
| Test integrity preserved | ✅ | Root suite count stayed 24; feature assertions rose 26 → 28; no skip, deletion, or weakened assertion |
| Tests map to ACs and edge cases | ✅ | 9/9 ACs and 4/4 edge cases are traced above; all three high-risk branches killed a mutant |
| Spec-defined outcomes are asserted exactly | ✅ | Shared TLC, diagnostic APEX, precise paths, success ordering, reconstruction, authority, and cleanup are literal assertions |
| Per-layer coverage expectation met | ✅ | This is a workspace policy/documentation feature; engine, Portal, and checkpoint contract layers each have a focal harness |
| No unclaimed new tests | ✅ | The two added assertions cover the shared-engine Portal route and shared-engine checkpoints |
| Documented guidelines followed | ✅ | `AGENTS.md:84`, `README.md:261`, and `.agents/skills/tlc-spec-driven/references/coding-principles.md:1` |

---

## Requirement Traceability Assessment

| Requirement | Evidence status | Delivery status |
| --- | --- | --- |
| UDDE-01 | ✅ Verified | ✅ Behavioral PASS |
| UDDE-02 | ✅ Verified | ✅ Behavioral PASS |
| UDDE-03 | ✅ Verified | ✅ Behavioral PASS |
| UDDE-04 | ✅ Verified | ✅ Behavioral PASS |
| UDDE-05 | ✅ Verified | ✅ Behavioral PASS |
| UDDE-06 | ✅ Verified | ✅ Behavioral PASS |

---

## Ranked Gaps

None.

---

## Summary

**Verdict**: PASS ✅

**Spec-anchored check**: 9/9 ACs matched the spec outcome; 0 spec-precision gaps.

**Edge cases**: 4/4 traced to passing assertions.

**Gate**: 24/24 root suites passed; complete-range diff integrity passed.

**Sensor**: 3 mutations injected, 3 killed, 0 survived; real worktree preserved.

**Delivery**: PASS at behavioral head `805165c5f0e49ab1c0eea65e6fc9bb559f21a347`; the report and traceability close in the evidence-only final commit.
