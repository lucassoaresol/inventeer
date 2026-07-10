# Linear Context for Portal

Read this reference when resolving or validating a Portal issue hierarchy.

## Canonical hierarchy

```text
PROD → INIT → PROJ → MILE → TASK → SUBTASK
```

The permanent product navigation issue for Portal is `INV-254`.

## Responsibilities

| Level | Responsibility |
|---|---|
| PROD | Permanent product purpose, ownership, and scope |
| INIT | Strategic outcome and initiative-level definitions of done |
| PROJ | Coordinated delivery covering one or more INIT outcomes |
| MILE | Verifiable intermediate outcome and milestone DoDs |
| TASK | Implementable or verifiable unit with declared MILE coverage |
| SUBTASK | Small operational step belonging to one TASK |

## Resolution procedure

1. Retrieve the target issue including parent and relations.
2. Follow the parent relationship one level at a time.
3. Confirm that each child uses the next valid hierarchy level.
4. Stop successfully only when the chain reaches `INV-254`.
5. Treat related or blocked-by relations as dependencies, not ancestry.
6. Report missing, skipped, duplicated, archived, or conflicting hierarchy nodes.

## DoD traceability

- Extract the target TASK or SUBTASK's declared MILE DoD coverage.
- Read the parent MILE outcome and its mapping to PROJ DoDs.
- Continue through PROJ and INIT outcomes without inventing implicit mappings.
- Preserve `Full` and `Partial` coverage exactly as declared.
- A partial mapping identifies contribution, not completion of the parent outcome.
- When descriptions conflict across levels, report the conflict and identify each source.

## Fields to capture

- Identifier, title, type label, status, owner, priority, and estimate.
- Objective or North Star question.
- Parent identifier and Linear project association.
- Declared outcome or DoD coverage.
- Blocking, blocked-by, related, duplicate, or archived state when relevant.

## Failure conditions

Do not declare the task prepared when:

- the chain does not reach `INV-254`;
- a required parent is missing;
- the issue type conflicts with its hierarchy position;
- DoD coverage is required but absent or ambiguous;
- the issue is duplicate, canceled, or archived without explicit user intent to inspect history.
