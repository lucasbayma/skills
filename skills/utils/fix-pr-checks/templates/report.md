<report_template>
Use this exact shape, adapted to current facts:

```markdown
Poll: <timestamp> | PR: <number/url> | Next: 60s

| Check | State | Cause | Fix | Verify |
|---|---|---|---|---|
| `<check>` | fail | <root cause> | <change made/planned> | `<cmd>` <pass/fail> |

Status: <pass/fail/pending/no checks>. <short next action>.
```

When no failures:

```markdown
Poll: <timestamp> | PR: <number/url>

| Check bucket | Count | Note |
|---|---:|---|
| pass | <n> | ok |
| pending | <n> | wait |
| fail | 0 | none |

Status: No fail. Next poll 60s.
```

When checks are not running:

```markdown
Poll: <timestamp> | PR: <number/url>

| Signal | Result |
|---|---|
| PR found | <yes/no> |
| checks found | no |
| likely reason | <workflow not triggered/no commits/no permission/provider unavailable> |

Status: No checks running.
```
</report_template>
