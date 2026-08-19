# Retrospective Evidence Freshness Validation

**Overall**: PASS
**Contract status**: PASS
**Operational status**: PASS
**Date**: 2026-08-18
**Spec**: `.specs/features/retrospective-evidence-freshness/spec.md`
**Diff range**: `79643d9..653de07`
**Verifier**: standalone fresh-eyes fallback; no subagent per explicit user request

---

## Delivery Evidence

- **Validation state**: `pass`
- **Evidence binding**: base `79643d9`, behavioral head `52a24be`, corrective head/work SHA
  `653de07cc9900154543aae73b58e77a4d0de9fb0`
- **Requirement contract**: approved spec at `52a24be`, re-read at `653de07`
- **Gate state**: green; root evidence gate and complete-range diff-integrity gate returned zero
- **Pending delivery conditions**: none; the final evidence commit is limited to spec, index,
  validation and Handoff closure
- **High-risk paths**: `scripts/audit-session-history.py`, `scripts/workspace-handoff.py`,
  `.specs/STATE.md` and the two behavioral fixtures

## Task Completion

No `tasks.md` exists. The approved medium feature was delivered as one integrated capability in
`52a24be`; `653de07` closes the decision-index omission found by the terminal gate.

| Delivery commit | Status | Notes |
| --- | --- | --- |
| `52a24be` | PASS | Auditor v3, portable receipt, Handoff freshness, dual verdicts and behavioral tests |
| `653de07` | PASS | Adds AD-046 to the deterministic decision index |

## Spec-Anchored Acceptance Criteria

| Requirement | Spec-defined outcome | `file:line` + assertion expression | Result |
| --- | --- | --- | --- |
| REF-01 | Contract v3 and no `primary_sessions` | `scripts/test-session-history-audit.py:326` — `assert set(report) == {...}`; `:337` — `assert report["contract_version"] == 3` | PASS |
| REF-02 | Exact Codex physical, continuation and logical counts | `scripts/test-session-history-audit.py:344` — `assert report["codex"] == {... "session_instances": 3, "continuations": 1, ... "logical_work_streams": 2 ...}` | PASS |
| REF-03 | Exact Claude physical, sidechain and logical counts | `scripts/test-session-history-audit.py:368` — `assert report["claude"] == {... "session_instances": 7, "sidechains": 1, ... "logical_sessions": 7 ...}` | PASS |
| REF-04 | Requested, matched and unmatched exclusions are separate | `scripts/test-session-history-audit.py:340` — `assert report["exclusions_requested"] == 3`; `:341` — `assert report["exclusions_matched"] == 2`; `:342` — `assert report["exclusions_unmatched"] == 1` | PASS |
| REF-05 | Out-of-cohort exclusion stays unmatched without changing cohort | `scripts/test-session-history-audit.py:342` — `assert report["exclusions_unmatched"] == 1`; `:344` and `:368` assert the complete unchanged engine cohorts | PASS |
| REF-06 | Receipt binds normalized provenance, auditor and report checksum | `scripts/test-session-history-audit.py:537` — `assert set(receipt) == {...}`; `:550` — `assert receipt["normalized_arguments"] == {...}`; `:560` — `assert receipt["report_sha256"] == hashlib.sha256(canonical_report).hexdigest()` | PASS |
| REF-07 | Portable root and no physical paths or session IDs | `scripts/test-session-history-audit.py:529` — `assert portable_cwd not in receipt_output.stdout`; `:531` — `assert PRIMARY not in receipt_output.stdout`; `:548` — `assert receipt["workspace_root"] == "<workspace-root>"` | PASS |
| REF-08 | Equivalent cohorts under different roots produce identical receipts | `scripts/test-session-history-audit.py:535` — `assert portable_receipts[0] == portable_receipts[1]` | PASS |
| REF-09 | Handoff records timestamp, SHA, publication and invalidation | `scripts/test-workspace-handoff.py:111` — `for expected in (...)`; `:119` — `assert expected in rendered` | PASS |
| REF-10 | Only Handoff is replaced | `scripts/test-workspace-handoff.py:110` — `assert rendered.split("## Handoff", 1)[0] == original.decode("utf-8").split("## Handoff", 1)[0]` | PASS |
| REF-11 | Behavioral descendants invalidate; evidence-only descendants remain fresh | `scripts/test-workspace-handoff.py:138` — `assert fresh_descendant.returncode == 0`; `:161` — `assert sha_changed.returncode == 1`; `:162` — `assert json.loads(sha_changed.stdout)["reason"] == "sha-changed"` | PASS |
| REF-12 | Publication drift returns stale/publication-changed | `scripts/test-workspace-handoff.py:144` — `assert publication_changed.returncode == 1`; `:145` — `assert json.loads(publication_changed.stdout) == {"schema": 1, "state": "stale", "reason": "publication-changed"}` | PASS |
| REF-13 | Transient external action is rejected before bytes change | `scripts/test-workspace-handoff.py:130` — `assert rejected.returncode == 2`; `:131` — `assert "transient external action" in rejected.stderr`; `:132` — `assert state.read_bytes() == before_rejection` | PASS |
| REF-14 | Missing, symlinked, malformed or outside-root state fails closed | `scripts/test-workspace-handoff.py:184` — `assert missing_status.returncode == 2`; `:195` — `assert linked_status.returncode == 2`; `:212` — `assert malformed_write.returncode == 2`; `:223` — `assert state.read_bytes() == root_before` | PASS |
| REF-15 | Workflow validation declares contract and operational axes | `scripts/test-workspace-handoff.py:229` — `assert "**Contract status**: PASS" in unified_validation`; `:230` — `assert "**Operational status**: UNPROVEN" in unified_validation` | PASS |
| REF-16 | Missing pilot is explicit and cannot be hidden by one PASS | `scripts/test-workspace-handoff.py:231` — `assert "**Missing operational evidence**:" in unified_validation`; `:232` — `assert "**Overall**: PASS" not in unified_validation` | PASS |
| REF-17 | Historical backfill changes checksum and preserves bounds/outcomes | `scripts/test-session-history-audit.py:587` — `assert backfilled_receipt["report_sha256"] != receipt["report_sha256"]`; `:588`-`:591` assert identical bounds and explicit exclusion fields | PASS |
| REF-18 | Shared cross-engine ID is globally deduplicated with engine decomposition | `scripts/test-session-history-audit.py:341` — `assert report["exclusions_matched"] == 2`; `:343` — `assert report["exclusions_by_engine"] == {"codex": 2, "claude": 1}` | PASS |
| REF-19 | Invalid window or workspace identity fails before receipt | `scripts/test-session-history-audit.py:606` — `assert invalid_workspace.returncode != 0`; `:630` — `assert reversed_window.returncode != 0` | PASS |
| REF-20 | Missing upstream is indeterminate, never fresh | `scripts/test-workspace-handoff.py:170` — `assert indeterminate.returncode == 2`; `:171` — `assert json.loads(indeterminate.stdout) == {"schema": 1, "state": "indeterminate", "reason": "upstream-unavailable"}` | PASS |

