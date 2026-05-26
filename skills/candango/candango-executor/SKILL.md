---
name: candango-executor
description: Candango Executor. Execute approved feature issues autonomously through a main-agent orchestration loop. Use when the user wants the agent to identify executable issues, generate an HTML dashboard with dependency tree, Kanban status, and execution history, delegate each issue to a TDD executor subagent, delegate validation to an independent read-only validator subagent, loop until validation passes, run final repo validation, and communicate all user-facing updates and reports using caveman style.
---

# Candango Executor

Main agent orchestrates. Executor subagent edits. Validator subagent reviews only.

## Hard Rules

- Main agent does not implement feature code.
- Executor subagent uses Matt Pocock's `$tdd` and may edit files.
- Validator subagent receives code diff plus issue/plan/UAT context, not executor chat history.
- Validator subagent must not fix code.
- If validator reports required fixes, main agent sends report back to executor.
- Main agent polls/health-checks active subagents every 1 minute when tool support allows.
- Main agent updates dashboard after every status change and major event.
- After any issue transitions to `done`, regardless of its previous status, main agent rechecks every backlog issue and starts any issue that is now unblocked.
- Every user-facing message, dashboard entry, and written report uses `$caveman` style: terse, high-signal, no fluff.
- If issue/plan/UAT conflict or terms are ambiguous, pause execution and use `$candango-discover`.

## Setup

Read:

- `docs/agents/autonomous-feature-execution.md`
- `docs/agents/feature-issue-tracker.md`
- `docs/agents/feature-validation.md`
- `docs/agents/feature-docs.md`
- feature plan/UAT docs
- executable issues from tracker

If final validation command is missing, discover from CI first. If still unknown, ask:

`Is there any command you want me to run at the end of feature development?`

## Issue Discovery

Select issues that are:

- approved for implementation
- AFK/executable
- not blocked by unfinished dependencies
- status `backlog` or explicitly selected by user

Build dependency graph. Detect cycles before starting.

## Dashboard

Use `scripts/feature_dashboard.py`.

Create:

- JSON state: `docs/features/<feature-slug>/state.json`
- HTML page: `docs/features/<feature-slug>/index.html`
- Use same feature folder as `plan.md`, `uat.md`, `issues.md`, and `design/`.

Dashboard must show:

- issue dependency tree with links
- active subagent session output panels
- Kanban columns: `backlog`, `in-progress`, `validation`, `uat`, `done`
- execution history panel with caveman reports
- final validation command/status

See `references/dashboard-state.md`.

## Execution Loop

Run continuously while selected issues remain in `backlog`, `in-progress`, or `validation`.

At startup, and after any issue transitions to `done`, rescan all backlog issues:

- Re-evaluate dependencies against current issue statuses.
- Treat an issue as startable when it is approved, AFK/executable, in `backlog`, and all `blocked_by` issues are complete enough for its dependency rule.
- Start every newly startable issue allowed by current subagent capacity.
- Do not wait for the originally selected unblocked set to drain before discovering newly unblocked backlog work.
- Do not start newly unblocked issues on intermediate transitions such as `validation`, `uat`, or blocked states; only `done` releases new starts after the initial scan.

For each startable issue:

1. Move issue to `in-progress`.
2. Start executor subagent with prompt from `references/executor-prompt.md`.
3. Poll every 1 minute. Update dashboard with health/status and active subagent output.
4. When executor finishes, move issue to `validation`.
5. Start validator subagent with prompt from `references/validator-prompt.md`.
6. If validator passes, move issue to `uat` when UAT/manual acceptance remains, else `done`.
7. If validator requires fixes, move issue to `in-progress` and send validator report to executor.
8. If the issue transitions to `done`, immediately rescan all backlog issues and start any newly unblocked issue.
9. Repeat until pass or blocked.

If UAT is manual, hand off to `$candango-uat-runner` before `done`.

## Final Validation

After all selected issues are `done`:

1. Run configured final validation command.
2. Summarize output in dashboard.
3. If command fails, create corrective issue(s) or send failure back to executor depending on scope.
4. Mark feature complete only after command passes or user explicitly accepts residual risk.

## Stop Conditions

Pause and ask user when:

- dependency cycle exists
- issue requirements conflict with plan/UAT
- validator and executor loop fails twice on same issue with same finding
- final validation requires credentials/env unavailable to agent
- manual UAT needed
