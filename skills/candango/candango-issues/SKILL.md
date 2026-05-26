---
name: candango-issues
description: Candango Issues. Thin Candango wrapper over Matt Pocock's to-issues skill. Convert a feature plan into implementation issues, stories, tasks, and subtasks. Use when the user wants issues saved to GitHub Issues, Linear, Jira, or local markdown, with dependencies, acceptance criteria, AFK/HITL classification, and autonomous-execution-ready issue bodies. Always writes a local Markdown issue index under docs/features using the feature slug, even when also publishing to GitHub, Linear, Jira, or another tracker.
---

# Candango Issues

Use `$to-issues` as the issue-slicing engine.

Before use `$to-issues`, confirm with user the tracker (GitHub, Linear, Jira, or other), besides the markdown file

Then, convert each `$to-issues` issue to [issue-template.md](./references/issue-template.md) and store them in `docs/features/<feature-slug>/issues.md`.

Hard rule: do not write `issues.md`, create tracker issues, or mutate any tracker until the user explicitly approves the proposed issue breakdown.