**Status**: 20/20 requirements match precise spec outcomes; 0 spec-precision gaps.

## Edge Cases

| Edge case | Evidence | Result |
| --- | --- | --- |
| Historical retrospective enters an already closed window | `scripts/test-session-history-audit.py:563` adds the backfill; `:587`-`:591` assert changed checksum with stable bounds and explicit exclusion outcomes | PASS |
| One ID exists in both engine histories | `scripts/test-session-history-audit.py:341` and `:343` assert union total 2 and engine counts 2/1 | PASS |
| Invalid time range or empty logical workspace | `scripts/test-session-history-audit.py:593`-`:631` assert both processes fail closed | PASS |
| Upstream cannot be resolved | `scripts/test-workspace-handoff.py:165`-`:175` assert `indeterminate/upstream-unavailable` | PASS |

## Gate Check

- **Resource preflight**: 12 CPUs, load `0.49/0.39/0.34`, 1,538,994,176 bytes available memory,
  1,042,272,256 bytes free swap and 981,132,472,320 bytes available filesystem; sequential gate
- **Gate command**: `python3 scripts/workspace-gate-evidence.py run --profile workspace`
- **Gate result**: exit 0, `{"profile":"workspace","result":"passed","schema":1}` at `653de07`
- **Diff-integrity command**: `git diff --check 79643d9..653de07`
- **Diff-integrity result**: exit 0, no output
- **Root suites**: 25 passed, 0 failed, 0 skipped; 24 before the feature, +1 Handoff suite
- **Feature fixtures**: 20 auditor scenarios + 12 Handoff/document scenarios passed
- **Test integrity**: no prior test removed, skipped or weakened

## Discrimination Sensor

Mutations ran in three separate copies from `git archive 653de07` under one `mktemp` directory.
The scratch was removed; real-tree porcelain before and after remained exactly the two preexisting
lesson files.

| Mutation | Scratch file:line | Behavior-level fault | Result |
| --- | --- | --- | --- |
| M1 | `scripts/audit-session-history.py:21` | Changed contract version 3 to 2 | KILLED at `scripts/test-session-history-audit.py:337` |
| M2 | `scripts/audit-session-history.py:574` | Summed per-engine exclusion matches instead of unioning shared IDs | KILLED at `scripts/test-session-history-audit.py:341` |
| M3 | `scripts/workspace-handoff.py:344` | Inverted publication equality so a matching state became stale | KILLED at `scripts/test-workspace-handoff.py:122` |

**Sensor depth**: lightweight, three high-risk semantic branches.
**Result**: 3/3 killed, 0 survived — PASS.

## Code Quality

| Principle | Status | Evidence |
| --- | --- | --- |
| Minimum code and no speculative flexibility | PASS | One auditor mode and one root-only Handoff helper implement the approved contract |
| Surgical scope | PASS | Root scripts, tests, instructions and TLC/workspace artifacts only; no `repos/` change |
| Existing patterns | PASS | Atomic replacement follows the checkpoint helper; aggregate gate adds one suite |
| Spec-anchored tests | PASS | 20/20 mapping above uses exact values and structured states |
| Necessary tests only | PASS | Every added assertion maps to REF-01..REF-20 or one listed edge case |
| Project guidelines | PASS | `AGENTS.md` and `.agents/skills/tlc-spec-driven/references/coding-principles.md` followed |
| Lessons ownership | PASS | Preexisting `.specs/LESSONS.md` and `.specs/lessons.json` changes were preserved and excluded from commits |

## Requirement Traceability Update

| Requirements | Previous status | New status |
| --- | --- | --- |
| REF-01..REF-20 | Implemented | Verified |

## Summary

**Overall**: PASS

The auditor now emits an unambiguous portable v3 receipt, the versioned Handoff proves behavioral
and publication freshness without SHA self-reference, and workflow validation separates contract
from operation. The root gate, real sanitized receipt, final Handoff query and discrimination sensor
provide operational evidence for this workspace capability. The separate Portal dual-engine pilot
remains explicitly `UNPROVEN` in its own validation report.
