# Versioned Cycle Task Clarifications Design

**Spec:** `.specs/features/versioned-cycle-task-clarifications/spec.md`
**Status:** Approved

## Architecture Overview

The versioned layer is a curated historical register, organized by cycle first and product second.
Each issue has one Markdown record containing the durable clarification outcome. The ignored session
tree remains the working surface and is not linked as a required dependency.

```text
cycles/
└── 10/
    ├── README.md
    └── portal/
        └── tasks/
            ├── README.md
            └── INV-xxxx.md
```

The cycle index answers what was clarified in that planning window. Each task record answers what
was learned, which decisions survived, what remained outside the task, and where current facts must
be revalidated.

## Existing Components to Leverage

| Component | Location | How to use |
| --- | --- | --- |
| Project authority map | `projects/portal.md` | Point readers from the product entry point to cycle clarification records while preserving canonical sources. |
| Ephemeral task workspace | `session-context/portal/<INV-ID>/` | Source material for one-time curation only; never a runtime dependency of the promoted record. |
| Cycle 10 analysis | `session-context/portal/cycle-10/` | Identify the initial task set and cross-task clarification outcomes without promoting the raw analysis. |
| Workspace contract suite | `scripts/test-workspace.sh` | Run a focused structural and safety test as part of the terminal root gate. |

## Record Contract

Every promoted task file contains:

- cycle, product, record type, snapshot date, and lifecycle-at-snapshot metadata;
- an authority notice that names Linear and the applicable product sources;
- the durable clarification outcome;
- consolidated decisions and boundaries;
- dependencies or unresolved decisions that were material at the snapshot;
- canonical source pointers that allow revalidation without local session artifacts.

Records exclude chat/session IDs, process state, branch instructions, logs, raw API output,
credentials, customer data, TLC task state, and review bundles.

## Lifecycle

1. Clarification can be drafted and iterated in ignored session context.
2. Promotion happens only after the durable outcome can be separated from chronology and runtime
   evidence.
3. The record is written inside the cycle in which that clarification informed planning.
4. Later status changes do not silently update historical metadata.
5. A material clarification in another cycle creates a new snapshot in that cycle and references
   the earlier record; it does not move the old file.

## Error Handling Strategy

| Error scenario | Handling | Impact |
| --- | --- | --- |
| Missing or extra initial Cycle 10 task | Contract test fails with the task-set difference | Prevents an incomplete first promotion. |
| Missing authority or lifecycle section | Contract test fails with the file path | Prevents a local note from masquerading as canonical state. |
| Operational marker in a durable record | Contract test fails closed | Keeps session/runtime details out of Git. |
| Missing `/session-context/` ignore rule | Contract test fails | Preserves the existing ephemeral boundary. |

## Risks & Concerns

| Concern | Location | Impact | Mitigation |
| --- | --- | --- | --- |
| Raw handoffs contain superseded conclusions and local operational evidence | `session-context/portal/INV-*/clarification-handoff.md` | Blind copying would create stale and noisy durable records. | Curate only final decisions, boundaries, dependencies, and canonical source pointers. |
| Cycle snapshots can be mistaken for current Linear state | `cycles/<cycle>/<product>/tasks/` | An agent could act on stale owner, relation, or status data. | Required authority and snapshot metadata plus mandatory revalidation instructions. |
| A task can span cycles | Cycle hierarchy | Moving the file would erase planning history; copying without semantics would create ambiguity. | Preserve old snapshots and add a new cycle-scoped record only for material re-clarification. |
| Current worktree contains unrelated lesson edits | `.specs/LESSONS.md`, `.specs/lessons.json` | Broad formatting or cleanup could overwrite user work. | Do not touch those paths; gates compare and preserve them. |

## Tech Decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Top-level grouping | Cycle first, then product, then tasks | Matches the user's confirmed mental model that INVs belong inside Cycle 10 and leaves room for multiple products in a cycle. |
| File granularity | One Markdown file per INV | Gives each clarification an independent history and avoids one large mutable cycle document. |
| Promotion form | Curated task record, not copied handoff | Keeps durable signal while excluding obsolete chronology and execution state. |
| Canonical status | Historical non-canonical snapshot | Preserves planning memory without competing with Linear or product repositories. |

The hierarchy and lifecycle are cross-workspace conventions and therefore require a new active
decision in `.specs/STATE.md`.
