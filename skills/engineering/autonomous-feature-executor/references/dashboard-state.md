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
      "summary": "Caveman report"
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
