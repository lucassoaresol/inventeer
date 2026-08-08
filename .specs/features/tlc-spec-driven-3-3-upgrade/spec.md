# TLC Spec-Driven 3.3.0 Upgrade Specification

**Status:** Approved
**Review language:** Portuguese
**Canonical language:** English for skill and feature artifacts; Portuguese for workspace decisions

## Problem Statement

The vendored `tlc-spec-driven` skill is based on upstream 3.2.0 and contains deliberate Inventeer
workflow extensions. Upstream 3.3.0 adds deterministic validators for specifications, task plans,
commit messages, and validation state, but its untested parsers do not fully recognize artifact
formats already produced by this workspace. A blind replacement could lose local workflow behavior;
a retroactive validation sweep could also fail historical artifacts that predate the new contract.

The workspace needs a reproducible three-way upgrade that preserves its local extensions, hardens
the new validators against representative artifacts, and adopts the gates prospectively.

## Goals

- Upgrade the pinned upstream base from 3.2.0 to 3.3.0 without losing local TLC behavior.
- Make the four new deterministic validators reliable for newly created artifacts.
- Add behavioral regression coverage to the root workspace gate.
- Keep historical artifacts readable without requiring retroactive rewrites.
- Record exact upstream provenance, local policy, and validation evidence.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Rewriting historical `.specs/` artifacts | They were valid under the workflow version active when produced. |
| Removing Inventeer-specific TLC extensions | AD-016 explicitly maintains the local fork. |
| Publishing changes to the upstream repository | This workspace only consumes and hardens the vendored dependency. |
| Changing product repositories or `session-context/` | The upgrade is limited to the workspace workflow. |
| Making APEX executable in Codex | Executor routing remains governed by AD-026. |

## Assumptions & Open Questions

| Assumption or question | Resolution | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Upstream identity | Use commit `fe318be656b315d5b6f45cf7ea23946b2d0241b0`, version 3.3.0 | A fixed commit makes the merge reproducible. | Yes |
| Merge policy | Reapply local changes from base `6663279cd659b60cecb3e8d2dcc13162c88a8b7a` | This is the AD-016 three-way model. | Yes |
| Validator adoption | Apply validators to artifacts created or materially revised under 3.3.0 | Legacy documents did not promise the new schema. | Yes |
| Verification independence | Use a standalone fresh-eyes pass and disposable mutation sensor | The user explicitly prohibited subagents. | Yes |
| Remaining open questions | None | Scope and compatibility policy are explicit. | Yes |

**Open questions:** none

## User Stories

### P1: Reproducible Vendor Upgrade

**Acceptance Criteria**:

1. **TLC330-01** — WHEN the upgrade is applied THEN the workspace SHALL pin upstream version 3.3.0
   and commit `fe318be656b315d5b6f45cf7ea23946b2d0241b0` in its vendor manifest.
2. **TLC330-02** — WHEN upstream content is merged THEN all intentional base-to-local workflow
   extensions SHALL remain present unless an explicit replacement is documented.
3. **TLC330-03** — WHEN the vendored version is displayed THEN README and manifest metadata SHALL
   agree with the skill metadata.

### P1: Deterministic Gate Compatibility

**Acceptance Criteria**:

4. **TLC330-04** — WHEN a canonical acceptance-criteria heading uses Markdown emphasis with the
   colon inside or outside the emphasis THEN `validate_spec.py` SHALL recognize it.
5. **TLC330-05** — WHEN validation contains an explicit overall PASS or FAIL plus subordinate sensor
   results THEN `validate_state.py` SHALL use the overall verdict and SHALL NOT let a subordinate
   PASS mask an overall FAIL.
6. **TLC330-06** — WHEN a completed validation claims PASS without `file:line` evidence THEN the
   state validator SHALL fail closed.
7. **TLC330-07** — WHEN task dependencies and Mermaid edges disagree THEN `validate_tasks.py` SHALL
   reject the plan; matching plans SHALL pass.
8. **TLC330-08** — WHEN a commit message violates or satisfies the supported Conventional Commit
   contract THEN `check_commit.py` SHALL return the corresponding deterministic result.

### P1: Prospective Adoption and Regression Protection

**Acceptance Criteria**:

9. **TLC330-09** — WHEN the root workspace gate runs THEN it SHALL execute behavioral tests for all
   four deterministic TLC validators.
10. **TLC330-10** — WHEN the 3.3.0 validators are adopted THEN the root gate SHALL NOT sweep and
    retroactively reject historical feature artifacts.
11. **TLC330-11** — WHEN a new or materially revised TLC artifact uses the 3.3.0 workflow THEN the
    applicable validator SHALL be run explicitly before its transition is treated as complete.
12. **TLC330-12** — WHEN validator behavior is independently challenged in disposable copies THEN
    representative weakened or regressed mutations SHALL be detected by the test suite.

## Edge Cases

- A validation document mentions both PASS and FAIL in narrative or sensor sections: only the
  explicit overall verdict controls completion.
- An acceptance-criteria heading is `**Acceptance Criteria:**` or `**Acceptance Criteria**:`: both
  forms are valid.
- A historical spec lacks 3.3.0-only sections: it remains historical evidence and is not rewritten.
- Upstream adds files that have no local counterpart: they are imported unchanged before local
  hardening is applied.
- A local extension touches the same file as upstream: the final diff must be reviewed against both
  the old upstream base and the new pinned commit.

## Requirement Traceability

| Requirement ID | Component | Provenance | Status |
| --- | --- | --- | --- |
| TLC330-01 | Vendor manifest | Upstream 3.3.0 and AD-016 | Verified |
| TLC330-02 | Skill tree | Upstream 3.3.0 and AD-016 | Verified |
| TLC330-03 | README and metadata | Upstream 3.3.0 and AD-016 | Pending |
| TLC330-04 | Spec validator and fixtures | Upstream 3.3.0 plus local compatibility review | Verified |
| TLC330-05 | State validator and fixtures | Upstream 3.3.0 plus local compatibility review | Verified |
| TLC330-06 | State validator and fixtures | Upstream 3.3.0 plus local compatibility review | Verified |
| TLC330-07 | Task validator and fixtures | Upstream 3.3.0 plus local compatibility review | Verified |
| TLC330-08 | Commit validator and fixtures | Upstream 3.3.0 plus local compatibility review | Verified |
| TLC330-09 | Root workspace gate | Workspace safety requirements and user instruction | Verified |
| TLC330-10 | Prospective adoption policy | Workspace safety requirements and user instruction | Pending |
| TLC330-11 | Transition gate policy | Workspace safety requirements and user instruction | Pending |
| TLC330-12 | Standalone discrimination sensor | Workspace safety requirements and user instruction | Pending |

## Success Criteria

- The final skill reports 3.3.0 and retains every reviewed Inventeer extension.
- Representative valid artifacts pass and malformed or misleading artifacts fail.
- The complete root gate passes from the delivered commit.
- A disposable mutation sensor proves that the new regression tests discriminate key failures.
