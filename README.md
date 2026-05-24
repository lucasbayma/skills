# Autonomous Feature Skills

[![skills.sh](https://skills.sh/b/lucasbayma/skills)](https://skills.sh/lucasbayma/skills)

Skills for planning, specifying, slicing, validating, and executing features with agent subloops.

Inspired by `mattpocock/skills`: small composable skills, repo-local config in `docs/agents/`, vertical slices, TDD, explicit issue tracker, and domain docs.

## Quickstart

1. Run `$setup-autonomous-feature-skills` in the target repo.
2. Clarify ambiguous scope with `$grill-with-docs`.
3. If UI scope exists, create/edit screens with `$huashu-design`.
4. Plan the feature with `$feature-plan`.
5. Write the technical spec with `$feature-spec`.
6. Create tracker issues with `$feature-issues`.
7. Generate UATs with `$feature-uat`.
8. Execute approved issues with `$autonomous-feature-executor`.

## Usage

### Install With skills.sh

Install from GitHub:

```bash
npx skills@latest add lucasbayma/skills
```

Then select the skills you want in the installer.

Recommended install set:

- `setup-autonomous-feature-skills`
- `caveman`
- `grill-with-docs`
- `huashu-design`
- `feature-plan`
- `feature-spec`
- `feature-issues`
- `feature-uat`
- `autonomous-feature-executor`

After installation, run `$setup-autonomous-feature-skills` once in each target repo.

### Manual Install / Link

Use this repo as a skills source for your agent, or copy/link the folders under `skills/` into the agent's skills directory.

Example local layout:

```text
skills/
├── design/huashu-design/
├── engineering/autonomous-feature-executor/
├── engineering/feature-issues/
├── engineering/feature-plan/
├── engineering/feature-spec/
├── engineering/feature-uat/
├── engineering/grill-with-docs/
├── engineering/setup-autonomous-feature-skills/
└── productivity/caveman/
```

### First Run In A Repo

Run setup once per target codebase:

```text
Use $setup-autonomous-feature-skills to configure this repo for autonomous feature delivery.
```

Setup creates repo-local config under `docs/agents/`:

- issue tracker
- feature folder layout
- design artifact rules
- validation command
- autonomous execution rules

### Small Feature

Use when scope is clear and low risk:

```text
Use $feature-plan to plan this small feature: <feature request>.
Then use $feature-spec, $feature-issues, $feature-uat, and $autonomous-feature-executor.
```

Expected output:

- `docs/features/<feature-slug>/plan.md`
- `technical-spec.md`
- `issues.md` or tracker issues
- `uat.md`
- `index.html`
- `state.json`

### Large Or Ambiguous Feature

Use `grill-with-docs` first:

```text
Use $grill-with-docs to clarify this feature against repo docs and business rules: <feature request>.
```

Then:

```text
Use $feature-plan to turn the resolved decisions into a feature plan.
Use $feature-spec to write the technical spec.
Use $feature-issues to create vertical-slice issues.
Use $feature-uat to generate UATs.
Use $autonomous-feature-executor to execute approved issues.
```

### Feature With UI

If `grill-with-docs` finds web/app/dashboard/forms/screens/flows/design-system scope, it asks:

```text
UI scope found. Create/edit layouts now? Where: Figma, local HTML prototype, existing codebase, screenshots, other? Recommended: local HTML prototype first, then port.
```

If yes:

```text
Use $huashu-design to create UI screens/prototype for this feature in docs/features/<feature-slug>/design/.
```

Then link design artifacts from:

- `plan.md`
- `technical-spec.md`
- issues
- `uat.md`

### Feature Without UI

Skip `huashu-design`.

Record in plan/spec:

```text
Design artifacts skipped: no interface scope.
```

### Autonomous Execution

Run after issues/UAT/spec are ready:

```text
Use $autonomous-feature-executor to execute the approved issues for docs/features/<feature-slug>/.
```

Executor creates/updates:

- `docs/features/<feature-slug>/index.html`
- `docs/features/<feature-slug>/state.json`

Loop:

1. Main agent discovers unblocked issues.
2. Executor subagent implements with TDD.
3. Validator subagent reviews without executor context.
4. Main agent sends fixes back if needed.
5. Main agent runs final validation command.
6. Dashboard updates after every major event.

### Prompts

Full pipeline:

```text
Use $setup-autonomous-feature-skills if this repo is not configured.
Use $grill-with-docs to clarify this feature:

<feature request>

If interface scope exists, ask whether to create/edit layouts and where.
Then use $feature-plan, $feature-spec, $feature-issues, $feature-uat, and $autonomous-feature-executor.
All communication and reports must use $caveman.
```

Plan only:

```text
Use $feature-plan to create docs/features/<feature-slug>/plan.md for:

<feature request>
```

Spec only:

```text
Use $feature-spec to create technical-spec.md from docs/features/<feature-slug>/plan.md.
```

Issues only:

```text
Use $feature-issues to create vertical-slice issues from docs/features/<feature-slug>/technical-spec.md.
Target tracker: <GitHub | Linear | Jira | local markdown>.
```

UAT only:

```text
Use $feature-uat to generate UATs from plan/spec/issues in docs/features/<feature-slug>/.
```

UI only:

```text
Use $huashu-design to create/edit screens for docs/features/<feature-slug>/.
Target surface: <Figma | local HTML prototype | existing codebase | screenshots>.
```

## Communication Contract

All user-facing communication and written reports must use repo-local `$caveman`.

This includes:

- planning summaries
- clarification questions
- technical spec summaries
- issue breakdown reports
- UAT reports
- executor reports
- validator reports
- dashboard history
- final completion reports

## Feature Folder

All feature-specific docs and HTML live together:

`docs/features/<feature-slug>/`

Default contents:

- `plan.md`
- `technical-spec.md`
- `uat.md`
- `issues.md`
- `index.html` execution dashboard
- `state.json` execution state
- `design/` local UI/design artifacts

## Skills

- [`setup-autonomous-feature-skills`](./skills/engineering/setup-autonomous-feature-skills/SKILL.md): configure issue tracker, feature folder layout, validation command, dashboard path, and subagent rules.
- [`caveman`](./skills/productivity/caveman/SKILL.md): mandatory terse user-facing communication and reports.
- [`grill-with-docs`](./skills/engineering/grill-with-docs/SKILL.md): stress-test feature plans against domain docs and update glossary/ADRs.
- [`huashu-design`](./skills/design/huashu-design/SKILL.md): create/review UI screens, layouts, and prototypes when feature scope includes an interface.
- [`feature-plan`](./skills/engineering/feature-plan/SKILL.md): shape feature scope, decisions, risks, and delivery slices.
- [`feature-spec`](./skills/engineering/feature-spec/SKILL.md): create technical spec from plan/context.
- [`feature-issues`](./skills/engineering/feature-issues/SKILL.md): publish vertical-slice issues to GitHub, Linear, Jira, or local markdown.
- [`feature-uat`](./skills/engineering/feature-uat/SKILL.md): generate business-facing UAT scenarios.
- [`autonomous-feature-executor`](./skills/engineering/autonomous-feature-executor/SKILL.md): orchestrate TDD executor and read-only validator subagents with HTML dashboard.

## Credits

Forked/adapted skills:

- [`caveman`](./skills/productivity/caveman/SKILL.md): forked from local skill at `/Users/bayma/.agents/skills/caveman/SKILL.md`, originally inspired by Matt Pocock's concise communication workflow.
- [`grill-with-docs`](./skills/engineering/grill-with-docs/SKILL.md): forked/adapted from Matt Pocock's [`grill-with-docs`](https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs).
- [`huashu-design`](./skills/design/huashu-design/SKILL.md): forked/adapted from local [`huashu-design`](https://github.com/alchaincyf/huashu-design)-style skill at `/Users/bayma/.agents/skills/huashu-design/SKILL.md`.

Architecture reference:

- [`mattpocock/skills`](https://github.com/mattpocock/skills): composable skills, repo-local `docs/agents/` config, issue tracker setup, domain docs, vertical slices.

## Execution Model

Main agent:

- discovers executable issues
- builds issue dependency tree
- creates/updates HTML dashboard
- delegates implementation to executor subagent
- delegates review to validator subagent
- loops until validation passes
- runs final validation command

Executor subagent:

- uses TDD
- edits code
- reports changed files, tests, risks

Validator subagent:

- receives issue/spec/UAT and diff
- receives no executor chat context
- does not edit code
- returns pass/fix report

Dashboard statuses:

- `backlog`
- `in-progress`
- `validation`
- `uat`
- `done`
