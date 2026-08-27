# Routed Skill Context Preflight Validation

**Verdict:** PASS
**Evidence range:** `dc8da08..HEAD`
**Gate:** `python3 scripts/workspace-gate-evidence.py run --profile workspace` - passed, 29 suites
**Discrimination sensor:** 7 of 7 mutants killed, plus 4 synthetic failure cases inside the detector
**Coverage:** 12 of 12 acceptance criteria, 4 of 4 edge cases

Verification ran as the standalone fresh-eyes pass from the skill's Sub-Agent Delegation section:
the session's operating instructions forbid dispatching an unrequested sub-agent, so the Verifier
role was executed inline against the committed diff surface.

---

## P1: Declare the preflight inside each routed skill

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --- | --- | --- | --- |
| AC1 Both commands as the first workflow step | Step 1 names check and plan | `scripts/test-workspace-context.py:429` - `assert violation is None, violation`, over `preflight_violation` which requires both commands in step 1 | PASS |
| AC2 `--route` matches the manifest route | Route equals the referencing route | `:429` - `preflight_violation` compares `plan --route <route>` against the route derived from the manifest at `:400-415` | PASS |
| AC3 Step instructs stopping on non-zero | Literal `non-zero` present | `:431` - `assert "non-zero" in step` | PASS |
| AC4 Step states the metadata-only bound | Literal `metadata only` present | `:432` - `assert "metadata only" in step` | PASS |
| AC5 Remaining steps keep order, renumbered by one | Sequential 1..N, original text | Verified in execution: all six workflows renumber sequentially (18, 15, 10, 10, 12, 10 steps) with no cross-reference to a step number | PASS |
| AC6 No preflight in an unrouted skill | Absent from the body | `:437` - `assert "workspace-context.py" not in body` for `create-review-bundle` | PASS |

**Independent test:** every routed skill's first step names its own route; the five edited skills
match the `discover-project-context` wording byte for byte apart from the route token.

## P1: Detect a missing or mismatched declaration

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --- | --- | --- | --- |
| AC1 Missing command fails naming the skill | Message contains `omits` | `:454-455` - `assert violation is not None`, `assert expected in violation` for the `comando ausente` case | PASS |
| AC2 Wrong route fails naming both | Message contains `must plan route` | `:454-455` - `rota trocada` case | PASS |
| AC3 Demoted step fails | Non-None violation | `:454-455` - `passo demovido` case | PASS |
| AC4 Routed set derived from the manifest | Not hardcoded | `:400-415` builds `routed_skills` from `MANIFEST`; `:416` - `assert routed_skills, "no routed skills derived from the manifest"` | PASS |

**Independent test:** removing the step, swapping the route, or demoting it each fail the suite
against the real files (sensor Q1, Q2, Q3).

## P2: Keep the instructions pointing at the operative location

| Criterion | Spec-defined outcome | `file:line` + assertion | Result |
| --- | --- | --- | --- |
| AC1 Instructions name the skills as the invocation point | Clause states the declared first step | `AGENTS.md:65-71`; asserted indirectly by `scripts/test-workspace-context.py:367` (`ok 11`) which still finds both commands | PASS |
| AC2 Exit semantics preserved | ``exit `1` `` and ``exit `2` `` retained | `:367` - `for outcome in ("exit \`1\`", "exit \`2\`", "metadata"): assert outcome in agents` | PASS |

---

## Edge Cases

| Edge case | `file:line` + assertion | Result |
| --- | --- | --- |
| A route referencing a vendored skill is exempt | `:410-412` - `if skill in VENDORED: continue`; `tlc-spec-driven` is referenced by `portal-task` and `assistants-task` and carries no preflight | PASS |
| A new route without a preflight fails | `:417` - `assert set(routed_skills) == {...}` pins the routed set; sensor Q5 confirms an empty set fails at `:416` | PASS |
| Preflight present but outside step 1 | `:454` - `passo demovido` case; sensor Q3 against the real file | PASS |
| Bold step titles keep the skill's own formatting | `advance-delivery-front` step 1 reads `**Bound the context.** Run ...`, matching its sibling steps | PASS |

---

## Discrimination Sensor

Mutants were injected into a disposable `git worktree`; the real tree was never modified and the
worktree was removed with `--force` afterwards.

| Mutant | Injected defect | Result |
| --- | --- | --- |
| Q1 | Preflight removed from `review-pull-request` | KILLED |
| Q2 | `triage-project-cycle` plans `portal-task` instead of its own route | KILLED |
| Q3 | `portal-task-context` preflight demoted to step 2 | KILLED |
| Q4 | `create-review-bundle` gains a preflight it has no route for | KILLED |
| Q5 | Every skill treated as vendored, emptying the routed set | KILLED |
| Q6 | Step drops the stop-on-non-zero instruction | KILLED |
| Q7 | Step drops the metadata-only bound | KILLED |

**7 of 7 killed.** The detector additionally exercises four synthetic failure shapes in-process at
`:447-455`, so it cannot pass vacuously if the real files were ever all removed.

---

## Test Integrity

| Suite | Before | After | Delta |
| --- | --- | --- | --- |
| `scripts/test-workspace-context.py` | 11 named cases | 12 named cases | +1, none removed |
| Aggregate `scripts/test-workspace.sh` | 29 suites | 29 suites | unchanged, all passing |

No assertion was weakened and no test was deleted or skipped.

---

## Findings

1. **The pattern already existed and had not been propagated.** `discover-project-context` declared
   the preflight as step 1 under AD-051, and the other five routed skills never received it. The
   defect was not a missing idea but an unenforced one, which is why the detector matters more than
   the five edits.

2. **Two routes reference a vendored skill.** `portal-task` and `assistants-task` both list
   `tlc-spec-driven`. Requiring a preflight there would place workspace-local text inside content
   that `update-vendored-skill.sh` replaces wholesale, so the contract exempts vendored skills and
   the test asserts the exemption rather than leaving it implicit.

3. **The instruction is now policy, not trigger.** AGENTS.md states the rule and the exit semantics
   but points at the skill body as the point of invocation. This is the reason the original rule
   underperformed: an engine reads ambient instructions once per session, and reads the skill body
   at the moment the work begins.
