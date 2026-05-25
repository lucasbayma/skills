---
name: candango-uat
description: Candango UAT. Generate user acceptance tests from business definitions, feature plans, feature context, and issue acceptance criteria. Use when the user wants UAT scenarios before implementation, during validation, or before marking autonomous feature work done.
---

# Candango UAT

Create UATs that prove business behavior, not internal implementation.

All user-facing communication and written UAT reports must use `$caveman`.

## Inputs

Read:

- business definitions from conversation/context
- feature plan
- issue acceptance criteria
- design artifacts from `candango-design` when interface scope exists
- `docs/features/<feature-slug>/context.md`
- root `CONTEXT.md` as reference input
- product/domain docs

## Workflow

### 1. Extract Business Rules

List externally visible rules:

- actors
- triggers
- happy paths
- edge cases
- permission boundaries
- error states
- data visibility
- audit/notification outcomes
- visual/interface states when UI scope exists

### 2. Generate Scenarios

Use Given/When/Then format. Each UAT must map to at least one acceptance criterion or business rule.

Classify:

- critical
- important
- optional

Mark whether scenario is automatable, manual, or both.

### 3. Attach To Work

Save by default:

`docs/features/<feature-slug>/uat.md`

Keep all feature docs and HTML in `docs/features/<feature-slug>/`.

For each implementation issue, list related UAT IDs. If tracker supports subtasks, create UAT tasks only when user asks; otherwise keep UATs in docs and link from issues.

### 4. Validation Use

During autonomous execution, validator uses UATs as business oracle. Executor may add automated tests that cover UATs, but validator decides whether behavior matches.

## Output

Use `references/uat-template.md`.
