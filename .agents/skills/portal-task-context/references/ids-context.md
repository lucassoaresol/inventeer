# IDS Context for Portal Tasks

Read this reference for every Portal task, then load IDS documents only when a trigger below applies.

## Relationship

Portal is the client-facing entry into the Inventeer Delivery System. It presents and enforces parts
of the governed delivery lifecycle, but
`repos/inventeer-ops/artifacts/products/ids` remains canonical for IDS pipeline contracts and
standards. Portal product artifacts may refine the client experience without redefining IDS rules.

## Mandatory IDS triggers

Consult `repos/inventeer-ops/artifacts/products/ids` when the task touches any of these concerns:

- client intake, scoping, routing, maturity, or input quality;
- DAP, EPP, DEP, their structures, required fields, or validation;
- Gate 1, Gate 2, Gate 3, approval, rejection, or sign-off;
- rigor classification or rigor-dependent behavior;
- execution-engine handoff or delivery evidence;
- authority boundaries derived from IDS governance;
- canonical status, lifecycle, or transition meaning inherited from the IDS pipeline;
- output contracts consumed by another IDS stage.

For UI-only presentation, local styling, component refactors, or implementation mechanics with no
pipeline semantic impact, record `IDS context: not applicable` and the reason instead of loading IDS.

## Loading procedure

1. Read `repos/inventeer-ops/CLAUDE.md` before using IDS material.
2. Read `repos/inventeer-ops/artifacts/products/ids/README.md` for the IDS subtree map.
3. Locate the relevant standard by concept under
   `repos/inventeer-ops/artifacts/products/ids/artifacts/`; do not load the entire directory.
4. Prefer the most specific canonical standard or template.
5. Record the exact file and section that constrains the Portal task.
6. Compare Portal artifacts and implementation against that constraint.
7. Report conflicts; do not silently resolve them in favor of Portal code or local docs.

Common entry points include:

| Concern | IDS entry point |
|---|---|
| Pipeline and source-of-truth rules | `repos/inventeer-ops/artifacts/products/ids/artifacts/IDS_Operating_System_Overview.md` |
| Intake scoping | `repos/inventeer-ops/artifacts/products/ids/artifacts/IDS_Product_Intake_Scoping_Standard.md` |
| Intake paths and routing | `repos/inventeer-ops/artifacts/products/ids/artifacts/IDS_Intake_Paths_Framework.md`, `repos/inventeer-ops/artifacts/products/ids/artifacts/IDS_VOB_Routing_Standard.md` |
| Input quality | `repos/inventeer-ops/artifacts/products/ids/artifacts/IDS_Input_Quality_Rules_Standard.md` |
| Intake to DAP Gate | `repos/inventeer-ops/artifacts/products/ids/artifacts/IDS_Intake_to_DAP_Gate_Standard.md` |
| DAP structure | `repos/inventeer-ops/artifacts/products/ids/artifacts/DAP_Internal_Structure_Standard.md`, `repos/inventeer-ops/artifacts/products/ids/artifacts/DAP_Standard_Template.md` |
| EPP structure | `repos/inventeer-ops/artifacts/products/ids/artifacts/EPP_Internal_Structure_Standard.md`, `repos/inventeer-ops/artifacts/products/ids/artifacts/EPP_Standard_Template.md` |
| DEP structure | `repos/inventeer-ops/artifacts/products/ids/artifacts/DEP_Structure_Standard.md` |
| Approval behavior | `repos/inventeer-ops/artifacts/products/ids/artifacts/IDS_Approval_Rules_Standard.md` |
| Rigor | `repos/inventeer-ops/artifacts/products/ids/artifacts/IDS_Rigor_Classification_Standard.md` |
| Execution handoff | `repos/inventeer-ops/artifacts/products/ids/artifacts/EE_Output_Contract.md`, `repos/inventeer-ops/artifacts/products/ids/artifacts/IDS_Execution_Engine_Boundary_Map.md` |

## Boundaries

- Treat IDS as read-only unless the user's task explicitly scopes a change to IDS itself.
- Reference IDS documents by path and section; never duplicate their bodies.
- A Portal task cannot silently amend an IDS contract.
- If the required IDS rule is missing or ambiguous, recommend clarification or an IDS-scoped decision
  before implementing Portal behavior that would establish a competing rule.
