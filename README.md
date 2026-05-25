# Candango Skills

[![skills.sh](https://skills.sh/b/lucasbayma/skills)](https://skills.sh/lucasbayma/skills)

Candango is a set of skills for taking a feature from repo setup to UAT, with planning, specification, vertical issues, autonomous execution, TDD, external validation, and wrap-up.

## Usage

Install with `skills.sh`:

```bash
npx skills@latest add lucasbayma/skills
```

Select the recommended set:

- `candango-setup`
- `candango-caveman`
- `candango-discover`
- `candango-design`
- `candango-tdd`
- `candango-plan`
- `candango-spec`
- `candango-issues`
- `candango-uat`
- `candango-executor`
- `candango-uat-runner`
- `candango-wrap-up`

Run setup once in each target repo:

```text
Use $candango-setup to configure this repo for autonomous feature delivery.
```

Use the full flow when you want to deliver a feature end to end:

```text
Use $candango-discover to clarify this feature:

<feature request>

Then use $candango-plan, $candango-spec, $candango-issues, $candango-uat,
$candango-executor, $candango-uat-runner, and $candango-wrap-up.
All communication and reports must use $candango-caveman.
```

For a small feature that is already clear:

```text
Use $candango-plan to plan this small feature:

<feature request>

Then use $candango-spec, $candango-issues, $candango-uat, and
$candango-executor.
```

If the feature includes screens, flows, dashboards, apps, forms, or any visual surface, run `candango-design` before finalizing the plan, spec, and issues:

```text
Use $candango-design to locate the design system and coordinate UI work for this feature.
Target surface: local HTML prototype.
```

## Full Loop

### Development Cycle

![Full Candango development cycle](./docs/calango-development-cycle.svg)

### Executor Cycle

![Executor loop with TDD and external validation](./docs/executor-cycle.svg)

The key point: the executor that implements the work does not validate its own work. It writes code with TDD; another subagent, without the executor's conversation context and without permission to edit, reviews the diff against the spec, issue, and UAT. If validation fails, the main agent turns the report into another TDD round. Manual UAT and final repo validation happen only after that.

## Skills

### [`candango-setup`](./skills/candango/candango-setup/SKILL.md)

Configures the repo for the Candango flow. It discovers or asks which tracker to use, where feature docs live, which command validates the work, where to save the dashboard, how to handle design artifacts, and which rules agents must follow.

It creates local documentation so the other skills do not depend on conversation memory. Run it once per repo, and run it again only when changing tracker, docs convention, or validation process.

### [`candango-caveman`](./skills/candango/candango-caveman/SKILL.md)

Defines the flow's communication style: short, direct, no filler, while preserving technical substance. The goal is to reduce noise in plans, specs, issues, executor reports, validator reports, dashboard history, UAT, and PRs.

Use it when you want the whole cycle to produce high-signal responses and reports.

### [`candango-discover`](./skills/candango/candango-discover/SKILL.md)

Clarifies a feature before planning. It reads docs, ADRs, domain context, repo configs, and relevant code before asking questions. When it asks, it asks one question at a time, with a recommended answer.

Use it to resolve ambiguous terms, business rules, actors, permissions, happy paths, errors, contracts, UX, rollout, UAT, slicing, final validation, and autonomous-execution readiness. The result is enough feature context for the plan, spec, issues, and UAT.

### [`candango-design`](./skills/candango/candango-design/SKILL.md)

Runs when the feature has an interface: web screen, app, dashboard, admin panel, onboarding, checkout, settings, form, table, flow, or visual change. It locates the design system, coordinates UI work, and makes sure design artifacts are available before the plan and spec are finalized.

The recommended path is a local HTML prototype first, then porting into the real codebase. Generated artifacts become references for the plan, spec, issues, and visual UAT.

### [`candango-plan`](./skills/candango/candango-plan/SKILL.md)

Turns the request, context, and decisions into an implementation-ready plan. It records the problem, users, expected outcome, non-goals, constraints, risks, decisions, and vertical slices.

The skill classifies a feature as small, medium, or large. For each slice, it defines outcome, dependencies, acceptance signals, risk, and whether it can run AFK or needs HITL.

### [`candango-spec`](./skills/candango/candango-spec/SKILL.md)

Turns the approved plan into a technical specification. It describes architecture, contracts, data, permissions, errors, observability, test strategy, validation, and rollout.

The spec should let another agent implement without hidden context, let the validator review without inventing requirements, and let issues be created without becoming a horizontal list of layers.

### [`candango-issues`](./skills/candango/candango-issues/SKILL.md)

Breaks the plan and spec into vertical, executable issues. Each issue should be small enough to validate independently, but complete enough to deliver observable behavior.

It models dependencies, `blocked_by`, `unblocks`, parent, acceptance criteria, AFK/HITL type, validation expectations, and links to UAT/design when they exist. Before writing or publishing issues, it shows the proposed breakdown and waits for approval.

### [`candango-uat`](./skills/candango/candango-uat/SKILL.md)

Generates acceptance scenarios from business rules, the plan, spec, issues, and design artifacts. The focus is external behavior, not internal detail.

UATs use Given/When/Then, have priority, indicate whether they are automated, manual, or both, and point to which acceptance criteria they prove. During execution, the validator uses these UATs as the business oracle.

### [`candango-tdd`](./skills/candango/candango-tdd/SKILL.md)

The skill the executor uses to implement one issue at a time. The cycle is RED, GREEN, REFACTOR: one behavior test fails, the smallest implementation passes, and cleanup happens only while everything is green.

Tests should go through public interfaces, survive refactors, and verify real behavior. The executor output always includes the issue, implemented behavior, tests, changed files, commands, and risks.

### [`candango-executor`](./skills/candango/candango-executor/SKILL.md)

Orchestrates autonomous execution. The main agent picks unblocked issues, updates the dashboard, starts an executor with `candango-tdd`, starts an independent validator, decides whether to return to fixes, UAT, or done, and runs final validation.

The executor may edit code. The validator does not edit; it receives the diff, spec, issue, and UAT, but not the executor conversation. This forces external validation instead of self-approval.

### [`candango-uat-runner`](./skills/candango/candango-uat-runner/SKILL.md)

Runs manual or semi-automated UAT after implementation. It guides one scenario at a time, runs automated checks when possible, gives clear manual steps to the user, and records passed, failed, or blocked status.

When a UAT fails, it captures repro steps, expected behavior, actual behavior, evidence, and related context, then sends that package to `candango-executor` to restart the fix loop with TDD and validation.

### [`candango-wrap-up`](./skills/candango/candango-wrap-up/SKILL.md)

Finalizes the feature. It removes temporary dashboard files, verifies tests and final validation, checks UAT status, classifies the PR as feat, bugfix, or chore, prepares the commit, and creates the PR.

The PR should make clear what changed, why it changed, which UATs passed or remain pending, which commands validated the work, and whether temporary files were cleaned up.

## References and Credits

Candango combines original ideas with skills and patterns I used as a base:

- [`mattpocock/skills`](https://github.com/mattpocock/skills): the main reference for small composable skills, disciplined TDD, strong questions before implementation, local domain docs, and vertical issues.
- [`grill-with-docs`](https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs), by Matt Pocock: the base for stress-testing requirements against docs, ADRs, and domain language.
- [`tdd`](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd), by Matt Pocock: the base for the behavior-oriented RED/GREEN/REFACTOR cycle.
- [`huashu-design`](https://github.com/alchaincyf/huashu-design), by alchaincyf: the base for the HTML design skill, prototypes, screens, visual demos, and interface artifacts.
- `caveman`: adapted from a local ultra-compressed communication skill, inspired by the short-report style used in the skills ecosystem.

The rest of the Candango skills connect these pieces into a full cycle: repo setup, clarification, optional design, plan, spec, issues, UAT, autonomous execution, independent validation, guided UAT, and wrap-up.
