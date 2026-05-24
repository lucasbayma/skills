---
name: feature-wrap-up
description: Wraps completed feature work into a clean pull request with caveman summary, UAT status, validation evidence, and temporary dashboard cleanup. Use when the user asks to wrap up, finalize, prepare PR, create PR, ship feature work, or clean temporary feature dashboard files.
---

# Feature Wrap-Up

Finalize feature work and create a PR.

All user-facing communication and PR text must use `$caveman`.

## Inputs

Read:

- `docs/features/<feature-slug>/plan.md`
- `technical-spec.md`, `issues.md`, `uat.md`
- dashboard state when present
- current git branch, diff, commits, and remote
- validation commands from repo docs or CI config

If feature folder or PR target branch is ambiguous, ask once.

## Workflow

### 1. Clean Temporary Files

Remove generated dashboard runtime files that should not ship:

- `docs/features/<feature-slug>/index.html`
- `docs/features/<feature-slug>/state.json`
- `docs/features/<feature-slug>/state.json.lock`
- hidden temp files matching dashboard atomic-write leftovers

Do not remove plan/spec/issues/UAT/design artifacts unless user asks.

### 2. Verify

Run:

- focused tests touched by implementation
- final validation command when known
- lint/typecheck when cheap and relevant
- UAT status check from `uat.md`

If UATs exist:

- list checked UATs as `[x]`
- list missing/unconfirmed UATs as `[ ]`
- do not claim UAT complete unless all required scenarios are checked

### 3. Classify PR

- `[bugfix]` for defect fixes, regressions, failed UAT fixes, or production bug work
- `[chore]` for docs, tooling, tests-only, dependency, cleanup, or internal maintenance
- `[feat]` for user-visible product behavior or new capability

Title format: `[feat|chore|bugfix] <clear implementation title>`. Use implementation-specific title, not generic feature folder name.

### 4. Commit

Before staging:

- inspect `git status -sb`
- inspect diff
- stage only intended files
- never stage unrelated user changes silently

Commit message should be terse and match the PR scope.

### 5. Create PR

Use GitHub CLI or configured connector. PR description must use caveman style:

```md
## Summary
- <what changed>
- <why>

## UAT
- [x] UAT-001 <short title/evidence>
- [ ] UAT-002 <reason unmarked>

## Validation
- <command>: pass/fail/not run

## Cleanup
- removed temporary dashboard files: yes/no
```

Default to draft PR when validation or required UAT is missing. Mark ready only when user asks or all required checks are complete.

## Stop Conditions

Pause before PR when:

- unrelated worktree changes are mixed with feature changes
- final validation fails
- required UATs remain unconfirmed and user asked for ready PR
- branch/remote/auth is missing
