---
name: tdd
description: Test-driven development with red-green-refactor for autonomous feature execution. Use when implementing feature issues, fixing validator findings, writing behavior tests, building vertical slices, or when autonomous-feature-executor delegates an issue to an executor subagent. Requires one behavior at a time, public-interface tests, minimal implementation, and caveman-style user-facing reports.
---

# Test-Driven Development

Use `$caveman` for every user-facing update and final report.

Executor subagent uses this skill for one issue at a time. Main agent does not implement code.

Candango role: build discipline. Converts one approved issue into tested behavior through red-green-refactor.

## Philosophy

Tests verify behavior through public interfaces, not implementation details. Code can change; behavior contract stays.

Good tests:

- exercise real code paths
- use public APIs/UI/CLI boundaries
- read like specs
- survive refactors

Bad tests:

- mock internal collaborators by default
- test private methods
- assert implementation shape
- pass while user-visible behavior breaks

Read when needed:

- `references/tests.md`
- `references/mocking.md`
- `references/deep-modules.md`
- `references/interface-design.md`
- `references/refactoring.md`

## Autonomous Feature Contract

Input must include:

- issue body
- acceptance criteria
- feature plan/spec/UAT links or text
- relevant repo docs
- validator report when in fix loop

Output report must include:

- issue id
- behavior implemented
- tests added/changed
- files changed
- commands run
- validator findings addressed
- risks/open items

## Anti-Pattern: Horizontal Slices

Do not write all tests first, then all implementation.

Correct loop:

```text
RED: one failing behavior test
GREEN: minimal code to pass
REFACTOR: clean only while green
```

Repeat per behavior.

## Workflow

### 1. Orient

Before edits:

- read issue/spec/UAT
- inspect existing tests for same area
- find public interface to test
- identify final/local validation command
- list behaviors to cover

Do not ask user during autonomous execution unless issue/spec/UAT conflict.

### 2. First Tracer Bullet

Write one failing test for one externally visible behavior.

Confirm failure is meaningful:

- test fails for expected reason
- failure proves missing behavior
- no unrelated failure masks signal

### 3. Green

Implement minimum code to pass current test.

Rules:

- no speculative features
- no broad refactor while red
- no unrelated cleanup
- no silent contract changes

### 4. Increment

For each remaining behavior:

- add one test
- see it fail
- implement minimal code
- run focused tests

### 5. Refactor

Only when green:

- remove duplication
- deepen modules
- improve names
- simplify interface
- keep behavior tests passing

### 6. Validate

Run:

- focused test command
- relevant lint/typecheck if cheap
- issue-specific command from spec

Return caveman report.

## Checklist Per Cycle

```text
[ ] Test describes behavior, not implementation
[ ] Test uses public interface
[ ] Test fails before implementation
[ ] Code is minimal for current behavior
[ ] No speculative feature
[ ] Refactor only while green
[ ] Commands reported
```
