---
name: candango-setup
description: Candango Setup. Configure a repo for autonomous feature delivery skills. Use before candango-plan, candango-spec, candango-issues, candango-uat, candango-uat-runner, candango-executor, or candango-wrap-up when the repo has not yet declared its issue tracker, feature folder layout, UAT location, validation command discovery rules, dashboard location, design artifact location, or agent execution conventions. Part of Candango Skills by lucasbayma.
---

# Candango Setup

Scaffold per-repo config consumed by the feature delivery skills.

Borrow Matt Pocock's pattern: keep skills small, compose them through repo-local docs, and make tracker/domain choices explicit before work starts.

## Process

### 1. Explore

Inspect current repo before asking questions:

- `git remote -v`, `.git/config`
- `AGENTS.md`, `CLAUDE.md`
- `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/`
- `docs/agents/`
- `.github/workflows/`, CI config, package scripts, Makefile, task runners
- `.scratch/`, `docs/features/`, existing issue/story docs

### 2. Decide Config

Ask only for values not discoverable from repo.

Required decisions:

- **Issue tracker**: GitHub Issues, Linear, Jira, local markdown, or other.
- **Feature folder layout**: all docs, dashboard HTML, state JSON, design artifacts, and local issues live under `docs/features/<feature-slug>/`.
- **Final validation command**: discovered from CI when possible; otherwise ask: `Is there any command you want me to run at the end of feature development?`
- **Dashboard path**: `docs/features/<feature-slug>/index.html`.
- **Dashboard state path**: `docs/features/<feature-slug>/state.json`.
- **Dashboard cleanup**: `$candango-wrap-up` removes runtime dashboard files before PR when they are not needed.
- **Design artifact path/surface**: default ask per feature; local artifacts go under `docs/features/<feature-slug>/design/`; external options Figma, existing codebase, screenshots, other.
- **Status model**: use `backlog`, `in-progress`, `validation`, `uat`, `done`.
- **Subagent policy**: executor may edit; validator may not edit.
- **Implementation style**: executor subagents use repo-local `$candango-tdd`.
- **UAT run style**: `$candango-uat-runner` guides one UAT at a time and restarts TDD fix loops on failure.
- **Wrap-up style**: `$candango-wrap-up` creates PRs with caveman descriptions and UAT status.
- **Communication style**: use repo-local `$candango-caveman` for all user-facing communication and written reports.
- **Clarification style**: use repo-local `$candango-discover` before planning/spec work when feature terms or business rules are ambiguous.

### 3. Write

Before editing `CLAUDE.md` or `AGENTS.md`, ask explicit permission.

Selection rules:

- If `CLAUDE.md` exists, propose editing `CLAUDE.md`.
- Else if `AGENTS.md` exists, propose editing `AGENTS.md`.
- If neither exists, ask which one to create.

Show:

- target file
- exact block to add/update
- docs files to create

Stop until the user approves. Do not modify `CLAUDE.md`, `AGENTS.md`, or create a new agent instruction file before approval.

Add or update one block:

```markdown
## Autonomous feature skills

### Issue tracker

See `docs/agents/feature-issue-tracker.md`.

### Feature docs

See `docs/agents/feature-docs.md`.

### Design artifacts

See `docs/agents/feature-design.md`.

### Validation

See `docs/agents/feature-validation.md`.

### Autonomous execution

See `docs/agents/autonomous-feature-execution.md`.

### Local support skills

Use `$candango-caveman` for every user-facing message/report and `$candango-discover` for feature clarification against docs.
```

Then create:

- `docs/agents/feature-issue-tracker.md`
- `docs/agents/feature-docs.md`
- `docs/agents/feature-validation.md`
- `docs/agents/feature-design.md`
- `docs/agents/autonomous-feature-execution.md`

Use `references/repo-config-templates.md` for starter content.

### 4. Done

Report config files created and which skills consume them. Tell user these files are editable later; rerun setup only when switching tracker or process.
