# Dashboard State

`feature_dashboard.py` reads/writes JSON and renders HTML.

Save state and HTML inside same feature folder as docs:

- `docs/features/<feature-slug>/state.json`
- `docs/features/<feature-slug>/index.html`

## State Shape

```json
{
  "feature": {
    "title": "Feature name",
    "summary": "Caveman report"
  },
  "issues": [
    {
      "id": "ISSUE-1",
      "title": "Issue title",
      "url": "https://...",
      "status": "backlog",
      "type": "AFK",
      "blocked_by": [],
      "summary": "Caveman report",
      "execution_time": "12m"
    }
  ],
  "active_agents": [
    {
      "id": "executor-ISSUE-1",
      "role": "executor",
      "issue_id": "ISSUE-1",
      "session": "session-123",
      "status": "running",
      "started_at": "2026-05-24T12:00:00Z",
      "summary": "Implementing issue.",
      "output": "latest subagent output"
    }
  ],
  "events": [
    {
      "time": "2026-05-24T12:00:00Z",
      "issue_id": "ISSUE-1",
      "actor": "main",
      "summary": "Moved to validation. Executor done."
    }
  ],
  "final_validation": {
    "command": "npm test",
    "status": "pending",
    "summary": ""
  }
}
```

## Statuses

- backlog
- in-progress
- validation
- uat
- done

## Issue Runtime

Kanban cards show issue execution time. Prefer `execution_time` for a precomputed value such as `12m` or `1h 8m`. If omitted, the dashboard also accepts `duration`, `elapsed`, or `runtime`. When `started_at` and `finished_at` are present, it calculates the duration automatically.

## Auto Refresh

Rendered HTML refreshes itself every 10 seconds while the tab is visible. Collapsed/open state for toggle sections is kept in browser `localStorage`.

## Active Agents

Running subagent sessions can be shown in collapsible dashboard panels through `active_agents`. Each agent should have a stable `id`, plus optional `role`, `issue_id`, `session`, `status`, `started_at`, `summary`, and `output`.

Use `feature_dashboard.py agent --id <id> ...` to create or update a running session. Pass `--output` or `--output-file` to refresh the visible output, and `--append-output` to append instead of replacing. Use `feature_dashboard.py agent-remove --id <id>` when the subagent finishes. Agents with terminal statuses such as `done`, `complete`, `completed`, `finished`, or `stopped` are hidden from the rendered HTML.
