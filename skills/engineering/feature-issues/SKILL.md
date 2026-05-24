---
name: feature-issues
description: Convert a feature plan or technical spec into implementation issues, stories, tasks, and subtasks. Use when the user wants issues saved to GitHub Issues, Linear, Jira, or local markdown, with dependencies, acceptance criteria, AFK/HITL classification, and autonomous-execution-ready issue bodies. Always writes a local Markdown issue index under docs/features using the feature slug, even when also publishing to GitHub, Linear, Jira, or another tracker.
---

# Feature Issues

Break spec into independently executable vertical slices and publish them to chosen tracker.

All user-facing communication and written issue reports must use `$caveman`.

Hard rule: do not write `issues.md`, create tracker issues, or mutate any tracker until the user explicitly approves the proposed issue breakdown.

Candango role: work breakdown layer. Turns the blueprint into approved issue-sized units of construction.

## Inputs

Read:

- feature plan/spec
- design artifacts from `huashu-design` when interface scope exists
- `docs/agents/feature-issue-tracker.md`
- `docs/agents/feature-docs.md`
- relevant parent issue/epic/story
- `docs/features/<feature-slug>/context.md`
- root `CONTEXT.md` and ADRs as reference inputs

If tracker is ambiguous, ask user to choose GitHub, Linear, Jira, local markdown, or other.

## Workflow

### 1. Slice

Create tracer-bullet issues:

- thin end-to-end behavior
- demoable/verifiable alone
- clear dependencies
- explicit AFK/HITL type
- no horizontal "backend only" or "frontend only" issue unless truly independently valuable

### 2. Model Dependencies

Each issue must include:

- `blocked_by`
- `unblocks`
- `parent`
- dependency rationale

Use real tracker IDs after publishing.

### 3. Draft Issue Bodies

Use `references/issue-template.md`.

Every autonomous-ready issue needs:

- business context
- what to build
- acceptance criteria
- technical constraints
- validation expectations
- UAT references when available
- design artifact references when UI scope exists
- status initialized as `backlog`

### 4. Confirm

Show proposed breakdown before writing any file or publishing anything:

- title
- type AFK/HITL
- blocked by
- acceptance summary
- target tracker

Ask user to approve:

- issue list
- granularity
- dependencies
- AFK/HITL classification
- target tracker
- local Markdown output path

Stop here until the user explicitly approves. Do not create or edit `docs/features/<feature-slug>/issues.md` before approval.

### 5. Publish

Always write the local Markdown issue index first:

- path: `docs/features/<feature-slug>/issues.md`
- include every issue body using `references/issue-template.md`
- include tracker URL/ID for each issue after publish
- keep dependency links updated with real tracker IDs when available

Then use tracker config:

- **GitHub**: create issues with `gh issue create` or GitHub connector.
- **Linear**: use Linear connector when available; if unavailable, keep local Markdown as source of truth and tell user.
- **Jira**: use configured Jira workflow if available; if unavailable, keep local Markdown as source of truth and tell user.
- **Local markdown**: `docs/features/<feature-slug>/issues.md` is the source of truth.

Do not close or mutate parent issue unless user asks.
