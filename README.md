# Candango Skills

[![skills.sh](https://skills.sh/b/lucasbayma/skills)](https://skills.sh/lucasbayma/skills)

Candango Skills is a coordinated set of agent skills for building software features from intent to validated execution.

Inspired by `mattpocock/skills`: small composable skills, repo-local config in `docs/agents/`, vertical slices, TDD, explicit issue tracker, and domain docs.

`Candango` is the project identity: a builder-oriented workflow for coordinating planning, design, issue slicing, testing, validation, UAT, wrap-up, and execution into one feature worksite.

## Quickstart

1. Run `$setup-autonomous-feature-skills` in the target repo.
2. Clarify ambiguous scope with `$grill-with-docs`.
3. If UI scope exists, create/edit screens with `$huashu-design`.
4. Plan the feature with `$feature-plan`.
5. Write the technical spec with `$feature-spec`.
6. Create tracker issues with `$feature-issues`.
7. Generate UATs with `$feature-uat`.
8. Execute approved issues with `$autonomous-feature-executor`.
9. Run guided UAT with `$feature-uat-runner`.
10. Wrap up and create PR with `$feature-wrap-up`.

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
- `tdd`
- `feature-plan`
- `feature-spec`
- `feature-issues`
- `feature-uat`
- `feature-uat-runner`
- `autonomous-feature-executor`
- `feature-wrap-up`

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
├── engineering/feature-uat-runner/
├── engineering/feature-wrap-up/
├── engineering/grill-with-docs/
├── engineering/setup-autonomous-feature-skills/
├── engineering/tdd/
└── productivity/caveman/
```

### First Run In A Repo

Run setup once per target codebase:

```text
Use $setup-autonomous-feature-skills to configure this repo for Candango delivery.
```

Setup creates repo-local config under `docs/agents/`:

- issue tracker
- feature folder layout
- design artifact rules
- validation command
- Candango execution rules

### Small Feature

Use when scope is clear and low risk:

```text
Use $feature-plan to plan this small feature: <feature request>.
Then use $feature-spec, $feature-issues, $feature-uat, and $autonomous-feature-executor.
```

Expected output:

- `docs/features/<feature-slug>/context.md`
- `docs/features/<feature-slug>/plan.md`
- `technical-spec.md`
- `issues.md`
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
- `context.md`
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
Then use $feature-plan, $feature-spec, $feature-issues, $feature-uat, $autonomous-feature-executor, $feature-uat-runner, and $feature-wrap-up.
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

Run UAT:

```text
Use $feature-uat-runner to guide me through UATs from docs/features/<feature-slug>/uat.md.
```

Wrap up:

```text
Use $feature-wrap-up to clean temporary dashboard files and create a PR for docs/features/<feature-slug>/.
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
- UAT run confirmations
- executor reports
- validator reports
- dashboard history
- final completion reports
- PR descriptions

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

`index.html` and `state.json` are runtime dashboard files. `$feature-wrap-up` removes them before PR when they are not needed.

## Skills

- [`setup-autonomous-feature-skills`](./skills/engineering/setup-autonomous-feature-skills/SKILL.md): configure issue tracker, feature folder layout, validation command, dashboard path, and subagent rules.
- [`caveman`](./skills/productivity/caveman/SKILL.md): mandatory terse user-facing communication and reports.
- [`grill-with-docs`](./skills/engineering/grill-with-docs/SKILL.md): stress-test feature plans against domain docs and write feature-scoped `context.md`.
- [`huashu-design`](./skills/design/huashu-design/SKILL.md): create/review UI screens, layouts, and prototypes when feature scope includes an interface.
- [`tdd`](./skills/engineering/tdd/SKILL.md): implement one issue at a time with red-green-refactor.
- [`feature-plan`](./skills/engineering/feature-plan/SKILL.md): shape feature scope, decisions, risks, and delivery slices.
- [`feature-spec`](./skills/engineering/feature-spec/SKILL.md): create technical spec from plan/context.
- [`feature-issues`](./skills/engineering/feature-issues/SKILL.md): write `issues.md` and publish vertical-slice issues to GitHub, Linear, Jira, or local markdown.
- [`feature-uat`](./skills/engineering/feature-uat/SKILL.md): generate business-facing UAT scenarios.
- [`autonomous-feature-executor`](./skills/engineering/autonomous-feature-executor/SKILL.md): orchestrate TDD executor and read-only validator subagents with HTML dashboard.
- [`feature-uat-runner`](./skills/engineering/feature-uat-runner/SKILL.md): guide user through UAT scenarios, mark confirmations, and restart TDD fix loops on failure.
- [`feature-wrap-up`](./skills/engineering/feature-wrap-up/SKILL.md): clean temporary dashboard files, summarize validation/UAT, and create a PR.

## Credits

Forked/adapted skills:

- [`caveman`](./skills/productivity/caveman/SKILL.md): forked from local skill at `/Users/bayma/.agents/skills/caveman/SKILL.md`, originally inspired by Matt Pocock's concise communication workflow.
- [`grill-with-docs`](./skills/engineering/grill-with-docs/SKILL.md): forked/adapted from Matt Pocock's [`grill-with-docs`](https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs).
- [`tdd`](./skills/engineering/tdd/SKILL.md): forked/adapted from Matt Pocock's [`tdd`](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd).
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
