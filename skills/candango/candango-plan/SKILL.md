---
name: candango-plan
description: Candango Plan. Thin Candango wrapper over Matt Pocock's to-prd skill. Use when the user wants to shape feature scope, clarify business rules, split uncertain work from ready work, identify dependencies, and produce a concise implementation-ready plan for later candango-issues, candango-uat, or candango-executor use.
---

# Candango Plan

Create an implementation-ready plan from conversation, repo context, and business definitions.

All user-facing communication and written planning reports must use `$caveman`.

Use `$to-prd` as the planning engine. Save the Candango-shaped output as a feature plan, not a standalone PRD:

`docs/features/<feature-slug>/plan.md`

## Inputs

Use what already exists first:

- user request and conversation context
- `docs/features/<feature-slug>/context.md`
- root `CONTEXT.md`, `CONTEXT-MAP.md`, ADRs as reference inputs
- existing feature docs under configured docs path
- related issues/stories/tasks
- relevant code paths and tests

If setup config is missing, run `candango-setup` first.

If feature scope, terms, business rules, or acceptance signals are ambiguous, run `candango-discover` before writing the plan.

If `candango-discover` identifies interface scope and user wants screens/layouts, run `candango-design` before finalizing delivery slices.

## Workflow

### 1. Frame Feature

Capture:

- problem
- target users/actors
- business outcome
- non-goals
- constraints
- assumptions
- unknowns

Use feature-scoped domain language from `docs/features/<feature-slug>/context.md` when present; fall back to root `CONTEXT.md`.

### 2. Classify Size

Classify as:

- **Small**: one vertical slice, low ambiguity, direct implementation.
- **Medium**: several slices, known architecture.
- **Large**: multiple domains, schema/API/workflow changes, or unresolved business decisions.

Large features need explicit decision log and phased delivery.

### 3. Identify Decisions

Separate:

- business decisions
- UX/product decisions
- interface/design artifact decisions
- technical decisions
- data/API contract decisions
- operational/rollout decisions

Mark each as decided, assumed, or open.

### 4. Draft Delivery Shape

Produce vertical slices, not horizontal layers. Each slice must be demoable or verifiable alone.

For each slice include:

- title
- outcome
- dependencies
- acceptance signals
- design artifact link when UI scope exists
- risk
- AFK/HITL classification

### 5. Confirm

For non-trivial features, ask user to approve only unresolved decisions and slice boundaries. Do not re-ask settled facts.

Use `candango-discover` for one-question-at-a-time clarification when ambiguity remains.

## Output

Write or return a plan using `references/feature-plan-template.md`.

Prefer saving to configured docs path:

`docs/features/<feature-slug>/plan.md`

Keep all feature docs and HTML in `docs/features/<feature-slug>/`.

If user only wants quick planning, return plan in chat.
