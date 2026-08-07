# PR Review Pilot Hardening Specification

**Status:** Delivered and verified on 2026-08-07 (`46ebfd9`)
**Review language:** Portuguese
**Canonical language:** English for skill and script contracts

## Problem Statement

The pull-request review pilot defines evidence identity and prospective metrics, but it cannot yet
persist sanitized review outcomes, revalidates only the head SHA, and has only static wording tests.
Workspace validation is also spread across independent commands.

## Scope

- Keep review execution read-only for GitHub, Linear, product repositories, branches, and worktrees.
- Store pilot observations only under ignored `session-context/review-pilot/`.
- Persist structured metadata only; never persist comments, diffs, finding prose, credentials,
  customer data, production output, or transcript bodies.
- Do not materialize PR heads locally in this increment; measure that limitation during the pilot.

## Acceptance Criteria

1. **PRH-01** — WHEN the final observed base SHA or head SHA differs from the reviewed identity,
   THEN the review verdict SHALL be `stale` until the changed surface is reviewed.
2. **PRH-02** — WHEN a review has unresolved P0 or P1 findings, THEN its verdict SHALL be `block`;
   unresolved P2 findings SHALL block unless an explicit durable accepted-risk contract classifies
   them as `accepted-by-contract`; P3-only findings MAY be non-blocking.
3. **PRH-03** — WHEN a pilot record is appended, THEN a deterministic helper SHALL validate a
   closed schema and write one canonical JSON line below `session-context/review-pilot/`.
4. **PRH-04** — WHEN an input contains an unknown field, malformed SHA, arbitrary finding text,
   path escape, credential-like field, or inconsistent stale verdict, THEN recording SHALL fail
   without changing the ledger.
5. **PRH-05** — WHEN the ledger is summarized, THEN comparable outcome counts and rates SHALL follow
   the review contract and zero denominators SHALL produce `null`, not a fabricated percentage.
6. **PRH-06** — WHEN Linear evidence is reused across workflow boundaries, THEN the supplied
   snapshot SHALL carry retrieval time and `updatedAt`; any changed bound input or decision-relevant
   event SHALL require a refresh, without claiming freshness from elapsed time alone.
7. **PRH-07** — WHEN workspace validation runs, THEN one command SHALL execute every maintained
   workspace harness, skill structural validation, Python compilation, shell syntax, Markdown-link
   validation, and diff-integrity check without reducing coverage.
8. **PRH-08** — WHEN GitHub MCP authentication is documented, THEN a dedicated least-privilege
   fine-grained token SHALL be the default and reuse of `gh auth token` SHALL be labeled a fallback
   whose scopes must be inspected first.

## Success Criteria

- Behavioral tests reject stale-base, unsafe-schema, and false-rate calculations.
- The unified workspace gate passes on the complete root workspace.
- A disposable-copy discrimination sensor kills faults in stale detection and schema rejection.
- No product repository, GitHub object, Linear issue, branch, or worktree is modified.

## Requirement Traceability

| Requirement | Evidence owner | Status |
| --- | --- | --- |
| PRH-01 | Review skill plus stale base/head behavior tests | Verified |
| PRH-02 | Review contract plus unresolved severity behavior test | Verified |
| PRH-03 | Sanitized ledger helper plus append/canonicalization test | Verified |
| PRH-04 | Closed-schema and path-boundary behavior tests | Verified |
| PRH-05 | Outcome, evidence-source, check, Linear, and zero-denominator summary tests | Verified |
| PRH-06 | Timestamped Linear snapshot contract and workflow test | Verified |
| PRH-07 | Unified workspace gate and structural validation | Verified |
| PRH-08 | Least-privilege token documentation and MCP contract test | Verified |

**Coverage:** 8/8 requirements verified and delivered in the attributable functional commit
`46ebfd9`.
