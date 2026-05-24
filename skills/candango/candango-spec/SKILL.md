---
name: candango-spec
description: Candango Spec. Create a technical specification from a feature plan, PRD, issue, or conversation context. Use when the user wants a concrete implementation spec covering architecture, contracts, data changes, test strategy, validation commands, rollout, and risks before creating issues or executing a feature autonomously. Part of Candango Skills by lucasbayma.
---

# Candango Spec

Turn approved plan into technical spec another agent can implement without hidden context.

All user-facing communication and written spec reports must use `$candango-caveman`.

## Preconditions

Prefer `candango-plan` first unless feature is tiny and already clear.

Use `candango-discover` first when business definitions, domain terms, or validation expectations are ambiguous.

Use `candango-design` before finalizing the spec when the business definition includes interface scope and the user wants layouts/screens created or edited.

Read:

- repo setup docs under `docs/agents/`
- `docs/features/<feature-slug>/context.md`
- root `CONTEXT.md` and ADRs as reference inputs
- relevant source modules and tests
- existing specs for same area

## Workflow

### 1. Discover Architecture

Identify existing patterns for:

- routing/API
- state/data model
- persistence
- auth/permissions
- validation
- background jobs/events
- UI conventions
- design artifacts from `candango-design`, Figma, screenshots, or existing UI
- tests and CI

Reference behavior and interfaces, not speculative file lists.

### 2. Define Contracts

Specify durable contracts:

- public interfaces
- request/response shapes
- schema changes
- events
- permissions
- error states
- observability expectations

Avoid brittle implementation detail unless it encodes a real decision.

### 3. Define Test Strategy

Prefer behavior tests through public interfaces. Include:

- existing test examples to copy
- new test cases by behavior
- fixtures/data needs
- UAT source signals
- design acceptance signals for UI states when interface scope exists
- final validation command

If final command is not discoverable from CI/package scripts, ask user exactly:

`Is there any command you want me to run at the end of feature development?`

### 4. Write Spec

Use `references/technical-spec-template.md`.

Save by default:

`docs/features/<feature-slug>/technical-spec.md`

Keep all feature docs and HTML in `docs/features/<feature-slug>/`.

## Quality Bar

Spec is ready when:

- executor can implement without more conversation
- validator can check behavior against acceptance criteria
- issues can be sliced without inventing requirements
- UATs can be derived from business rules
