---
name: check-pr-comments
description: Check PR Comments. Triage pull request comments and review threads from the current polling window, propose 2-3 fix or reply options, and wait for user direction before changing code, posting responses, or resolving threads. Use after a PR has review comments or when the user asks to check PR feedback.
---

<objective>
Triage feedback on an open pull request without losing the user's decision point. The skill gathers PR issue comments, review summaries, line comments, and review threads from one polling window; groups related feedback; then presents each actionable comment with 2-3 concrete options for fixing, replying, resolving, or deferring.

The first pass is advisory only. Do not edit files, resolve threads, dismiss reviews, or post replies until the user chooses how to proceed.
</objective>

<quick_start>
When invoked:

1. Identify the PR from the user-provided URL/number or the current branch.
2. Fetch comments, reviews, review comments, and unresolved review threads in one polling window.
3. Present a compact triage list with 2-3 suggestions per item.
4. Ask the user which suggestions to apply or how they want to respond.
5. After approval, implement selected code changes, reply with the solution made, and resolve review threads when supported.
</quick_start>

<essential_principles>
**One polling window:** Treat one triage pass as a snapshot. Record the fetch time and do not mix later comments into the same list unless the user asks to refresh.

**Advice before action:** The first output is a decision menu, not an implementation. Wait for the user's opinion before editing code, posting replies, marking threads resolved, or changing PR state.

**Comment fidelity:** Preserve reviewer intent. Quote only short snippets when needed, include author, location, link, and whether the comment is blocking, informational, or ambiguous.

**Actionable options:** Each item gets 2-3 practical suggestions. Prefer one direct fix, one lower-risk alternative, and one response/clarification path when appropriate.

**No silent posting:** Draft replies can be prepared after user approval, but posting GitHub comments requires explicit approval unless the user already asked to post.

**Reply before resolve:** When a selected fix addresses a review thread, reply with what changed and validation performed before resolving the thread. For top-level PR comments that cannot be resolved, post or draft an acknowledgement instead.
</essential_principles>

<workflow>
1. **Locate PR**
   - Use an explicit PR URL/number if provided.
   - Otherwise inspect the current branch and use the GitHub connector or `gh pr view`.
   - If more than one PR is plausible, ask one concise clarification question.

2. **Define polling window**
   - If the user specified a window, use it.
   - Otherwise use the current triage invocation as the window and include all currently visible unresolved review threads plus recent PR issue comments and reviews.
   - Capture the fetch timestamp in the response.

3. **Fetch PR feedback**
   - Prefer the GitHub connector when available.
   - With GitHub CLI, gather:
     - PR metadata: `gh pr view <pr> --json number,title,url,author,headRefName,baseRefName,reviewDecision,comments,reviews,latestReviews,files`
     - Review comments: `gh api repos/{owner}/{repo}/pulls/<number>/comments --paginate`
     - Review thread state via GraphQL when needed, especially unresolved threads.
   - Include top-level PR comments, review summaries, inline review comments, replies, and stale/resolved status when available.
   - Capture review thread node IDs when available so selected threads can be replied to and resolved later.

4. **Read local context**
   - Inspect the touched files and nearby code for each inline comment.
   - Check tests, issue context, feature docs, or UAT notes when they explain expected behavior.
   - Do not make edits during this step.

5. **Classify and group**
   - Merge duplicate comments that point to the same underlying change.
   - Classify each group as `fix`, `reply`, `clarify`, `defer`, or `non-actionable`.
   - Mark confidence as high, medium, or low.

6. **Present decision list**
   - For each actionable group, show:
     - `id`: stable short label such as `PRC-001`
     - `source`: author, file/line or thread, short link
     - `ask`: concise summary of reviewer request
     - `risk`: behavior, test, design, security, or maintainability impact
     - `suggestions`: 2-3 options with tradeoffs
     - `reply/resolution`: whether this can be replied to, resolved, both, or only acknowledged
     - `recommended`: one option and why
   - End by asking which IDs/options the user wants applied, replied to, or skipped.

7. **Act after user opinion**
   - Apply only the selected fixes or responses.
   - Keep code edits scoped to the approved comments.
   - Run focused validation relevant to changed files.
   - Write a concise reply for each addressed comment explaining:
     - what changed
     - where the fix landed
     - which validation passed or was not run
   - Show reply drafts before posting unless the user explicitly approved posting.
   - For review threads, after posting the solution reply, resolve the thread when the user approved resolution and validation supports the fix.
   - For top-level PR comments or review summaries that do not support resolution, reply with the solution and report that there is no resolvable thread.

8. **Reply and resolve mechanics**
   - Prefer the GitHub connector when it exposes reply and resolve actions.
   - With GitHub GraphQL, use `addPullRequestReviewThreadReply` to reply to a review thread and `resolveReviewThread` to mark it resolved.
   - Only resolve threads tied to selected IDs and only after the matching reply is posted or explicitly skipped by the user.

9. **Report completion**
   - Summarize applied fixes, drafted/posted replies, skipped items, and validation results.
   - List which review threads were resolved, which comments only received replies, and which IDs still need a decision.
</workflow>

<output_format>
Use this structure for the first triage pass:

```md
**PR Comment Triage**
Window: <timestamp/window>
PR: <number/title/link>

PRC-001 — <short title>
Source: <author>, <file:line or thread>, <link>
Ask: <reviewer request>
Risk: <impact>
Suggestions:
1. <direct fix>
2. <alternative fix or narrower change>
3. <reply/clarification/defer path>
Reply/resolution: <reply only | reply + resolve thread | no platform resolution available>
Recommended: <option> because <reason>

Decision needed: tell me which `PRC-*` options to apply, reply to, or skip.
```
</output_format>

<anti_patterns>
- Do not treat every comment as a required code change.
- Do not collapse distinct reviewer concerns into one vague task.
- Do not post "fixed" replies before validation.
- Do not refresh the polling window silently after presenting the triage list.
- Do not mark threads resolved unless the user explicitly approves, the fix or reply has been posted, validation is known, and the platform/tool supports it safely.
</anti_patterns>

<success_criteria>
The skill is successful when:

- PR comments and review threads are fetched from a clearly stated polling window
- Actionable comments are grouped without losing source links
- Each group has 2-3 concrete fix/reply suggestions
- The user is asked for a decision before edits or GitHub replies
- Approved follow-up work is scoped to selected comment IDs
- Addressed review threads receive a solution reply before being resolved
- Validation and remaining unresolved items are reported clearly
</success_criteria>
