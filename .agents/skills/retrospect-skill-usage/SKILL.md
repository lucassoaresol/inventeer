---
name: retrospect-skill-usage
description: Analyze skill use and behavior retrospectively from sanitized Codex and Claude session-history metrics. Use for skill or workflow retrospectives and recommendations; do not use for product discovery, pull-request review, ordinary status reporting, or implementation.
---

# Retrospect Skill Usage

Produce an evidence-bounded retrospective in chat without persisting transcript content. This skill
is read-only: it may recommend a change, but it does not edit skills, instructions, histories, or
product repositories.

## Workflow

1. Define the cohort before interpretation:

   - use this workspace's exact root `cwd`;
   - choose a closed UTC interval `[since, until)`;
   - identify the current Codex or Claude session and pass it with `--exclude-session`;
   - record requested, matched, and unmatched exclusions; an unmatched current-session exclusion is
     a limitation, not proof that the session was absent;
   - distinguish primary sessions, continuations, sidechains, subagents, copies, and logical work
     streams using the auditor's fields.

2. Generate the sanitized receipt:

   ```bash
   scripts/audit-session-history.py \
     --cwd <exact-workspace-root> \
     --since <inclusive-utc> \
     --until <exclusive-utc> \
     --exclude-session <current-session-id> \
     --workspace-id inventeer-personal-engineering \
     --format receipt-json
   ```

   Use the engine history roots associated with this workspace when defaults cannot resolve them.
   Do not copy transcripts, prompts, commands, tool results, physical paths, session IDs, or receipt
   internals into a versioned artifact.

3. Interpret evidence by strength:

   - `skill_invocations` is a structured native invocation signal;
   - `skill_load_proxies` is only evidence that an exact workspace `SKILL.md` path appeared in a
     tool-call input; it does not prove invocation or compliant execution;
   - prose mentions are neither invocation nor load evidence;
   - `null` plus `unsupported_metrics` means not measurable, never zero;
   - do not compare a metric across engines when either engine lists it as unsupported.

   Before treating zero use as a finding, establish an opportunity denominator from requests for
   which the skill should actually have applied. If that opportunity cannot be measured safely,
   label the conclusion qualitative or indeterminate. A call or load alone also does not prove the
   skill's behavioral contract was followed; use sanitized outcomes or directly inspect only the
   minimum relevant local evidence.

4. Report the cohort, limitations, observed behavior, and recommendations in chat. Separate facts
   from inference and classify every recommendation as one of:

   - engine limitation;
   - ambient instruction misplaced;
   - skill execution failure;
   - existing skill improvement;
   - genuinely missing capability.

   Prefer improving an existing owner when the capability already belongs there. Propose a new
   skill only for a repeated, bounded workflow with a distinct owner and meaningful reusable
   guidance.

## Handoff boundary

Do not implement recommendations in this workflow. If the user authorizes implementation, hand a
skill creation or update to `skill-creator` and execute/specify/validate the change with
`tlc-spec-driven`. Product findings belong in their canonical product source, and transversal
workspace decisions follow `.specs/STATE.md`; neither move is authorized by retrospective analysis
alone.
