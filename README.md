# Candango Skills

[![skills.sh](https://skills.sh/b/lucasbayma/skills)](https://skills.sh/lucasbayma/skills)

Candango-branded skills for planning, specifying, slicing, validating, and executing features with agent subloops.

Inspired by `mattpocock/skills`: small composable skills, repo-local config in `docs/agents/`, vertical slices, TDD, explicit issue tracker, and domain docs.

## Quickstart

1. Run `$candango-setup` in the target repo.
2. Clarify ambiguous scope with `$candango-discover`.
3. If UI scope exists, create/edit screens with `$candango-design`.
4. Plan the feature with `$candango-plan`.
5. Write the technical spec with `$candango-spec`.
6. Create tracker issues with `$candango-issues`.
7. Generate UATs with `$candango-uat`.
8. Execute approved issues with `$candango-executor`.
9. Run guided UAT with `$candango-uat-runner`.
10. Wrap up and create PR with `$candango-wrap-up`.

## Usage

### Install With skills.sh

Install from GitHub:

```bash
npx skills@latest add lucasbayma/skills
```

Then select the skills you want in the installer.

Recommended install set:

- `candango-setup`
- `candango-caveman`
- `candango-discover`
- `candango-design`
- `candango-tdd`
- `candango-plan`
- `candango-spec`
- `candango-issues`
- `candango-uat`
- `candango-uat-runner`
- `candango-executor`
- `candango-wrap-up`

After installation, run `$candango-setup` once in each target repo.

### Manual Install / Link

Use this repo as a skills source for your agent, or copy/link the folders under `skills/` into the agent's skills directory.

Example local layout:

```text
skills/
└── candango/
    ├── candango-setup/
    ├── candango-caveman/
    ├── candango-discover/
    ├── candango-design/
    ├── candango-tdd/
    ├── candango-plan/
    ├── candango-spec/
    ├── candango-issues/
    ├── candango-uat/
    ├── candango-uat-runner/
    ├── candango-executor/
    └── candango-wrap-up/
```

### First Run In A Repo

Run setup once per target codebase:

```text
Use $candango-setup to configure this repo for autonomous feature delivery.
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
Use $candango-plan to plan this small feature: <feature request>.
Then use $candango-spec, $candango-issues, $candango-uat, and $candango-executor.
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

Use `candango-discover` first:

```text
Use $candango-discover to clarify this feature against repo docs and business rules: <feature request>.
```

Then:

```text
Use $candango-plan to turn the resolved decisions into a feature plan.
Use $candango-spec to write the technical spec.
Use $candango-issues to create vertical-slice issues.
Use $candango-uat to generate UATs.
Use $candango-executor to execute approved issues.
```

### Feature With UI

If `candango-discover` finds web/app/dashboard/forms/screens/flows/design-system scope, it asks:

```text
UI scope found. Create/edit layouts now? Where: Figma, local HTML prototype, existing codebase, screenshots, other? Recommended: local HTML prototype first, then port.
```

If yes:

```text
Use $candango-design to create UI screens/prototype for this feature in docs/features/<feature-slug>/design/.
```

Then link design artifacts from:

- `plan.md`
- `context.md`
- `technical-spec.md`
- issues
- `uat.md`

### Feature Without UI

Skip `candango-design`.

Record in plan/spec:

```text
Design artifacts skipped: no interface scope.
```

### Autonomous Execution

Run after issues/UAT/spec are ready:

```text
Use $candango-executor to execute the approved issues for docs/features/<feature-slug>/.
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
Use $candango-setup if this repo is not configured.
Use $candango-discover to clarify this feature:

<feature request>

If interface scope exists, ask whether to create/edit layouts and where.
Then use $candango-plan, $candango-spec, $candango-issues, $candango-uat, $candango-executor, $candango-uat-runner, and $candango-wrap-up.
All communication and reports must use $candango-caveman.
```

Plan only:

```text
Use $candango-plan to create docs/features/<feature-slug>/plan.md for:

<feature request>
```

Spec only:

```text
Use $candango-spec to create technical-spec.md from docs/features/<feature-slug>/plan.md.
```

Issues only:

```text
Use $candango-issues to create vertical-slice issues from docs/features/<feature-slug>/technical-spec.md.
Target tracker: <GitHub | Linear | Jira | local markdown>.
```

UAT only:

```text
Use $candango-uat to generate UATs from plan/spec/issues in docs/features/<feature-slug>/.
```

Run UAT:

```text
Use $candango-uat-runner to guide me through UATs from docs/features/<feature-slug>/uat.md.
```

Wrap up:

```text
Use $candango-wrap-up to clean temporary dashboard files and create a PR for docs/features/<feature-slug>/.
```

UI only:

```text
Use $candango-design to create/edit screens for docs/features/<feature-slug>/.
Target surface: <Figma | local HTML prototype | existing codebase | screenshots>.
```

## Communication Contract

All user-facing communication and written reports must use repo-local `$candango-caveman`.

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

All candango-specific docs and HTML live together:

`docs/features/<feature-slug>/`

Default contents:

- `plan.md`
- `technical-spec.md`
- `uat.md`
- `issues.md`
- `index.html` execution dashboard
- `state.json` execution state
- `design/` local UI/design artifacts

`index.html` and `state.json` are runtime dashboard files. `$candango-wrap-up` removes them before PR when they are not needed.

## Skills

- [`candango-setup`](./skills/candango/candango-setup/SKILL.md): configure issue tracker, feature folder layout, validation command, dashboard path, and subagent rules.
- [`candango-caveman`](./skills/candango/candango-caveman/SKILL.md): mandatory terse user-facing communication and reports.
- [`candango-discover`](./skills/candango/candango-discover/SKILL.md): stress-test feature plans against domain docs and write feature-scoped `context.md`.
- [`candango-design`](./skills/candango/candango-design/SKILL.md): create/review UI screens, layouts, and prototypes when feature scope includes an interface.
- [`candango-tdd`](./skills/candango/candango-tdd/SKILL.md): implement one issue at a time with red-green-refactor.
- [`candango-plan`](./skills/candango/candango-plan/SKILL.md): shape feature scope, decisions, risks, and delivery slices.
- [`candango-spec`](./skills/candango/candango-spec/SKILL.md): create technical spec from plan/context.
- [`candango-issues`](./skills/candango/candango-issues/SKILL.md): write `issues.md` and publish vertical-slice issues to GitHub, Linear, Jira, or local markdown.
- [`candango-uat`](./skills/candango/candango-uat/SKILL.md): generate business-facing UAT scenarios.
- [`candango-executor`](./skills/candango/candango-executor/SKILL.md): orchestrate TDD executor and read-only validator subagents with HTML dashboard.
- [`candango-uat-runner`](./skills/candango/candango-uat-runner/SKILL.md): guide user through UAT scenarios, mark confirmations, and restart TDD fix loops on failure.
- [`candango-wrap-up`](./skills/candango/candango-wrap-up/SKILL.md): clean temporary dashboard files, summarize validation/UAT, and create a PR.

## Credits

Forked/adapted skills:

- [`candango-caveman`](./skills/candango/candango-caveman/SKILL.md): forked/adapted from local skill at `/Users/bayma/.agents/skills/caveman/SKILL.md`, with inspiration from Matt Pocock's concise communication workflow.
- [`candango-discover`](./skills/candango/candango-discover/SKILL.md): forked/adapted from Matt Pocock's [`grill-with-docs`](https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs).
- [`candango-tdd`](./skills/candango/candango-tdd/SKILL.md): forked/adapted from Matt Pocock's [`tdd`](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd).
- [`candango-design`](./skills/candango/candango-design/SKILL.md): forked/adapted from local `huashu-design` at `/Users/bayma/.agents/skills/huashu-design/SKILL.md`, based on [`alchaincyf/huashu-design`](https://github.com/alchaincyf/huashu-design).

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
