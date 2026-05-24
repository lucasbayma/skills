---
name: feature-uat-runner
description: Runs existing feature UATs interactively against the implemented code, guiding the user through each scenario and marking confirmations. Use when the user wants to run UAT, validate acceptance manually, check off UAT scenarios, or restart development from a failed UAT.
---

# Feature UAT Runner

Run UATs from `docs/features/<feature-slug>/uat.md` one scenario at a time.

All user-facing communication and written UAT reports must use `$caveman`.

## Inputs

Read:

- `docs/features/<feature-slug>/uat.md`
- `plan.md`, `technical-spec.md`, `issues.md`, and dashboard state when present
- repo setup docs under `docs/agents/`
- stack files such as `package.json`, lockfiles, Docker files, app config, routes, tests, and README
- relevant code paths for each UAT scenario

If feature folder is ambiguous, ask which `docs/features/<feature-slug>/` to use.

## Workflow

### 1. Prepare Run

Infer the technical stack and test surface:

- app start command
- focused test command
- seed/data setup
- browser/API/CLI path to exercise
- required env vars or credentials
- whether scenario is automated, manual, or both

Do not ask the user to inspect implementation details. Give user-facing steps only.

### 2. Guide Each Scenario

For each unchecked UAT:

1. Show UAT id/title and expected outcome.
2. Run automatable checks yourself when available.
3. Give precise manual steps for the user, based on the repo stack.
4. Ask for confirmation: passed, failed, or blocked.
5. Wait for user answer before moving to next UAT.

### 3. Mark Checked

When user confirms pass:

- update `uat.md`
- prefer existing checkbox/status format if present
- otherwise maintain a `## UAT Run Log` section:
  - `- [x] UAT-001: passed <ISO timestamp> - <short evidence>`

When blocked or failed:

- record under `## UAT Run Log`:
  - `- [ ] UAT-001: failed <ISO timestamp> - <problem>`
- do not mark checked

### 4. Failure Loop

If user says a UAT failed or describes a problem:

1. Capture exact repro, expected behavior, actual behavior, and evidence.
2. Search code/tests/docs for likely source.
3. Start a fix loop using repo-local `$tdd`.
4. Add or update behavior tests that reproduce the failed UAT.
5. Implement the minimal fix.
6. Run focused tests, relevant validation, and the failed UAT again.
7. Return to the UAT checklist only after validation passes.

For autonomous feature execution, send the UAT failure back through `$autonomous-feature-executor` instead of bypassing the executor/validator split.

## Stop Conditions

Pause and ask when:

- UAT steps require unavailable credentials or third-party access
- environment setup cannot be inferred
- expected behavior conflicts with spec/issues
- user reports behavior that cannot be reproduced after investigation

## Output

Keep a terse caveman report:

- UATs passed
- UATs failed/blocked
- files updated
- commands run
- fix loop status when failures occurred
