# LESSONS - auto-maintained by scripts/lessons.py

> Machine-owned. Do NOT hand-edit. Changes are overwritten on the next `lessons.py` write.
> Canonical state lives in `.specs/lessons.json`. Edit lessons only via the script.
> promote_threshold=2 distinct features · window_days=45 · quarantine_threshold=2 · merge_similarity=0.6

## Confirmed (load these at Specify/Design)

Corroborated across multiple features. Safe to apply as guidance.

### L-008 - In workspace contract tests, assert every named authority surface and declared lifecycle edge case, not only the primary path
- signal: `ac_gap` · recurrence: 2 feature(s) · scope: `workspace-contract-tests` · harmful: 1
- features: portal-tlc-session-artifacts, apex-safety-session-audit
- evidence: .specs/features/portal-tlc-session-artifacts/validation.md:49 (workspace-contract-tests) (+1 more)
- last seen: 2026-08-02T11:28:52Z

## Candidates (under observation - do NOT load as guidance yet)

Seen once or not yet corroborated. Tracked, not trusted.

### L-001 - Test invalid-but-resolvable Git refs, not only missing refs, when guards depend on ancestry.
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `git-inspector` · harmful: 0
- features: delivery-front-continuity
- evidence: validation.md:M1 (git-inspector)
- last seen: 2026-07-22T20:39:26Z

### L-002 - Test Git range semantics on diverged histories so two-dot and three-dot behavior cannot pass the same fixture.
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `git-inspector` · harmful: 0
- features: delivery-front-continuity
- evidence: validation.md:M2 (git-inspector)
- last seen: 2026-07-22T20:39:26Z

### L-003 - Run final diff integrity checks against the complete feature evidence range, not only the working tree.
- signal: `gate_fail` · recurrence: 1 feature(s) · scope: `workflow` · harmful: 0
- features: review-evidence-lifecycle
- evidence: .specs/features/review-evidence-lifecycle/validation.md:F1 (workflow)
- last seen: 2026-07-24T14:00:43Z

### L-004 - Bind adjacent checksum entries to the exact artifact basename and digest before treating evidence as verified.
- signal: `ac_gap` · recurrence: 1 feature(s) · scope: `review-bundle` · harmful: 0
- features: review-evidence-lifecycle
- evidence: validation.md:F1 REL-12/REL-14 (review-bundle)
- last seen: 2026-07-24T14:36:08Z

### L-005 - Assert every workspace policy clause explicitly, including exclusions and canonical destinations.
- signal: `ac_gap` · recurrence: 1 feature(s) · scope: `workspace-policy-tests` · harmful: 0
- features: engine-aware-skill-learning
- evidence: .specs/features/engine-aware-skill-learning/validation.md:76 (workspace-policy-tests)
- last seen: 2026-07-28T05:27:56Z

### L-006 - Run a staged or equivalent diff-integrity check for new files before committing
- signal: `gate_fail` · recurrence: 1 feature(s) · scope: `workspace-delivery` · harmful: 0
- features: workspace-mcp-resource-preflight
- evidence: .specs/features/workspace-mcp-resource-preflight/validation.md:63-67 (workspace-delivery)
- last seen: 2026-07-29T00:45:42Z

### L-007 - Resolve MCP working directories from the engine operational workspace root and prove the configured target exists before publication
- signal: `review_finding` · recurrence: 1 feature(s) · scope: `mcp` · harmful: 0
- features: workspace-mcp-resource-preflight-cwd-correction
- evidence: .specs/features/workspace-mcp-resource-preflight/validation.md:Runtime Finding (mcp)
- last seen: 2026-07-29T01:10:51Z

### L-009 - When an acceptance criterion depends on real browser behaviour (focus on a rendered point, responsive reflow), declare it as manual UAT in the spec instead of accepting a class or wiring assertion as coverage
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `jsdom-component-tests` · harmful: 0
- features: technical-dora-metrics-tab
- evidence: session-context/portal/INV-3833/tlc/validation.md#accessibility AC1/AC4 (jsdom-component-tests)
- last seen: 2026-08-18T01:53:08Z

### L-010 - A validation report must not claim full AC coverage while flagging any criterion as a gap: mark those ACs as not covered and keep the checkpoint state below passed until they are verified
- signal: `review_finding` · recurrence: 1 feature(s) · scope: `validation-reports` · harmful: 0
- features: technical-dora-metrics-tab
- evidence: Codex review 01a01295-ae97-7cb2-a136-87dc4d74e3f1 finding 2 (validation-reports)
- last seen: 2026-08-18T03:08:29Z

