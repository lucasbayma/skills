# Repo Config Templates

## docs/agents/feature-issue-tracker.md

```markdown
# Feature Issue Tracker

Tracker: <GitHub Issues | Linear | Jira | local markdown | other>

Creation workflow:
- <exact command/tool/connector or local path>

Issue statuses:
- backlog
- in-progress
- validation
- uat
- done

Autonomous issue rules:
- AFK issues may be executed by subagents.
- HITL issues require user approval before implementation.
- Dependencies must be explicit in issue body.
- Repo-local `$candango-caveman` is mandatory for all user-facing communication and written reports.
- Repo-local `$candango-discover` resolves ambiguous feature terms/rules before planning/spec work.
```

## docs/agents/feature-docs.md

```markdown
# Feature Docs

Default feature docs path:

`docs/features/<feature-slug>/`

Files:
- `context.md` output from `$candango-discover`
- `plan.md`
- `technical-spec.md`
- `uat.md`
- `issues.md` always, even when issues are also published to GitHub, Linear, Jira, or another tracker
- `index.html` execution dashboard, removed by `$candango-wrap-up` before PR when not needed
- `state.json` execution state, removed by `$candango-wrap-up` before PR when not needed
- `design/` local UI/design artifacts

Rule:
- Keep all candango-specific docs and generated HTML in this folder.
- Keep `issues.md` updated with tracker IDs/URLs after publishing.

Use `docs/features/<feature-slug>/context.md` as the feature-scoped glossary/context created by `$candango-discover`. Root `CONTEXT.md` and ADRs are reference inputs unless the user explicitly asks to update global docs.
```

## docs/agents/feature-validation.md

```markdown
# Feature Validation

Final validation command:

`<command>`

Discovery rules:
- Prefer CI commands from `.github/workflows/`.
- Else use package/task runner scripts that match CI intent.
- Else ask user: "Is there any command you want me to run at the end of feature development?"

Feature is complete only when selected issues are done and final command passes, unless user accepts risk.
```

## docs/agents/feature-design.md

```markdown
# Feature Design

When business definition includes interface scope, ask:

`UI scope found. Create/edit layouts now? Where: Figma, local HTML prototype, existing codebase, screenshots, other? Recommended: local HTML prototype first, then port.`

Design surfaces:
- Figma
- local HTML prototype
- existing codebase
- screenshots
- other

Default local prototype path:

`docs/features/<feature-slug>/design/`

Rules:
- Use `$candango-design` to find the repo design system and coordinate UI screens, layouts, flows, prototypes, and design review.
- Link design artifacts from plan, spec, issues, and UAT.
- If user skips design work, record `Design artifacts skipped by user`.
- Keep local design HTML and assets inside `docs/features/<feature-slug>/design/`.
```

## docs/agents/autonomous-feature-execution.md

```markdown
# Autonomous Feature Execution

Dashboard:
- state: `docs/features/<feature-slug>/state.json`
- html: `docs/features/<feature-slug>/index.html`
- folder: `docs/features/<feature-slug>/`

Roles:
- Main agent: orchestrates, updates dashboard, runs final validation.
- Executor subagent: implements issue with repo-local `$candango-tdd`, may edit files.
- Validator subagent: validates diff against issue/spec/UAT, must not edit files.
- UAT runner: guides user through manual UATs, marks checked scenarios, and restarts TDD fix loops on failure.
- Feature wrap-up: removes runtime dashboard files and creates PR with UAT/validation status.
- Caveman skill: compresses all user-facing communication and reports.
- Grill-with-docs skill: clarifies feature decisions and updates domain docs before execution.
- Candango-design skill: finds design-system context and coordinates UI work when interface scope exists.
- TDD skill: red-green-refactor execution for one issue at a time.

Communication:
- All user-facing messages and reports must use `$candango-caveman`.

Polling:
- Health-check active subagents every 1 minute when tooling supports it.

Status model:
- backlog
- in-progress
- validation
- uat
- done
```
