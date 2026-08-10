# IDS Context for Assistants Tasks

Read this reference for every Assistants task, then load IDS material only when a trigger applies.

## Relationship

Assistants is a governed Inventeer product. Its DAP, EPP, DEP and Gate state live canonically under
the Assistants workspace in
`repos/inventeer-ops/artifacts/products/ids/clients/Inventeer-Internal/Inventeer-Assistants/`;
`repos/assistants/artifacts` consumes and refines those contracts but cannot contradict or duplicate
them.

## Mandatory IDS triggers

Consult `repos/inventeer-ops/artifacts/products/ids` when the task touches:

- product scope, requirements, DoDs, non-goals, or acceptance governed by DAP;
- architecture, runtime, infrastructure, security, persistence, provider, or delivery constraints
  locked by EPP;
- Gate 1, Gate 2, Gate 3, approval, sign-off, or material change;
- DEP evidence, go-live evidence, validation packaging, or delivery completion;
- rigor classification or approval requirements;
- execution-engine boundaries or governed handoff;
- a conflict between implemented reality and a governing product contract.

For isolated runtime refactors, tests, bug fixes, or implementation mechanics with no contract
impact, record `IDS context: not applicable` and the reason instead of loading IDS.

## Loading procedure

1. Read `repos/inventeer-ops/CLAUDE.md` before using IDS material.
2. Read `repos/inventeer-ops/artifacts/products/ids/README.md` for the IDS subtree map.
3. Locate the Assistants workspace under
   `repos/inventeer-ops/artifacts/products/ids/clients/Inventeer-Internal/Inventeer-Assistants/`.
4. Load only the applicable canonical DAP, EPP, DEP, or IDS standard.
5. Record the exact file and section constraining the task.
6. Compare the local Assistants artifact and implementation against that source.
7. Report contradictions and uncertain contract status; do not silently choose the codebase version.

Common entry points:

| Concern | IDS entry point |
|---|---|
| DAP / product contract | `repos/inventeer-ops/artifacts/products/ids/clients/Inventeer-Internal/Inventeer-Assistants/01-DAP/` |
| EPP / engineering contract | `repos/inventeer-ops/artifacts/products/ids/clients/Inventeer-Internal/Inventeer-Assistants/02-EPP/` |
| DEP / delivery evidence | `repos/inventeer-ops/artifacts/products/ids/clients/Inventeer-Internal/Inventeer-Assistants/03-DEP/` |
| Inputs and superseded material | `repos/inventeer-ops/artifacts/products/ids/clients/Inventeer-Internal/Inventeer-Assistants/04-Inputs/`, `99-Archive/` when present |
| Pipeline and source-of-truth rules | `repos/inventeer-ops/artifacts/products/ids/artifacts/IDS_Operating_System_Overview.md` |
| Approval behavior | `repos/inventeer-ops/artifacts/products/ids/artifacts/IDS_Approval_Rules_Standard.md` |
| Rigor | `repos/inventeer-ops/artifacts/products/ids/artifacts/IDS_Rigor_Classification_Standard.md` |

## Boundaries

- Treat IDS as read-only unless the user's task explicitly scopes an IDS contract change.
- Reference contract paths and sections; never copy contract bodies.
- A code or artifact change in Assistants cannot silently ratify a contract deviation.
- If implementation reality intentionally diverged, require evidence of the approving decision or
  recommend resolving the governance conflict before building further on it.