### L-011 - Apply a visually-hidden utility to a wrapper div, never to a table or other display:table element, which treats height as a minimum and keeps stretching the page's scroll area
- signal: `review_finding` · recurrence: 1 feature(s) · scope: `screen-reader-markup` · harmful: 0
- features: technical-dora-metrics-tab
- evidence: validation.md UAT finding 6 (screen-reader-markup)
- last seen: 2026-08-18T06:23:12Z

### L-012 - When an acceptance criterion uses a broad quantifier (anywhere, everywhere, wherever presented), enumerate the concrete surfaces it must reach, or coverage becomes a judgement call at verification time
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `acceptance-criteria` · harmful: 0
- features: delivery-flow-metrics-tab
- evidence: session-context/portal/INV-3834/tlc/validation.md#AC2 (acceptance-criteria)
- last seen: 2026-08-19T10:32:49Z

### L-013 - When a guard is added to one side of a mirrored pair of endpoints, add the sibling's guard and both tests in the same increment; the untested half survives mutation.
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `http-routes` · harmful: 0
- features: ticket-foundation
- evidence: MU-13 / tickets-attachment-routes.plugin.ts:95 (http-routes)
- last seen: 2026-08-21T10:24:27Z

### L-014 - Pin a permission guard with an actor holding only the required code and another holding only the sibling code; an actor carrying every code cannot tell the two apart.
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `authorization-tests` · harmful: 0
- features: ticket-foundation
- evidence: M17 / tickets-attachment-routes.plugin.ts:150 (authorization-tests)
- last seen: 2026-08-21T10:24:28Z

### L-015 - When tenant scope is enforced in a service, no route may read a body, parse it or emit an audit event before that check runs; assert the audit row count, not only the response status.
- signal: `review_finding` · recurrence: 1 feature(s) · scope: `tenant-scope` · harmful: 0
- features: ticket-foundation
- evidence: TCK-02 / tickets-attachment-routes.plugin.ts:66 (tenant-scope)
- last seen: 2026-08-21T10:24:28Z

### L-016 - A route documented through openAPIRegistry.registerPath receives no validator; enforce in the plain handler every constraint the document publishes, and test that constraint.
- signal: `review_finding` · recurrence: 1 feature(s) · scope: `openapi-contract` · harmful: 0
- features: ticket-foundation
- evidence: Codex review / tickets.schema.ts:342 (openapi-contract)
- last seen: 2026-08-21T10:24:28Z

### L-017 - Reconcile a coverage tally against its own per-criterion table before publishing it; counts that do not sum to the requirement total hide a miscounted criterion.
- signal: `review_finding` · recurrence: 1 feature(s) · scope: `validation-report` · harmful: 0
- features: ticket-foundation
- evidence: validation.md coverage tally, first Verifier pass (validation-report)
- last seen: 2026-08-21T10:24:28Z

### L-018 - Derive the local gate list from every step the CI job runs, not only its npm scripts; a shell script invoked directly can be a distinct gate from the npm script that shares its name.
- signal: `gate_fail` · recurrence: 1 feature(s) · scope: `gate-inventory` · harmful: 0
- features: ticket-foundation
- evidence: CI anti-drift job / .github/workflows/ci.yml:95 (gate-inventory)
- last seen: 2026-08-21T11:06:36Z

### L-019 - When a published event carries its type and its payload as independent members, switch on the payload's own discriminant so the compiler narrows it, and derive the type from that same value instead of casting
- signal: `spec_deviation` · recurrence: 1 feature(s) · scope: `adapters` · harmful: 0
- features: ticket-lifecycle-notifications
- evidence: src/modules/ticket-notifications/application/ticket-lifecycle-notifier.ts:96 (SPEC_DEVIATION marker, validation.md Code Quality) (adapters)
- last seen: 2026-08-25T09:09:16Z

### L-020 - To replace a cached list wholesale rather than merge into it, give the cache key a generation segment instead of overwriting the key in place
- signal: `spec_deviation` · recurrence: 1 feature(s) · scope: `query-cache` · harmful: 0
- features: ticket-detail-overlay
- evidence: src/api/tickets/use-ticket-timeline.ts SPEC_DEVIATION; validation.md 'One SPEC_DEVIATION' (query-cache)
- last seen: 2026-08-25T10:20:43Z

