# Engine-Aware Skill Learning Validation

**Date**: 2026-07-28
**Spec**: `.specs/features/engine-aware-skill-learning/spec.md`
**Diff range**: `24ed3cd..4c3b208`
**Verifier**: standalone fresh-eyes fallback; no sub-agent used at the user's request

## Delivery Evidence

- **Validation state**: `pass`
- **Evidence binding**: `24ed3cd8e064777a675ef9c01a31b3971cb3a510..4c3b208b05bd923812bf0f998253a10b14eda4a9`
- **Requirement contract**: spec blob `a1e173381252e153286e6249ec195ca94370f9da`
- **Gate state**: green; 24/24 checks, ShellCheck and range-scoped diff integrity passed
- **Pending delivery conditions**: none; this report and the Handoff are evidence-only changes outside the validated implementation range
- **High-risk paths**: generated `apex-*` wrappers and engine-routing instructions
- **Independence limitation**: author/verifier separation was unavailable because sub-agents were explicitly avoided after repeated session communication failures

## Task Completion

| Task | Status | Evidence |
| --- | --- | --- |
| Decisions and retrospective contract | ✅ Done | `4e6c942` |
| Operational documentation | ✅ Done | `b5e1791` |
| Generated-wrapper enforcement | ✅ Done | `ef61dd7` |
| Shell lint correction | ✅ Done | `fd15cb1` |
| Validation coverage correction | ✅ Done | `4c3b208` |

## Spec-Anchored Acceptance Criteria

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --- | --- | --- | --- |
| ESL-01 — Evidência multi-engine | Both local histories are named; continuations/copies are distinguished; the current retrospective is excluded | `scripts/test-engine-routing.sh:71-84` — `grep -Fq "$path" ...`, `grep -q 'sessões principais, continuations e cópias' ...`, `grep -q 'retrospectiva é excluída do recorte' ...` | ✅ PASS |
| ESL-02 — Capacidade versus execução | Resource access is not represented as supported execution without invocation, session context, artifacts and gates | `scripts/test-engine-routing.sh:37-46` — `grep -q 'não criam uma execução APEX suportada' ...`, `grep -q 'invocação, contexto de' ...`, `grep -q 'sessão, artifacts e gates completos' ...` | ✅ PASS |
| ESL-03 — Roteamento atual | Codex uses TLC; eligible Claude repos use APEX; context skills still prepare the task | `scripts/test-engine-routing.sh:20-34` — AD-025 supersession/AD-026 active checks plus exact route and preparation assertions | ✅ PASS |
| ESL-04 — Wrappers honestos | Every generated wrapper declares the diagnostic boundary and routes Codex delivery to TLC | `scripts/test-engine-routing.sh:49-63` — loop asserts `não use como executor de entrega` and `Use \`tlc-spec-driven\` como executor`; `scripts/test-sync-apex-commands.sh:79-84` asserts generated output | ✅ PASS |
| ESL-05 — Destino dos aprendizados | Decisions, validated execution lessons and product findings have distinct canonical destinations; raw transcripts remain untracked | `scripts/test-engine-routing.sh:87-104` — destination assertions plus `git ls-files '*.jsonl'` rejection | ✅ PASS |
| ESL-06 — Consistência | Active decisions, AGENTS, README and all wrappers express the same engine-aware route | `scripts/test-engine-routing.sh:20-68` — active-decision, dual-document and all-wrapper conjunction | ✅ PASS |

**Status**: ✅ 6/6 acceptance criteria match their spec-defined outcomes.

## Discrimination Sensor

All mutations ran in disposable archives under `/tmp`; the source worktree was never mutated.

| Mutation | Target | Fault | Result |
| --- | --- | --- | --- |
| M1 | `scripts/sync-apex-commands.sh:161` | Removed `não use como executor de entrega` from generated wrapper metadata | ✅ Killed by `test-sync-apex-commands.sh`: `wrapper claims or implies supported APEX execution` |
| M2 | `AGENTS.md:61` | Changed “does not create supported execution” into “creates supported execution” | ✅ Killed by `test-engine-routing.sh`: `AGENTS.md conflates APEX resource access with supported execution` |
| M3 | `README.md:167` | Changed exclusion of the current retrospective into inclusion | ✅ Killed by `test-engine-routing.sh`: `README.md does not exclude the current retrospective` |

**Sensor depth**: lightweight, three targeted policy mutations  
**Result**: 3/3 killed — PASS ✅

## Gate Check

- **Build gate**: `shellcheck scripts/sync-apex-commands.sh scripts/test-engine-routing.sh scripts/test-sync-apex-commands.sh && ./scripts/test-engine-routing.sh && ./scripts/test-sync-apex-commands.sh`
- **Diff-integrity gate**: `git diff --check 24ed3cd..4c3b208`
- **Result**: 24 passed, 0 failed, 0 skipped; ShellCheck and diff integrity exited 0
- **Test count before feature**: 14
- **Test count after feature**: 24
- **Delta**: +10 checks

## Code Quality

| Principle | Status |
| --- | --- |
| Minimum and surgical changes | ✅ |
| No scope creep or unrelated product writes | ✅ |
| Generated wrappers remain derived from one generator | ✅ |
| Tests map to all six acceptance criteria | ✅ |
| Assertions target exact policy outcomes | ✅ |
| Workspace guidance followed | ✅ `AGENTS.md` and AD-026/AD-027 |

## Validation Iteration

The first fresh-eyes pass found that the routing test checked the headline routes but did not
discriminate every required clause of ESL-01, ESL-02 and ESL-05. Commit `4c3b208` added exact
assertions for current-retrospective exclusion, supported-execution prerequisites, context-skill
preparation and canonical learning destinations. The complete gate and sensor then passed.

## Requirement Traceability

| Requirement | Status |
| --- | --- |
| ESL-01 | ✅ Verified |
| ESL-02 | ✅ Verified |
| ESL-03 | ✅ Verified |
| ESL-04 | ✅ Verified |
| ESL-05 | ✅ Verified |
| ESL-06 | ✅ Verified |

## Summary

**Overall**: ✅ Ready

The workspace now records multi-engine retrospective evidence without versioning transcripts,
routes Codex delivery to TLC and eligible Claude delivery to APEX, and keeps every Codex APEX
wrapper explicitly diagnostic. Automated checks and three targeted mutations discriminate these
boundaries. The only process limitation is the intentionally accepted standalone verification
mode, used to preserve session continuity without sub-agents.
