# LESSONS — auto-maintained by scripts/lessons.py

> Machine-owned. Do NOT hand-edit. Changes are overwritten on the next `lessons.py` write.
> Canonical state lives in `.specs/lessons.json`. Edit lessons only via the script.
> promote_threshold=2 distinct features · window_days=45 · quarantine_threshold=2

## Confirmed (load these at Specify/Design)

Corroborated across multiple features. Safe to apply as guidance.

_none_

## Candidates (under observation — do NOT load as guidance yet)

Seen once or not yet corroborated. Tracked, not trusted.

### L-001 — Test invalid-but-resolvable Git refs, not only missing refs, when guards depend on ancestry.
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `git-inspector` · harmful: 0
- features: delivery-front-continuity
- evidence: validation.md:M1 (git-inspector)
- last seen: 2026-07-22T20:39:26Z

### L-002 — Test Git range semantics on diverged histories so two-dot and three-dot behavior cannot pass the same fixture.
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `git-inspector` · harmful: 0
- features: delivery-front-continuity
- evidence: validation.md:M2 (git-inspector)
- last seen: 2026-07-22T20:39:26Z

### L-003 — Run final diff integrity checks against the complete feature evidence range, not only the working tree.
- signal: `gate_fail` · recurrence: 1 feature(s) · scope: `workflow` · harmful: 0
- features: review-evidence-lifecycle
- evidence: .specs/features/review-evidence-lifecycle/validation.md:F1 (workflow)
- last seen: 2026-07-24T14:00:43Z

### L-004 — Bind adjacent checksum entries to the exact artifact basename and digest before treating evidence as verified.
- signal: `ac_gap` · recurrence: 1 feature(s) · scope: `review-bundle` · harmful: 0
- features: review-evidence-lifecycle
- evidence: validation.md:F1 REL-12/REL-14 (review-bundle)
- last seen: 2026-07-24T14:36:08Z

### L-005 — Assert every workspace policy clause explicitly, including exclusions and canonical destinations.
- signal: `ac_gap` · recurrence: 1 feature(s) · scope: `workspace-policy-tests` · harmful: 0
- features: engine-aware-skill-learning
- evidence: .specs/features/engine-aware-skill-learning/validation.md:76 (workspace-policy-tests)
- last seen: 2026-07-28T05:27:56Z

### L-006 — Run a staged or equivalent diff-integrity check for new files before committing
- signal: `gate_fail` · recurrence: 1 feature(s) · scope: `workspace-delivery` · harmful: 0
- features: workspace-mcp-resource-preflight
- evidence: .specs/features/workspace-mcp-resource-preflight/validation.md:63-67 (workspace-delivery)
- last seen: 2026-07-29T00:45:42Z

### L-007 — Resolve MCP working directories from the engine operational workspace root and prove the configured target exists before publication
- signal: `review_finding` · recurrence: 1 feature(s) · scope: `mcp` · harmful: 0
- features: workspace-mcp-resource-preflight-cwd-correction
- evidence: .specs/features/workspace-mcp-resource-preflight/validation.md:Runtime Finding (mcp)
- last seen: 2026-07-29T01:10:51Z

### L-008 — In workspace contract tests, assert every named authority surface and declared lifecycle edge case, not only the primary path
- signal: `ac_gap` · recurrence: 1 feature(s) · scope: `workspace-contract-tests` · harmful: 0
- features: portal-tlc-session-artifacts
- evidence: .specs/features/portal-tlc-session-artifacts/validation.md:49 (workspace-contract-tests)
- last seen: 2026-07-31T06:11:36Z

## Quarantined (failed when applied — ignore)

A confirmed lesson that recurred alongside failure. Kept for the maintainer to review.

_none_
