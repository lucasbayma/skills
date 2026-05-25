---
name: candango-discover
description: Candango Discover. Thin Candango wrapper over Matt Pocock's grill-with-docs skill. Use when planning a feature, clarifying ambiguous requirements, preparing candango-plan, or when user wants relentless questions with feature-scoped documentation updates in docs/features using the feature slug.
---

# Candango Discover

Use `$grill-with-docs` as the questioning engine. Pass Candango's feature context path as the docs output target:

`docs/features/<feature-slug>/context.md`

Interview user until plan is precise enough for issues, UATs, and autonomous execution.

Ask one question at a time. For each question, provide recommended answer. 

Before asking the question, check if code/docs can answer. If so, inspect repo instead of asking.

Use `$caveman` style for every user-facing question, summary, and report.

## Explore First

Read relevant:

- `CONTEXT.md`
- `CONTEXT-MAP.md`
- `docs/adr/`
- `docs/agents/`
- existing `docs/features/<feature-slug>/context.md`
- feature docs under configured path
- related issues/stories
- relevant source/tests

Create docs lazily. Write the grill session glossary and resolved context to `docs/features/<feature-slug>/context.md`. Use root `CONTEXT.md` only as input/reference unless the user explicitly asks to update global domain docs. Do not create ADR until a real decision is resolved.

## Question Path

Walk decision tree in dependency order:

1. Business outcome
2. Actors and permissions
3. Domain terms
4. Happy path
5. Edge/error paths
6. Data/API contracts
7. UX/product behavior
8. Interface scope and design artifact decision
9. Rollout/migration
10. UAT acceptance
11. Issue slicing
12. Final validation command
13. Autonomous execution readiness

Stop when next artifact can be produced without hidden context.

## Domain Rules

Challenge glossary conflicts immediately:

`CONTEXT says "Customer" means org, but plan uses customer as person. Which?`

Sharpen fuzzy language:

`"Account" overloaded. Do you mean User, Organization, or Billing Account? Recommended: Billing Account.`

Cross-check code when user claims current behavior. Surface contradictions.

## Documentation Updates

When term resolves, update `docs/features/<feature-slug>/context.md` inline using `references/CONTEXT-FORMAT.md`.

`docs/features/<feature-slug>/context.md` is glossary and feature-context only:

- no implementation notes
- no implementation plans
- no todo list
- no decision log
- no global domain changes unless copied from root `CONTEXT.md` as reference

Offer ADR only when all are true:

- hard to reverse
- surprising without context
- real trade-off

Use `references/ADR-FORMAT.md`.

## Feature-Specific Checks

Before ending, ensure answers exist for:

- What user-visible behavior changes?
- Does scope include interface work: web, app, dashboard, admin, flow, screen, layout, form, table, design system?
- If interface scope exists, did user choose whether to create/edit layouts/screens and where: existing codebase, Figma, screenshots, local design artifacts, or other?
- What is out of scope?
- Which UATs prove business success?
- Which issue tracker should receive work?
- Which slices are AFK vs HITL?
- Which dependencies block issue execution?
- What final validation command should run?
- What manual UAT, if any, blocks `done`?

If interface scope exists, ask exactly one caveman-style question before final summary:

`UI scope found. Create/edit layouts now? Where: existing codebase, Figma, screenshots, local design artifacts, other? Recommended: existing codebase for real UI; docs/features/<feature-slug>/design/ for artifacts.`

If user agrees, use `$candango-design` before `candango-plan` is finalized.

If final validation command is unknown after repo/CI discovery, ask exactly:

`Is there any command you want me to run at the end of feature development?`

## Output

After final question, summarize:

- resolved domain terms
- updated `docs/features/<feature-slug>/context.md`
- business decisions
- technical decisions
- interface/design artifact decision
- UAT signals
- issue slicing implications
- open questions, if any
