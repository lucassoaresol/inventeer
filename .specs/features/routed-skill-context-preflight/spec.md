# Routed Skill Context Preflight Specification

**Status:** Validated
**Review language:** Portuguese
**Canonical language:** English

## Problem Statement

AGENTS.md requires running `workspace-context.py check` and `plan --route <route>` before loading a
registered context route, but a sanitized session audit found the preflight in 2 of 27 Claude
sessions and 14 of 119 Codex files, while the routed skills themselves ran far more often. The rule
lives in ambient instructions that an engine reads once per session, whereas the skill body is read
at the moment the work starts. `discover-project-context` already declares the preflight as its
first workflow step; the other five routed skills do not, and nothing detects the difference.

## Goals

- [x] Make every routed skill declare its own preflight as the first workflow step.
- [x] Bind each declaration to that skill's own route, so a copied step cannot plan the wrong one.
- [x] Detect a missing or mismatched declaration deterministically.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Making the preflight executable by the harness | The engines run skill steps, not hooks; a declared step is the enforceable unit here. |
| Adding routes for `create-review-bundle` or `tlc-spec-driven` | Neither is a registered context route; inventing one would enlarge the manifest without a consumer. |
| Changing route budgets or the manifest schema | The routes already pass; this feature changes when the preflight is invoked, not what it measures. |
| Rewriting the workflow bodies of the five skills | Only the first step is added and the remainder renumbered. |
| Removing the AGENTS.md policy | The policy remains; only its operational trigger moves into the skills. |

---

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Wording of the new step | Copied from `discover-project-context` | The repo already established the pattern under AD-051; a second phrasing would create drift between skills. | y |
| Placement | First step of `## Workflow` | The preflight bounds context before any source is read; any later position defeats it. | y |
| Renumbering | Subsequent steps shift by one | No skill cross-references a step number, so renumbering is safe. | y |
| Enforcement location | `scripts/test-workspace-context.py` | That suite already owns the route manifest contract; the declaration is part of it. | y |
| `create-review-bundle` and `tlc-spec-driven` | Unchanged | Neither is referenced by a route, so neither has a preflight to declare. | y |

**Open questions:** none - all resolved or logged above.

---

## User Stories

### P1: Declare the preflight inside each routed skill ⭐ MVP

**User Story**: As the workspace maintainer, I want each routed skill to carry its own preflight
step, so the bound is applied when the work starts rather than depending on an ambient rule.

**Why P1**: The ambient rule reached 7% of Claude sessions; the skill body is read every time the
skill runs.

**Acceptance Criteria**:

1. The system SHALL declare, as the first `## Workflow` step of every skill referenced by a context
   route, both `python3 scripts/workspace-context.py check` and
   `python3 scripts/workspace-context.py plan --route <route>`.  <!-- ubiquitous -->
2. WHERE a skill declares the preflight THEN the `--route` value SHALL be the route whose manifest
   references that same skill.  <!-- optional-feature -->
3. The declared step SHALL instruct stopping on a non-zero result.  <!-- ubiquitous -->
4. The declared step SHALL state that the commands emit metadata only and do not replace reading the
   selected sources.  <!-- ubiquitous -->
5. WHEN the preflight step is inserted THEN the remaining workflow steps SHALL keep their original
   order and text, renumbered by one.  <!-- event-driven -->
6. The system SHALL NOT add a preflight step to a skill that no route references.  <!-- ubiquitous -->

**Independent Test**: Every routed skill's first workflow step names both commands and its own
route; `create-review-bundle` names neither.

---

### P1: Detect a missing or mismatched declaration ⭐ MVP

**User Story**: As the workspace maintainer, I want the gate to fail when a routed skill loses its
preflight or points at the wrong route, so the fix cannot silently regress.

**Why P1**: The original defect was undetectable, which is why it persisted.

**Acceptance Criteria**:

1. IF a skill referenced by a route omits either preflight command THEN the suite SHALL fail naming
   that skill.  <!-- unwanted-behavior -->
2. IF a routed skill declares `--route` with a route other than its own THEN the suite SHALL fail
   naming both routes.  <!-- unwanted-behavior -->
3. IF the preflight appears in the skill but not as the first workflow step THEN the suite SHALL
   fail.  <!-- unwanted-behavior -->
4. The suite SHALL derive the routed-skill set from the manifest rather than a hardcoded list.  <!-- ubiquitous -->

**Independent Test**: Removing the step, swapping the route, or demoting it to second position each
fails the suite.

---

### P2: Keep the instructions pointing at the operative location

**User Story**: As the workspace maintainer, I want AGENTS.md to state that the preflight is a
declared step of each routed skill, so the instruction and the skills do not drift.

**Why P2**: The policy is still correct; only its trigger moved.

**Acceptance Criteria**:

1. The workspace instructions SHALL state that each routed skill declares the preflight as its
   first step.  <!-- ubiquitous -->
2. The workspace instructions SHALL keep the exit semantics for the check and plan commands.  <!-- ubiquitous -->

**Independent Test**: The clause names the skills as the point of invocation and retains exit `1`
and exit `2` semantics.

---

## Edge Cases

- IF a route references a vendored skill THEN the suite SHALL NOT require a preflight declaration in
  it, because vendored content is replaced on update.
- WHEN a route is added to the manifest without a preflight in its skill THEN the suite SHALL fail,
  so the manifest and the skills cannot diverge.
- IF a skill declares the preflight commands inside a later section rather than the first workflow
  step THEN the suite SHALL fail.
- WHEN a skill's workflow uses bold step titles THEN the inserted step SHALL follow that skill's own
  formatting rather than imposing a foreign style.

---

## Requirement Traceability

| Requirement ID | Story | Provenance | Evidence | Phase | Status |
| --- | --- | --- | --- | --- | --- |
| RCP-01 | P1: Declare | ISSUE | Audit: preflight in 2 of 27 Claude sessions | Tasks | Pending |
| RCP-02 | P1: Declare | INHERITED | AD-048 requires routes to bound context before loading | Tasks | Pending |
| RCP-03 | P1: Declare | DECISION | Wording copied from the established `discover-project-context` pattern | Tasks | Pending |
| RCP-04 | P1: Declare | SAFETY | A copied step pointing at the wrong route would plan the wrong budget | Tasks | Pending |
| RCP-05 | P1: Detect | ISSUE | The original defect was undetectable | Tasks | Pending |
| RCP-06 | P1: Detect | SAFETY | The routed set must follow the manifest, not a hardcoded list | Tasks | Pending |
| RCP-07 | P2: Instructions | INHERITED | AGENTS.md is the workspace instruction source | Tasks | Pending |

**Coverage:** 7 total, 7 mapped to tasks, 0 unmapped

---

## Success Criteria

- [ ] All six routed skills declare their own preflight as the first workflow step.
- [ ] Removing, misrouting, or demoting the step fails the suite.
- [ ] `create-review-bundle` and `tlc-spec-driven` remain untouched.
- [ ] AGENTS.md names the skills as the point of invocation.
- [ ] `scripts/workspace-gate-evidence.py run --profile workspace` passes.
