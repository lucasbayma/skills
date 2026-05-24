#!/usr/bin/env python3
"""Render autonomous feature dashboard from JSON state."""

from __future__ import annotations

import argparse
import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATUSES = ["backlog", "in-progress", "validation", "uat", "done"]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "feature": {"title": "Untitled feature", "summary": ""},
            "issues": [],
            "events": [],
            "final_validation": {"command": "", "status": "pending", "summary": ""},
        }
    return json.loads(path.read_text())


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def issue_link(issue: dict[str, Any]) -> str:
    text = html.escape(issue.get("id", ""))
    url = issue.get("url")
    if url:
        return f'<a href="{html.escape(url)}">{text}</a>'
    return text


def render_tree(issues: list[dict[str, Any]]) -> str:
    by_blocker: dict[str, list[dict[str, Any]]] = {}
    blocked = set()
    for issue in issues:
        for dep in issue.get("blocked_by", []):
            by_blocker.setdefault(dep, []).append(issue)
            blocked.add(issue.get("id"))
    roots = [issue for issue in issues if issue.get("id") not in blocked]

    def node(issue: dict[str, Any]) -> str:
        children = by_blocker.get(issue.get("id"), [])
        child_html = "".join(node(child) for child in children)
        deps = ", ".join(html.escape(dep) for dep in issue.get("blocked_by", [])) or "none"
        body = (
            f"<span>{issue_link(issue)} {html.escape(issue.get('title', ''))}</span>"
            f"<small>{html.escape(issue.get('status', 'backlog'))} | deps: {deps}</small>"
        )
        if child_html:
            return f"<li>{body}<ul>{child_html}</ul></li>"
        return f"<li>{body}</li>"

    return "<ul class=\"tree\">" + "".join(node(root) for root in roots) + "</ul>"


def render_kanban(issues: list[dict[str, Any]]) -> str:
    columns = []
    for status in STATUSES:
        cards = []
        for issue in issues:
            if issue.get("status", "backlog") != status:
                continue
            cards.append(
                "<article class=\"card\">"
                f"<strong>{issue_link(issue)} {html.escape(issue.get('title', ''))}</strong>"
                f"<p>{html.escape(issue.get('summary', ''))}</p>"
                f"<small>{html.escape(issue.get('type', 'AFK'))}</small>"
                "</article>"
            )
        card_html = "".join(cards) or '<p class="empty">empty</p>'
        columns.append(f'<section class="column"><h3>{status}</h3>{card_html}</section>')
    return "<div class=\"kanban\">" + "".join(columns) + "</div>"


def render_events(events: list[dict[str, Any]]) -> str:
    rows = []
    for event in reversed(events[-80:]):
        rows.append(
            "<li>"
            f"<time>{html.escape(event.get('time', ''))}</time>"
            f"<b>{html.escape(event.get('actor', 'main'))}</b>"
            f"<span>{html.escape(event.get('issue_id', 'feature'))}</span>"
            f"<p>{html.escape(event.get('summary', ''))}</p>"
            "</li>"
        )
    return "<ol class=\"events\">" + "".join(rows) + "</ol>"


