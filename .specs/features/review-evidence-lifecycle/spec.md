# Review Evidence Lifecycle Specification

**Status:** Approved
**Review language:** Portuguese
**Canonical language:** English for skill content; Portuguese for workspace decisions

## Problem Statement

Repeated review bundles showed that implementation, validation, correction, commit, publication, and
promotion are distinct states. The current delivery-front contract tracks PR topology well but does
not bind validation evidence to the exact head and diff that were reviewed, while review bundles do
not describe their relationship to earlier generations.

The workspace needs a small, explicit evidence lifecycle across `advance-delivery-front`,
`create-review-bundle`, and the local TLC fork. The change must preserve their ownership boundaries:
delivery coordination consumes evidence, bundles package it, and TLC produces validation evidence.

## Goals

- Make stale or incomplete review evidence impossible to present as promotion-ready.
- Make successive review bundles traceable without making them canonical artifacts.
- Improve TLC specification, tasking, validation isolation, resource-aware gates, and learning from
  confirmed external review findings.
- Preserve read-only behavior for product repositories during inspection and bundling.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Mutating GitHub, Linear, branches, or product files from `advance-delivery-front` | AD-022 keeps the MVP read-only. |
| Treating a ZIP bundle as approval or freshness proof | Bundles remain historical `CODE` evidence. |
| Automatically importing arbitrary historical ZIP formats | Lineage applies to bundles produced by the current script contract. |
| Building a generic review database | The workspace needs portable evidence, not another source of truth. |
| Changing product repositories | This feature changes only the workspace and its skills. |

## Assumptions and Decisions

| Decision | Chosen behavior | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Evidence model | Track implementation and validation maturity separately | A clean test run does not prove commit/push/PR readiness. | Yes |
| Validation binding | Bind PASS to exact work SHA and review surface; change makes it stale | Prevent reuse after corrective edits. | Yes |
| Bundle lineage | Optional parent bundle plus required review-stage label when a parent is supplied | First bundles remain simple; later generations become comparable. | Yes |
| Scope surface | Support exact paths, path families, expected renames, generated artifacts, and forbidden local artifacts | Large mechanical refactors cannot be judged by file count alone. | Yes |
| Inspector evolution | Emit schema v2 with commits, rename-aware entries, and split working-tree paths | Deterministic evidence belongs in the script. | Yes |
| TLC external findings | Accept only confirmed findings grounded in validation evidence | Preserve evidence-or-zero and avoid turning opinions into lessons. | Yes |

**Open questions:** none.

## P1: Evidence-Aware Delivery Front

1. **REL-01** — WHEN a front is assessed THEN the contract SHALL report implementation maturity as
   `working-tree`, `committed`, `pushed`, or `pr-observed` and validation maturity as `missing`,
   `pass`, `fail`, `stale`, or `pending-delivery`.
2. **REL-02** — WHEN work SHA, working-tree diff, requirement contract, or applicable gate changes
   after validation THEN prior validation SHALL become `stale` for promotion.
3. **REL-03** — WHEN validation is `pass` but delivery-only criteria remain THEN the front SHALL be
   `pending-delivery`, not `reviewable`.
4. **REL-04** — WHEN review changes update a ready PR or a dependent base PR THEN affected boundaries,
   task-only surfaces, gates, and validation SHALL be reassessed before promotion.
5. **REL-05** — WHEN a delivery contract defines scope THEN it SHALL distinguish exact paths, path
   families, expected renames, allowed generated artifacts, and forbidden local artifacts.
6. **REL-06** — WHEN many files change through an expected mechanical rename THEN file count alone
   SHALL NOT classify the work as scope creep.

## P1: Deterministic Git Evidence

7. **REL-07** — WHEN the inspector runs THEN schema v2 SHALL emit commits in the review range.
8. **REL-08** — WHEN the review range contains renames or copies THEN the inspector SHALL emit
   rename-aware status entries in addition to final changed paths.
9. **REL-09** — WHEN the worktree is dirty THEN staged, unstaged, and untracked paths SHALL be emitted
   separately without changing the repository.
10. **REL-10** — WHEN the same refs, worktree, and timestamp are inspected twice THEN output SHALL be
    byte-identical.

## P1: Review Bundle Lineage

11. **REL-11** — WHEN a bundle is created without a parent THEN it SHALL record its review stage and
    an explicit absence of parent lineage.
12. **REL-12** — WHEN a parent bundle is supplied THEN the child SHALL record the parent basename,
    computed SHA-256, adjacent-checksum verification status, parent head SHA, and current head SHA.
13. **REL-13** — WHEN parent and child file manifests are available THEN lineage SHALL classify each
    path as `added`, `removed`, or `retained`.
14. **REL-14** — WHEN a parent is invalid, has no unique `files.tsv`, or its adjacent checksum fails
    THEN bundle creation SHALL fail without modifying the source repository or leaving a child ZIP.
15. **REL-15** — WHEN a lineage-enabled bundle is created THEN it SHALL remain review evidence only
    and SHALL NOT claim freshness, validation, or approval.

## P1: TLC Workflow Corrections

16. **REL-16** — WHEN Specify covers a contract-bearing change THEN compatibility and representation
    SHALL consider wire format, persistence, migration/backfill, rollout compatibility, exact
    encoding, and safe public disclosure.
17. **REL-17** — WHEN Tasks decomposes a broad mechanical refactor THEN atomicity SHALL mean one
    reversible semantic invariant, not an arbitrary one-file limit.
18. **REL-18** — WHEN full gates may exceed available resources THEN tasks SHALL record an equivalent
    resource-aware recipe such as deterministic sharding without weakening coverage.
19. **REL-19** — WHEN discrimination mutations run THEN only disposable worktrees or copies SHALL be
    allowed; stash-based mutation of the real worktree SHALL be forbidden.
20. **REL-20** — WHEN validation closes THEN it SHALL expose a compact delivery evidence block with
    verdict, exact diff range/head, gate state, pending delivery conditions, and high-risk paths.
21. **REL-21** — WHEN an external review finding is reproduced or otherwise confirmed and recorded in
    validation THEN the lessons tool SHALL accept it as a grounded `review_finding` signal.

## Edge Cases

- A validation report exists only as an uncommitted artifact: validation may pass, but implementation
  remains `working-tree` and promotion is blocked.
- A child bundle points to a valid ZIP whose adjacent checksum is missing: compute and record the
  parent SHA, mark verification `missing`, and continue.
- A parent checksum exists but is invalid: fail closed.
- A rename spans a diverged integration/work history: retain three-dot review semantics and report
  rename status from that same surface.
- A full suite OOMs but deterministic shards cover the complete suite: record the shard recipe and
  aggregate totals instead of weakening the gate.

## Requirement Traceability

| Requirements | Component | Provenance | Status |
| --- | --- | --- | --- |
| REL-01..06 | Delivery policy and skill | User-approved retrospective | In Tasks |
| REL-07..10 | Git inspector and harness | User-approved retrospective | In Tasks |
| REL-11..15 | Bundle skill, script, and harness | User-approved retrospective | In Tasks |
| REL-16..21 | TLC fork references, script, and tests | User-approved retrospective | In Tasks |

## Success Criteria

- A changed head cannot reuse a prior PASS for promotion.
- A validation PASS with uncommitted or pending delivery work is not called reviewable.
- Inspector tests discriminate two-dot/three-dot, ancestry, rename, and working-tree maturity.
- A second bundle proves its parent and path delta without changing the source repo.
- TLC validation and lessons behavior enforce the new workflow rules.

