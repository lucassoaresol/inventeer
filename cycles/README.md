# Cycle Clarification Register

This directory preserves curated task-clarification snapshots by planning cycle. It is durable
workspace memory, not a mirror of Linear and not a product specification store.

## Authority

- Linear remains canonical for current hierarchy, cycle, state, owner, relations, estimates, and
  execution.
- Product documentation remains canonical for product intent and governed contracts.
- Product repositories remain canonical for code, tests, and local technical decisions.
- A cycle record preserves what was clarified for planning at a dated snapshot. Revalidate its facts
  before preparing, implementing, reviewing, or resuming an issue.

## Layout

```text
cycles/<cycle>/<product>/tasks/INV-<id>.md
```

Each task record contains durable conclusions, decisions, scope boundaries, material dependencies,
and canonical source pointers. Session chronology, TLC artifacts, local process state, logs, review
bundles, credentials, customer data, and production output remain under ignored
`session-context/` or in their canonical system.

## Lifecycle

Promote a clarification only after its durable outcome can be separated from the working handoff.
Do not copy a raw handoff into this tree. If an issue receives materially new clarification in a
later cycle, preserve the earlier record and create a new snapshot in the later cycle. Linear, not
the directory location, answers which cycle currently owns the issue.

## Available cycles

- [Cycle 10](./10/README.md)
