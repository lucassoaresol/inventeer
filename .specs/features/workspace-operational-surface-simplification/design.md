# Workspace Operational Surface Simplification Design

## Decision Summary

Use existing workspace control planes instead of adding a new skill. Extend the context manifest,
narrow the generated APEX surface, add one metadata-only hygiene script, and register a disabled
stdio Figma server beside the official remote server.

## Components

| Component | Change | Boundary |
| --- | --- | --- |
| Context routing | Add `project-discovery` to the closed route manifest and planner | Reads metadata only before the discovery skill loads sources |
| Discovery skill | Replace unconditional repository update with read-only freshness evidence and separately authorized synchronization | Never mutates repos during discovery by default |
| APEX sync | Select only `all-tools`; remove all other generated wrappers | Diagnostic resource inspection only; TLC remains executor |
| Hygiene inventory | Read lesson metadata and top-level ephemeral paths; accept explicit lifecycle evidence flags | No content emission and no deletion operation |
| Figma pilot | Add pinned stdio server on loopback, disabled/not auto-enabled | Official OAuth server remains the default |
| Contract tests | Assert every authority, lifecycle, pin, address, and opt-in boundary | Follows confirmed lesson L-008 |

## Hygiene State Model

```text
Portal issue directory
  ├─ merged + closed evidence → eligible
  └─ otherwise               → external-confirmation-required

OMC runtime directory
  ├─ explicitly ended → eligible
  └─ otherwise        → liveness-confirmation-required

Unknown directory → protected-unclassified
```

The script reports eligibility only. It exposes no delete command.

## Figma Pilot Flow

```text
Official `figma` (enabled, OAuth, remote) ──→ default workflow

`figma-local` (disabled, stdio)
  └─ npx pinned package
       └─ 127.0.0.1:1994
            └─ manually installed Figma Desktop plugin
                 └─ disposable pilot file
```

## Security and Failure Handling

- Reject mutable package versions and non-loopback configuration in tests.
- Keep Codex approval at `prompt` for the whole local server during the pilot.
- Do not add `figma-local` to Claude's auto-enabled MCP list.
- Fail APEX sync if the aggregate inspector is missing.
- Treat timestamps as retention signals only; lifecycle evidence remains explicit.
- Preserve unknown and symlinked ephemeral paths as protected.