### L-021 - In a suite whose setup already starts a global request-mocking server, register handlers on that server instead of creating a second one, or every request is handled twice
- signal: `review_finding` · recurrence: 1 feature(s) · scope: `integration-tests` · harmful: 0
- features: ticket-detail-overlay
- evidence: src/pages/app/tickets/tickets-flow.integration.test.tsx:387; validation.md 'Issues found' (integration-tests)
- last seen: 2026-08-25T10:20:43Z

### L-022 - Before calling a concurrency test failure a host flake, kill it with a deterministic mutant: if removing the serialization primitive makes it fail every run, it is a defect, and a green CI is favorable scheduling rather than counter-evidence
- signal: `gate_fail` · recurrence: 1 feature(s) · scope: `concurrency-tests` · harmful: 0
- features: ticket-lifecycle-notifications
- evidence: CI run 32852682651 job 97817095822; dod-dataset.integration.spec.ts:106 (concurrency-tests)
- last seen: 2026-08-25T14:29:19Z

### L-023 - When a surface has a published design, read the design source for layout before implementing it: acceptance criteria describe behaviour and never constrain appearance, so a fully green suite says nothing about visual fidelity
- signal: `review_finding` · recurrence: 1 feature(s) · scope: `design-to-code` · harmful: 0
- features: ticket-detail-overlay
- evidence: session-context/portal/INV-3831/tlc/validation.md 'What the UAT found that the tests did not' (design-to-code)
- last seen: 2026-08-25T18:19:31Z

### L-024 - After every exact-text substitution in a source file, read the region back and confirm the change landed: a failed match reports success and the following gate passes on the unchanged code
- signal: `review_finding` · recurrence: 1 feature(s) · scope: `editing` · harmful: 0
- features: ticket-detail-overlay
- evidence: session-context/portal/INV-3831/tlc/validation.md 'Process note — three patches lost silently' (editing)
- last seen: 2026-08-25T18:19:31Z

### L-025 - Take a design's dimensions from the node metadata, not from an exported image, because the export includes shadows and other effects that fall outside the node's own box
- signal: `review_finding` · recurrence: 1 feature(s) · scope: `design-to-code` · harmful: 0
- features: ticket-detail-overlay
- evidence: session-context/portal/INV-3831/tlc/validation.md item 4; ticket-detail-overlay.tsx sheet width (design-to-code)
- last seen: 2026-08-25T18:19:31Z

### L-026 - When state extensions are scoped by a cache generation, extend the old generation, switch generations, and assert the default limit again so leaked state cannot survive mutation.
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `query-cache-tests` · harmful: 0
- features: ticket-detail-overlay
- evidence: session-context/portal/INV-3831/tlc/validation.md:393 (query-cache-tests)
- last seen: 2026-08-25T19:19:16Z

### L-027 - When replacing an approved cache-seeding mechanism, update its task contract and algorithm comments in the same increment so verification evaluates the mechanism actually shipped.
- signal: `review_finding` · recurrence: 1 feature(s) · scope: `query-cache` · harmful: 0
- features: ticket-detail-overlay
- evidence: session-context/portal/INV-3831/tlc/validation.md:405 (query-cache)
- last seen: 2026-08-25T19:19:22Z

### L-028 - When a spec says a view reuses cache, state whether a background revalidation request still fires; with staleTime 0 the cache is served AND a request is issued
- signal: `spec_precision_gap` · recurrence: 1 feature(s) · scope: `tanstack-query-ui` · harmful: 0
- features: metrics-v2-shell
- evidence: session-context/portal/INV-3970/tlc/spec.md — edge case on returning to a page (tanstack-query-ui)
- last seen: 2026-08-26T18:03:43Z

### L-029 - Mutate the seam where a component composes its data hook, not only isolated modules; a suite that mocks the hook cannot detect a page that stopped fetching
- signal: `surviving_mutant` · recurrence: 1 feature(s) · scope: `discrimination-sensor` · harmful: 0
- features: metrics-v2-shell
- evidence: src/pages/app/metrics/pages/pages.test.tsx:234 — enabled:false survived 53 tests (discrimination-sensor)
- last seen: 2026-08-26T18:03:43Z

### L-030 - When retiring a test, split assertions that bundle two subjects; one half can outlive the construct that died and its loss is a silent regression
- signal: `review_finding` · recurrence: 1 feature(s) · scope: `test-migration` · harmful: 0
- features: metrics-v2-shell
- evidence: session-context/portal/INV-3970/tlc/evidence/t9-assertion-map.md:50 (test-migration)
- last seen: 2026-08-26T18:03:43Z

## Quarantined (failed when applied - ignore)

A confirmed lesson that recurred alongside failure. Kept for the maintainer to review.

_none_
