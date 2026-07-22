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

## Quarantined (failed when applied — ignore)

A confirmed lesson that recurred alongside failure. Kept for the maintainer to review.

_none_
