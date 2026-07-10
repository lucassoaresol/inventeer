# Portal Repository Topology

Read this reference before assigning implementation ownership.

## `repos/portal` — product understanding

Owns product artifacts, authority model, product requirements, plans, and the governed understanding
of Portal. Start here to understand what behavior means and why it exists.

It does not replace implementation, runtime tests, or repo-local technical decisions in API and web.

## `repos/portal-api` — backend and contracts

Owns backend business logic, public/shared contracts, persistence, migrations, server-side governance,
request transitions, snapshots, audit writes, and API behavior.

Read its `AGENTS.md` before acting. Shared contract changes begin here; identify downstream impact on
Portal Web explicitly.

## `repos/portal-web` — frontend

Owns the client-rendered experience, presentation, route and local UI state, forms, and consumption of
API-owned contracts.

It must not redefine shared contracts or absorb core backend business and governance rules.

## `repos/ids` — canonical delivery-system context

Owns pipeline standards and contracts that Portal presents or enforces. It is a contextual,
read-only dependency for Portal tasks with an IDS dimension, not an implementation repo for ordinary
Portal delivery. Load it selectively according to [ids-context.md](ids-context.md).

## Ownership decision

Classify the requested outcome:

| Outcome | Primary repo | Check related repo |
|---|---|---|
| Product definition or artifact | `portal` | API/web only if implementation impact is requested |
| Endpoint, business rule, contract, persistence | `portal-api` | `portal-web` for consumer impact |
| Page, interaction, presentation, client state | `portal-web` | `portal-api` for contract support |
| End-to-end workflow or shared contract change | Explicit multi-repo scope | all affected worktrees and gates |
| IDS-governed pipeline behavior | Portal implementation owner | `ids` for canonical constraints, read-only |

Do not broaden a single-repo task into cross-repo implementation based only on possible future impact.
Report downstream impact separately unless the requested outcome requires coordinated changes now.
