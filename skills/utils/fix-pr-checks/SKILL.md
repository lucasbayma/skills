---
name: fix-pr-checks
description: Monitors GitHub PR checks every 60 seconds, fixes failing checks, and reports failures and fixes in Caveman-style tables. Use when the user asks to watch, poll, repair, or summarize GitHub pull request checks.
---

<objective>
Monitor a GitHub pull request's checks on a 60-second polling loop, diagnose every failing or errored check, apply focused fixes, verify locally when possible, and report each poll in Caveman style using compact tables.

This skill is for active PR repair work. It keeps checking until checks pass, the user stops the run, no checks are running, or a blocker requires user input.
</objective>

<quick_start>
Use the current branch PR unless user gives PR number, URL, branch, or repo:

```bash
gh pr checks --json name,bucket,state,workflow,link,description,startedAt,completedAt
```

Poll manually every 60 seconds:

```bash
while true; do
  date
  gh pr checks "$PR" --json name,bucket,state,workflow,link,description,startedAt,completedAt
  sleep 60
done
```

For each poll, print Caveman table:

| Check | State | Failure | Fix | Verify |
|---|---|---|---|---|
| `ci/test` | fail | Jest snapshot drift | updated snapshot intent | `npm test` pass |

If no failures: `No fail. Checks pass/pending: <counts>. Next poll 60s.`
If no checks running: `No checks running. Reason: <not started/no workflow/no PR/no permissions>.`
</quick_start>

<workflow>
1. **Resolve target PR**
   - If user gives PR number, URL, branch, or `OWNER/REPO`, use it.
   - Otherwise run `gh pr view --json number,url,headRefName,baseRefName,state,isDraft` from current repo.
   - If no PR exists for current branch, report `No PR found for branch` and ask for PR target.

2. **Preflight**
   - Verify `gh auth status`.
   - Verify working tree with `git status --short`.
   - Preserve unrelated user changes. Do not revert files you did not change.
   - Identify package/test commands from repo conventions before fixing.

3. **Poll every 60 seconds**
   - Run `gh pr checks "$PR" --json name,bucket,state,workflow,link,description,startedAt,completedAt`.
   - Treat buckets as:
     - `fail` or `cancel`: must investigate and fix.
     - `pending`: wait and poll again unless logs show immediate failure details.
     - `pass`: record as passing.
     - `skipping`: report skipped, no fix unless required check blocked.
   - If command returns pending exit code, continue loop.
   - If command cannot find checks or PR has no check runs, report no checks running with likely reason.

4. **Investigate failures**
   - Prefer direct check logs from GitHub Actions:
     - Find run: `gh run list --branch "$(git branch --show-current)" --json databaseId,headSha,status,conclusion,workflowName,event,createdAt`
     - View logs: `gh run view <run-id> --log-failed`
   - For non-Actions checks, open/link provider details when available and summarize only actionable failure lines.
   - Map each failing check to root cause before editing.

5. **Fix one failure class at a time**
   - Make smallest repo-consistent code/test/config change.
   - Run local verification command that matches the failed check.
   - If multiple checks fail from same root cause, group them in report but verify affected commands.
   - Never commit, push, merge, rerun workflows, or force-push unless user asked. If user asked for full PR repair including push, push only after local verification.

6. **Print after each poll and after each fix**
   - Use Caveman: terse fragments, no filler, exact technical names.
   - Always use table for failures/fixes.
   - Include no-failure and no-running states explicitly.

7. **Continue or stop**
   - Continue polling every 60 seconds while checks are pending or failing and work remains possible.
   - Stop when all required checks pass, all checks pass, user stops, or a blocker needs human decision.
</workflow>

<templates>
For every poll/fix report, copy and fill `templates/report.md`.
</templates>

<safety_rules>
- Do not hide failing checks. If a check cannot be inspected, report `unknown` with the exact command/error.
- Do not claim fixed until local verification passes or remote rerun passes.
- Do not claim all checks pass while any required check is pending, failing, cancelled, or unknown.
- Do not overwrite unrelated local changes.
- Do not perform destructive git operations.
- Do not wait silently during polling; print current state before each 60-second wait.
</safety_rules>

<success_criteria>
This skill succeeds when:

- Target PR is identified or missing target is clearly reported.
- Checks are polled every 60 seconds while monitoring continues.
- Every failing check has cause, fix, and verification status in a Caveman-style table.
- No-failure polls explicitly say no failures.
- No-running checks explicitly say checks are not running and why if knowable.
- Work stops only when checks pass, user stops, or a blocker is clearly reported.
</success_criteria>
