# Pull Request Review Contract

Use this contract to make reviews reproducible, actionable, and measurable without overstating the
available evidence.

## Evidence identity

Record:

- repository and PR number;
- observation timestamp;
- PR author, state, and draft status;
- base ref and base SHA;
- head ref and head SHA;
- target Linear issue, its observed `updatedAt`, and DoD source, or `not identified`;
- Linear retrieval scope: `target-only`, `expanded`, `reused`, or `unavailable`, including every
  additional issue identifier and why it was needed;
- remote checks observed for that head;
- local validation command and exact Git object, or why local validation was not bound to the head.

The comparison is the PR's GitHub base/head surface. A local branch name, review bundle, previous
approval, or green check from another SHA does not substitute for this identity.

## Severity

- `P0`: immediate catastrophic or broadly destructive impact; stop delivery.
- `P1`: high-impact correctness, security, data-loss, or availability defect that should block.
- `P2`: concrete defect affecting a meaningful scenario; normally fix before merge.
- `P3`: bounded correctness or maintainability defect with low immediate impact.

Choose severity from user and system impact, likelihood, and blast radius—not fix effort. Keep
non-blocking improvements outside the finding list.

Unresolved `P0` or `P1` findings require `block`. Unresolved `P2` findings also require `block`
unless a durable requirement or accepted-risk decision has already classified the concern as
`accepted-by-contract`. A review with only unresolved `P3` findings may use `non-blocking findings`.

## Finding format

Use one entry per independent defect:

```text
[P1] Imperative, specific title

Evidence: path and line, diff hunk, failing check, or reproducible observation
Impact: concrete incorrect behavior and affected actor/data
Condition: input, state, sequence, or environment required to trigger it
Suggested direction: optional; describe the constraint, not a mandatory personal design
Reviewed head: full SHA
```

A finding is valid only when the changed code introduces or exposes the behavior and the impact is
plausible under the stated condition. Put unresolved requirement ambiguity under `Open questions`.

## Review result

Return sections in this order:

1. `Findings` — ordered P0 to P3; if empty, say `No actionable findings.`
2. `Verdict` — `block`, `non-blocking findings`, `no actionable findings`, or `inconclusive`.
3. `Reviewed surface` — PR, base SHA, head SHA, observation time, issue/DoD, and Linear retrieval
   scope with expansion reasons.
4. `Validation` — GitHub checks, local commands, and results, each bound to a SHA.
5. `Open questions and residual risk` — unverified behavior, missing access, absent tests, or accepted
   scope risks. Absence of findings is not proof that no defect exists.

If the base or head changed during review, replace the verdict with `stale` until the changed
surface is reviewed.

## Finding outcome states

Classify outcomes only from observable evidence:

- `accepted-fixed`: a later reviewed head changes the relevant behavior and verification confirms it.
- `accepted-by-contract`: the owner resolves the concern through an explicit, durable requirement or
  accepted-risk decision and the resulting implementation matches it.
- `rejected-with-evidence`: counter-evidence demonstrates that the reported behavior or impact is not
  a defect.
- `withdrawn-false-positive`: the reviewer explicitly withdraws the finding after counter-evidence or
  reproduction disproves it.
- `unresolved`: the finding remains applicable on the current head.
- `indeterminate`: a thread state, approval, merge, or missing history does not reveal the outcome.

Thread resolution, outdated position, a later approval, or a corrective-looking commit is supporting
evidence, not sufficient alone. Inspect the changed behavior before assigning a decided state.

## Post-merge outcomes

Record the merge SHA/date and observation cutoff. Use:

- `confirmed-escape`: a later corrective PR/commit/issue or reproduced regression is attributable to
  behavior introduced by the reviewed surface;
- `no-confirmed-escape`: no attributable correction was found within the stated window;
- `not-observed`: the merge or a meaningful observation window is unavailable.

Never report `no-confirmed-escape` as proven zero escaped defects.

## Pilot metrics

Aggregate only comparable, evidence-backed states:

- reviewed PRs and repositories;
- PRs with persisted review threads versus approvals without threads;
- findings by severity;
- decided findings (`accepted-fixed`, `accepted-by-contract`, `rejected-with-evidence`,
  `withdrawn-false-positive`);
- acceptance rate = accepted decided findings / all decided findings;
- false-positive rate = withdrawn false positives / all decided findings;
- unresolved and indeterminate findings, reported separately;
- confirmed escapes and the explicit observation window;
- reviews made stale by a head change;
- Linear issue reads per review, target-only versus expanded reviews, and expansion reasons;
- remote checks and head-bound local validations observed.

Do not calculate acceptance or false-positive percentages when the decided denominator is zero. Do
not use approval count, thread resolution, or absence of later commits as a proxy for review quality.
Do not reward fewer Linear reads by itself: the goal is to remove repeated or irrelevant traversal
without omitting inherited requirements that can change the verdict.

## Sanitized pilot record

Append one closed-schema JSON record through `scripts/pr-review-pilot.py`; never write the ledger by
hand. The schema permits identity SHAs, timestamps, enum states, issue identifiers, expansion reason
enums, check states, and finding IDs/severity/outcome only. It intentionally has no field for review
prose, comments, diffs, code, credentials, customer data, production output, or transcripts. Store
the resulting JSONL only below ignored `session-context/review-pilot/`; it is local, ephemeral,
non-canonical, and eligible for deletion after the pilot decision is closed.

Use this exact shape; values remain subject to the helper's enums and validation:

```json
{
  "schema_version": 1,
  "repository": "inventeer/portal-api",
  "pr": 280,
  "observed_at": "2026-08-07T12:00:00Z",
  "base_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "head_sha": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "final_base_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "final_head_sha": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "verdict": "no-actionable-findings",
  "github_review_evidence": "threads",
  "linear": {
    "target_issue": "INV-3145",
    "target_updated_at": "2026-08-07T10:00:00Z",
    "scope": "target-only",
    "reads": 1,
    "expansions": []
  },
  "checks": {"remote": "passed", "local": "unbound"},
  "findings": [],
  "post_merge": {"status": "not-observed", "cutoff": null}
}
```
