---
name: candango-discover
description: Candango Discover. Stress-test a feature plan against the repo's domain language, docs, ADRs, business rules, UAT needs, tracker shape, validation command, and autonomous execution readiness. Use when planning a feature, clarifying ambiguous requirements, preparing candango-plan or candango-spec, or when user wants relentless questions with feature-scoped documentation updates in docs/features using the feature slug. Fork credit to Matt Pocock grill-with-docs.
---

# Candango Discover

Interview user until plan is precise enough for spec, issues, UATs, and autonomous execution.

Ask one question at a time. For each question, provide recommended answer. 

Before asking the question, check if code/docs can answer. If so, inspect repo instead of asking and then confirm.

Use `$candango-caveman` style for every user-facing question, summary, and report.

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

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Update CONTEXT.md inline

When a term is resolved, update update `docs/features/<feature-slug>/context.md` inline using `references/CONTEXT-FORMAT.md`. Don't batch these up — capture them as they happen.

`CONTEXT.md` should be totally devoid of implementation details. Do not treat `CONTEXT.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).


## Documentation Updates

When term resolves, update `docs/features/<feature-slug>/context.md` inline using `references/CONTEXT-FORMAT.md`.

`docs/features/<feature-slug>/context.md` is glossary and feature-context only:

- no implementation notes
- no specs
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
- If interface scope exists, did user choose whether to create/edit layouts/screens and where: Figma, local HTML prototype, existing codebase, screenshots, or other?
- What is out of scope?
- Which UATs prove business success?
- Which issue tracker should receive work?
- Which slices are AFK vs HITL?
- Which dependencies block issue execution?
- What final validation command should run?
- What manual UAT, if any, blocks `done`?

If interface scope exists, ask exactly one caveman-style question before final summary:

`UI scope found. Create/edit layouts now? Where: Figma, local HTML prototype, existing codebase, screenshots, other? Recommended: local HTML prototype first, then port.`

If user agrees, use `$candango-design` before `candango-plan` or `candango-spec` is finalized.

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
