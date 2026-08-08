# Workspace Session Resilience v2 Pilot

**Status:** active
**Started at (UTC):** 2026-08-08T05:44:16Z
**Baseline auditor contract:** 2
**Baseline window:** `[2026-07-10T00:00:00Z, 2026-08-08T05:44:16Z)`
**Excluded sessions:** 1
**Progress:** 0/10 eligible primary sessions

## Evidence Boundary

The baseline was generated from exact workspace origins with an exclusive upper bound and an
explicit exclusion count. This artifact contains aggregates only. It does not contain session
identity, transcript locations or content, commands, tool names, credentials, customer data, or
production output.

## Baseline

| Metric | Value |
| --- | ---: |
| Codex history root available | yes |
| Codex files | 157 |
| Primary sessions | 107 |
| Continuations | 37 |
| Logical work streams | 70 |
| Subagents | 46 |
| Copies | 4 |
| Total aborted turns | 197 |
| Sessions with aborts | 67 (62.62%) |
| Maximum aborts in one primary session | 6 |
| Total compactions | 49 |
| Sessions with compactions | 38 (35.51%) |
| Maximum compactions in one primary session | 4 |
| Codex sessions with successful APEX outcomes | 21 |
| Codex sessions with attempted APEX operations | 24 |
| Claude history root available | yes |
| Claude files | 15 |
| Claude primary sessions | 15 |
| Claude sidechains | 0 |
| Claude copies | 0 |
| Claude sessions with successful APEX outcomes | 6 |
| Claude sessions with attempted APEX operations | 6 |

## Reproducibility Contract

The auditor selects origins in `[since, until)` and emits the contract version, normalized limits,
and exclusion count. Sessions originating at or after the pilot start do not change the baseline.

Local history roots remain mutable. If an import or restoration adds history inside the closed
window, changed aggregates are classified as source drift, not as a new pilot session.

## Eligible Evidence

A session counts when it:

- is a new primary Codex or Claude session originating from the exact workspace root after the
  pilot start;
- performs material planning, implementation, validation, review, or workflow maintenance;
- is not the retrospective performing the measurement;
- is not a copy, continuation, sidechain, or subagent;
- is classified by the sanitized auditor before transcript interpretation.

The pilot closes after ten eligible primary sessions or the next long workspace feature, whichever
happens first.

## Success Measures

| Measure | Target |
| --- | ---: |
| Verified work lost after an interruption | 0 |
| Heavy stages started without a resource preflight | 0 |
| Heavy stages started from a stale checkpoint | 0 |
| Status requests attributable to silent long-running work | 0 |
| Resumptions requiring more than one Git, Handoff, and tasks reconciliation | 0 |
| Potential secrets repeated or persisted by an agent | 0 |

Abort and compaction rates are diagnostic, not success targets, because the platform can cause them.
Process resilience is measured by lost work, stale state, silence, and reconstruction cost.

## Automation Decision Gate

A proposal for additional checkpoint or restricted gate-runner automation is eligible only if the
pilot observes at least one of these thresholds:

- two heavy gates started without a resource preflight;
- two status requests caused by silent long-running work;
- one stale checkpoint after an interruption; or
- recurring manual reconstruction of a command, gate, shard, or next task.

The pilot does not authorize implementing that automation.

## Closing Review

At the observation boundary:

1. Run the auditor with an explicit contract, closed time window, and current-session exclusion.
2. Compare primary interruption concentration with the baseline and classify any source drift.
3. Measure lost work, stale checkpoints, silence, and manual reconstruction.
4. Apply the Automation Decision Gate.
5. Record the outcome in the workspace decision log before changing the workflow.