def render_html(state: dict[str, Any]) -> str:
    feature = state.get("feature", {})
    validation = state.get("final_validation", {})
    title = html.escape(feature.get("title", "Untitled feature"))
    summary = html.escape(feature.get("summary", ""))
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} - Autonomous Feature Dashboard</title>
  <style>
    :root {{ color-scheme: light; --ink:#18202a; --muted:#667085; --line:#d8dee8; --bg:#f6f8fb; --panel:#ffffff; --accent:#2764d8; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font:14px/1.45 ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color:var(--ink); background:var(--bg); }}
    header {{ padding:24px 28px 12px; background:var(--panel); border-bottom:1px solid var(--line); }}
    h1 {{ margin:0 0 6px; font-size:26px; letter-spacing:0; }}
    h2 {{ margin:28px 0 12px; font-size:18px; }}
    h3 {{ margin:0 0 12px; font-size:13px; text-transform:uppercase; letter-spacing:.04em; color:var(--muted); }}
    main {{ padding:0 28px 32px; }}
    a {{ color:var(--accent); text-decoration:none; }}
    .summary {{ color:var(--muted); max-width:900px; }}
    .panel {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:16px; }}
    .tree, .tree ul {{ list-style:none; padding-left:18px; }}
    .tree li {{ margin:10px 0; position:relative; }}
    .tree small {{ display:block; color:var(--muted); margin-top:2px; }}
    .kanban {{ display:grid; grid-template-columns:repeat(5, minmax(160px, 1fr)); gap:12px; align-items:start; }}
    .column {{ min-height:180px; background:#eef2f7; border:1px solid var(--line); border-radius:8px; padding:12px; }}
    .card {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:10px; margin-bottom:10px; }}
    .card p {{ margin:6px 0; color:var(--muted); }}
    .card small, .empty {{ color:var(--muted); }}
    .validation {{ display:grid; gap:4px; }}
    .events {{ list-style:none; padding:0; margin:0; }}
    .events li {{ display:grid; grid-template-columns:180px 90px 110px 1fr; gap:10px; padding:10px 0; border-bottom:1px solid var(--line); }}
    .events p {{ margin:0; }}
    time {{ color:var(--muted); }}
    @media (max-width: 900px) {{ .kanban {{ grid-template-columns:1fr; }} .events li {{ grid-template-columns:1fr; }} }}
  </style>
</head>
<body>
  <header>
    <h1>{title}</h1>
    <p class="summary">{summary}</p>
  </header>
  <main>
    <h2>Issue Tree</h2>
    <section class="panel">{render_tree(state.get("issues", []))}</section>
    <h2>Kanban</h2>
    {render_kanban(state.get("issues", []))}
    <h2>Final Validation</h2>
    <section class="panel validation">
      <strong>{html.escape(validation.get("status", "pending"))}</strong>
      <code>{html.escape(validation.get("command", ""))}</code>
      <span>{html.escape(validation.get("summary", ""))}</span>
    </section>
    <h2>Execution History</h2>
    <section class="panel">{render_events(state.get("events", []))}</section>
  </main>
</body>
</html>
"""


def parse_issue(raw: str) -> dict[str, Any]:
    parts = raw.split("|")
    while len(parts) < 7:
        parts.append("")
    issue_id, title, url, status, issue_type, blocked_by, summary = parts[:7]
    return {
        "id": issue_id,
        "title": title,
        "url": url,
        "status": status or "backlog",
        "type": issue_type or "AFK",
        "blocked_by": [item.strip() for item in blocked_by.split(",") if item.strip()],
        "summary": summary,
    }


def render_to_file(state: dict[str, Any], html_path: Path) -> None:
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(render_html(state))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--html", required=True, type=Path)
    sub = parser.add_subparsers(dest="action", required=True)

    init = sub.add_parser("init")
    init.add_argument("--title", required=True)
    init.add_argument("--summary", default="")
    init.add_argument("--validation-command", default="")
    init.add_argument("--issue", action="append", default=[], help="id|title|url|status|type|blocked_by_csv|summary")

    issue_cmd = sub.add_parser("issue")
    issue_cmd.add_argument("--id", required=True)
    issue_cmd.add_argument("--status", choices=STATUSES)
    issue_cmd.add_argument("--summary")

    event = sub.add_parser("event")
    event.add_argument("--issue-id", default="feature")
    event.add_argument("--actor", default="main")
    event.add_argument("--summary", required=True)

    validation = sub.add_parser("validation")
    validation.add_argument("--command", dest="validation_command")
    validation.add_argument("--status", default="pending")
    validation.add_argument("--summary", default="")

    sub.add_parser("render")

    args = parser.parse_args()
    state = load_state(args.state)

    if args.action == "init":
        state["feature"] = {"title": args.title, "summary": args.summary}
        state["issues"] = [parse_issue(raw) for raw in args.issue]
        state["events"] = state.get("events", [])
        state["final_validation"] = {
            "command": args.validation_command,
            "status": "pending",
            "summary": "",
        }
    elif args.action == "issue":
        for issue in state.get("issues", []):
            if issue.get("id") == args.id:
                if args.status:
                    issue["status"] = args.status
                if args.summary is not None:
                    issue["summary"] = args.summary
                break
    elif args.action == "event":
        state.setdefault("events", []).append(
            {
                "time": now(),
                "issue_id": args.issue_id,
                "actor": args.actor,
                "summary": args.summary,
            }
        )
    elif args.action == "validation":
        state["final_validation"] = {
            "command": args.validation_command or state.get("final_validation", {}).get("command", ""),
            "status": args.status,
            "summary": args.summary,
        }

    save_state(args.state, state)
    render_to_file(state, args.html)


if __name__ == "__main__":
    main()
