# Claude Runtime State and Session Audit Validation

**Date:** 2026-08-02
**Spec:** `.specs/features/claude-runtime-state-audit/spec.md`
**Behavioral diff range:** `0311bcf..d1cc6f5`
**Verifier:** standalone fresh-eyes fallback, without sub-agents per user request

## Delivery Evidence

- **Validation state:** pass
- **Evidence binding:** four atomic behavioral commits ending at `d1cc6f5`; ignored local settings
  SHA-256 `31f8e24b362e247ce938cd832320375ec970f6a534c713671f721e5f183249fc`
- **Local runtime contract:** `.claude/settings.local.json` sets absolute `OMC_STATE_DIR` to
  `/root/lucas/inventeer/repo/inventeer/session-context/runtime/omc`
- **Gate state:** 88 passed, 0 failed, 0 skipped; targeted fixture 9/9; discrimination sensor
  3/3 killed; range diff integrity clean
- **Runtime smoke:** real Claude sessions started at the workspace root and wrote OMC state only
  below `session-context/runtime/omc/inventeer-7ac4362708085b7e/`, including after `cd repos`
- **Pending delivery conditions:** none; destructive cleanup of legacy `.omc/` directories is a
  separate, explicitly out-of-scope action

## Task Completion

| Task | Status | Evidence |
| --- | --- | --- |
| Define the approved requirement contract | Done | `dbf3e27` |
| Harden session origin and APEX evidence semantics | Done | `575f514` |
| Record the runtime-state policy | Done | `02018ae` and ignored local settings fingerprint above |
| Strengthen discriminating fixtures | Done | `d1cc6f5` |
| Validate real Claude runtime behavior | Done | Smoke sessions `81818181-8181-4818-8818-181818181818` and `91919191-9191-4919-8919-191919191919` |

## Spec-Anchored Acceptance Criteria

| Criterion | Evidence | Result |
| --- | --- | --- |
| Runtime-1 | Local settings contain the exact absolute `OMC_STATE_DIR`; `jq` parsing and fingerprint check passed | PASS |
| Runtime-2 | Root and `cd repos` smoke sessions created state below the central project leaf; legacy `.omc/` mtimes did not change | PASS |
| Runtime-3 | AD-035, `AGENTS.md`, and `README.md` define ignored, ephemeral, non-canonical state and safe cleanup timing | PASS |
| Runtime-4 | AD-035 explicitly preserves AD-031; no Portal artifact route changed | PASS |
| Runtime-5 | `git ls-files session-context .claude/settings.local.json` is empty; no runtime state, local setting, transcript, or secret entered Git | PASS |
| Origin-1 | Drift fixture starts at the workspace and ends in `repos`; exact report still includes its APEX success | PASS |
| Origin-2 | Visitor fixture starts outside and later visits the workspace; exact report excludes it | PASS |
| Origin-3 | The drift fixture reproduces `ea1175a4-a93b-4a29-8968-aa3c59bde4ba` ownership semantics as one logical session | PASS |
| APEX-1 | Exact JSON equality and text assertions require only `apex_tool_*` aggregate names | PASS |
| APEX-2 | `ReadMcpResourceTool` with server `apex` contributes `read_mcp_resource: 1` | PASS |
| APEX-3 | The otherwise equivalent `context7` resource fixture contributes no APEX outcome | PASS |
| APEX-4 | The audit reports transport/tool outcomes only; documentation forbids completion inference | PASS |
| APEX-5 | Exact fixtures preserve success, failure, denial, and unresolved outcomes separately | PASS |

**Status:** all 13 acceptance criteria match the precise spec outcomes.

## Test Adequacy

The final fixture set asserts complete dictionaries, absent legacy keys, text labels, privacy,
session-origin directionality, resource-server discrimination, and all four outcome classes. A
fresh-eyes mutation pass initially exposed two aggregate-invariant fixtures: the drift session had
no distinguishing APEX event, and the non-APEX resource used the same successful outcome as the
APEX resource. Commit `d1cc6f5` made both cases observably distinct before the final gate.

No new lesson was added. The corrected weakness is already covered by confirmed lesson L-008:
contract fixtures must exercise every declared lifecycle edge rather than only the primary path.

## Discrimination Sensor

| Mutation | Expected discriminator | Result |
| --- | --- | --- |
| Replace first-cwd retention with last-cwd behavior | Drift and visitor ownership assertions | KILLED |
| Accept a non-APEX generic resource server | Exact success/failure aggregates | KILLED |
| Restore ambiguous `apex_sessions`/`apex_calls` schema | Exact dictionaries and absent-key assertions | KILLED |

The three mutants ran in disposable scratch copies. The real worktree was not modified by them.

## Gate Check

- `scripts/test-engine-routing.sh`: 9 passed
- `scripts/test-machine-resource-preflight.sh`: 4 passed
- `scripts/test-mcp-config.py`: 11 passed
- `scripts/test-portal-tlc-session-artifacts.sh`: 9 passed
- `scripts/test-session-history-audit.py`: 9 passed
- `scripts/test-sync-apex-commands.sh`: 15 passed
- `.agents/skills/advance-delivery-front/scripts/test-inspect-git-front.sh`: 14 passed
- `.agents/skills/create-review-bundle/scripts/test-create-review-bundle.sh`: 14 passed
- TLC lessons checks: 2 passed
- TLC validation-guidance check: 1 passed
- Total: 88 passed, 0 failed, 0 skipped
- `git diff --check 0311bcf..d1cc6f5`: exit 0
- Runtime smoke: central state updated; all four observed legacy `.omc/` mtimes remained unchanged

The first final-gate preflight invocation used a nonexistent `.py` suffix and exited before running
any test. It was immediately corrected to the canonical `.sh` command above, which passed 4/4; the
invocation mistake changed no file or validation scope.

The machine snapshot reported 2 CPUs, approximately 2.9 GB available memory, no swap, and enough
disk. The complete gate therefore ran serially. No UAT was required for this infrastructure-only
tooling change.

## Requirement Traceability Update

| Requirement | Previous | New |
| --- | --- | --- |
| CRSA-01 through CRSA-08 | Pending | Verified |

## Summary

**Overall:** ready

Claude now receives a stable absolute OMC state root whenever it starts from this workspace, and a
real directory-change smoke test confirms that later working directories do not receive new
`.omc/` state. The sanitized history audit now owns Claude sessions by their origin, recognizes
generic APEX resource reads without counting other servers, and labels every aggregate as
tool-level evidence rather than workflow completion.
