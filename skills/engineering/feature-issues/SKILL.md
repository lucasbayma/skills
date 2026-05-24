---
name: feature-issues
description: Convert a feature plan or technical spec into implementation issues, stories, tasks, and subtasks. Use when the user wants issues saved to GitHub Issues, Linear, Jira, or local markdown, with dependencies, acceptance criteria, AFK/HITL classification, and autonomous-execution-ready issue bodies.
---

# Feature Issues

Break spec into independently executable vertical slices and publish them to chosen tracker.

All user-facing communication and written issue reports must use `$caveman`.

## Inputs

Read:

- feature plan/spec
- design artifacts from `huashu-design` when interface scope exists
- `docs/agents/feature-issue-tracker.md`
- `docs/agents/feature-docs.md`
- relevant parent issue/epic/story
- `CONTEXT.md` and ADRs

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

Show proposed breakdown before publishing:

- title
- type AFK/HITL
- blocked by
- acceptance summary
- target tracker

Ask user to approve granularity and tracker.

### 5. Publish

Use tracker config:

- **GitHub**: create issues with `gh issue create` or GitHub connector.
- **Linear**: use Linear connector when available; otherwise write local drafts and tell user.
- **Jira**: use configured Jira workflow if available; otherwise write local drafts and tell user.
- **Local markdown**: write files under `docs/features/<feature-slug>/`.

Do not close or mutate parent issue unless user asks.
