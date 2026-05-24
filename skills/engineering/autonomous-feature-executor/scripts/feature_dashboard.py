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
AUTO_REFRESH_SECONDS = 10


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_time(value: str) -> datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def format_duration(seconds: float) -> str:
    total = max(0, int(seconds))
    days, remainder = divmod(total, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if not parts and seconds:
        parts.append(f"{seconds}s")
    return " ".join(parts) or "0s"


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


def svg_issue_link(issue: dict[str, Any], content: str) -> str:
    url = issue.get("url")
    if url:
        return f'<a href="{html.escape(url)}">{content}</a>'
    return content


def truncate(text: str, length: int) -> str:
    if len(text) <= length:
        return text
    return text[: max(0, length - 3)].rstrip() + "..."


def status_class(status: str) -> str:
    safe = "".join(char if char.isalnum() else "-" for char in status.lower()).strip("-")
    return safe or "backlog"


def issue_execution_time(issue: dict[str, Any]) -> str:
    for key in ("execution_time", "runtime", "duration", "elapsed"):
        value = issue.get(key)
        if value:
            return str(value)

    started = parse_time(issue.get("started_at", ""))
    finished = parse_time(issue.get("finished_at", "") or issue.get("ended_at", ""))
    if started and finished:
        return format_duration((finished - started).total_seconds())
    if started:
        elapsed = datetime.now(timezone.utc) - started
        return f"running {format_duration(elapsed.total_seconds())}"
    return "not recorded"


def render_tree(issues: list[dict[str, Any]]) -> str:
    issue_by_id = {}
    issue_ids = []
    for issue in issues:
        issue_id = issue.get("id")
        if issue_id and issue_id not in issue_by_id:
            issue_by_id[issue_id] = issue
            issue_ids.append(issue_id)
    if not issue_ids:
        return '<p class="empty">empty</p>'

    children_by_dep: dict[str, list[str]] = {issue_id: [] for issue_id in issue_ids}
    indegree: dict[str, int] = {issue_id: 0 for issue_id in issue_ids}
    edges: list[tuple[str, str]] = []
    unknown_deps: dict[str, list[str]] = {}

    for issue in issues:
        issue_id = issue.get("id")
        if not issue_id:
            continue
        for dep in issue.get("blocked_by", []):
            if dep == issue_id:
                continue
            if dep not in issue_by_id:
                unknown_deps.setdefault(issue_id, []).append(dep)
                continue
            edge = (dep, issue_id)
            if edge in edges:
                continue
            edges.append(edge)
            children_by_dep.setdefault(dep, []).append(issue_id)
            indegree[issue_id] += 1

    order = {issue_id: index for index, issue_id in enumerate(issue_ids)}
    queue = [issue_id for issue_id in issue_ids if indegree[issue_id] == 0]
    depth = {issue_id: 0 for issue_id in queue}
    seen: list[str] = []
    remaining_indegree = dict(indegree)

    while queue:
        issue_id = queue.pop(0)
        seen.append(issue_id)
        for child_id in children_by_dep.get(issue_id, []):
            depth[child_id] = max(depth.get(child_id, 0), depth.get(issue_id, 0) + 1)
            remaining_indegree[child_id] -= 1
            if remaining_indegree[child_id] == 0:
                queue.append(child_id)

    cycle_ids = [issue_id for issue_id in issue_ids if issue_id not in seen]
    if cycle_ids:
        cycle_depth = (max(depth.values()) + 1) if depth else 0
        for issue_id in cycle_ids:
            depth.setdefault(issue_id, cycle_depth)

    layers: dict[int, list[str]] = {}
    for issue_id in issue_ids:
        layers.setdefault(depth.get(issue_id, 0), []).append(issue_id)
    for layer in layers.values():
        layer.sort(key=lambda issue_id: order[issue_id])

    node_w = 210
    node_h = 72
    gap_x = 76
    gap_y = 88
    margin = 36
    layer_indexes = sorted(layers)
    max_layer_size = max(len(layer) for layer in layers.values())
    graph_w = max(720, (margin * 2) + (max_layer_size * node_w) + ((max_layer_size - 1) * gap_x))
    graph_h = (margin * 2) + (len(layer_indexes) * node_h) + ((len(layer_indexes) - 1) * gap_y)

    positions: dict[str, tuple[int, int]] = {}
    for visual_layer, layer_index in enumerate(layer_indexes):
        layer = layers[layer_index]
        layer_w = (len(layer) * node_w) + ((len(layer) - 1) * gap_x)
        x = (graph_w - layer_w) // 2
        y = margin + visual_layer * (node_h + gap_y)
        for issue_id in layer:
            positions[issue_id] = (x, y)
            x += node_w + gap_x

    edge_html = []
    for dep_id, issue_id in edges:
        if dep_id not in positions or issue_id not in positions:
            continue
        dep_x, dep_y = positions[dep_id]
        issue_x, issue_y = positions[issue_id]
        start_x = dep_x + node_w // 2
        start_y = dep_y + node_h
        end_x = issue_x + node_w // 2
        end_y = issue_y
        mid_y = start_y + ((end_y - start_y) // 2)
        edge_html.append(
            '<path class="graph-edge" '
            f'd="M {start_x} {start_y} C {start_x} {mid_y}, {end_x} {mid_y}, {end_x} {end_y}" />'
        )

    node_html = []
    for issue_id in issue_ids:
        issue = issue_by_id[issue_id]
        x, y = positions[issue_id]
        status = issue.get("status", "backlog")
        title = truncate(issue.get("title", ""), 30)
        content = (
            f'<g class="graph-node status-{status_class(status)}" transform="translate({x} {y})">'
            f"<title>{html.escape(issue_id)} - {html.escape(issue.get('title', ''))}</title>"
            f'<rect width="{node_w}" height="{node_h}" rx="8" />'
            f'<text class="node-id" x="{node_w // 2}" y="25" text-anchor="middle">{html.escape(issue_id)}</text>'
            f'<text class="node-title" x="{node_w // 2}" y="45" text-anchor="middle">{html.escape(title)}</text>'
            f'<text class="node-status" x="{node_w // 2}" y="61" text-anchor="middle">{html.escape(status)}</text>'
            "</g>"
        )
        node_html.append(svg_issue_link(issue, content))

    notes = []
    if unknown_deps:
        missing = "; ".join(
            f"{html.escape(issue_id)}: {', '.join(html.escape(dep) for dep in deps)}"
            for issue_id, deps in unknown_deps.items()
        )
        notes.append(f'<p class="graph-note">Missing dependency nodes: {missing}</p>')
    if cycle_ids:
        notes.append(
            '<p class="graph-note warning">'
            f"Dependency cycle detected around: {', '.join(html.escape(issue_id) for issue_id in cycle_ids)}"
            "</p>"
        )

    return (
        '<div class="issue-graph">'
        f'<svg viewBox="0 0 {graph_w} {graph_h}" role="img" aria-label="Issue dependency graph">'
        "<defs>"
        '<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M 0 0 L 10 5 L 0 10 z" />'
        "</marker>"
        "</defs>"
        '<g class="graph-edges">'
        + "".join(edge_html)
        + "</g>"
        '<g class="graph-nodes">'
        + "".join(node_html)
        + "</g>"
        "</svg>"
        + "".join(notes)
        + "</div>"
    )


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
                '<div class="card-meta">'
                f"<small>{html.escape(issue.get('type', 'AFK'))}</small>"
                f"<small>runtime: {html.escape(issue_execution_time(issue))}</small>"
                "</div>"
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
    auto_refresh_ms = AUTO_REFRESH_SECONDS * 1000
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
    .issue-graph {{ width:100%; overflow:auto; padding:8px; }}
    .issue-graph svg {{ display:block; min-width:680px; width:100%; height:auto; }}
    .issue-graph marker path {{ fill:#344054; }}
    .graph-edge {{ fill:none; stroke:#344054; stroke-width:2.3; stroke-linecap:round; marker-end:url(#arrow); opacity:.86; }}
    .graph-edge:hover {{ stroke:var(--accent); opacity:1; }}
    .graph-node rect {{ fill:#fff; stroke:#98a2b3; stroke-width:1.4; filter:drop-shadow(0 3px 5px rgba(24,32,42,.08)); }}
    .graph-node .node-id {{ font-size:15px; font-weight:800; fill:var(--ink); }}
    .graph-node .node-title {{ font-size:11px; fill:#344054; }}
    .graph-node .node-status {{ font-size:10px; text-transform:uppercase; fill:var(--muted); }}
    .graph-node.status-done rect {{ fill:#ecfdf3; stroke:#75c486; }}
    .graph-node.status-in-progress rect {{ fill:#fff7e6; stroke:#f2b650; }}
    .graph-node.status-validation rect {{ fill:#eff8ff; stroke:#65a9e8; }}
    .graph-node.status-uat rect {{ fill:#fdf2fa; stroke:#df84bd; }}
    .graph-note {{ margin:8px 0 0; color:var(--muted); font-size:12px; }}
    .graph-note.warning {{ color:#b42318; }}
    .kanban {{ display:grid; grid-template-columns:repeat(5, minmax(160px, 1fr)); gap:12px; align-items:start; }}
    .column {{ min-height:180px; background:#eef2f7; border:1px solid var(--line); border-radius:8px; padding:12px; }}
    .card {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:10px; margin-bottom:10px; }}
    .card p {{ margin:6px 0; color:var(--muted); }}
    .card-meta {{ display:flex; flex-wrap:wrap; gap:6px 10px; margin-top:8px; }}
    .card small, .empty {{ color:var(--muted); }}
    .toggle-section {{ margin-top:28px; }}
    .toggle-section summary {{ display:flex; align-items:center; gap:8px; width:max-content; cursor:pointer; color:var(--ink); }}
    .toggle-section summary::-webkit-details-marker {{ display:none; }}
    .toggle-section summary::marker {{ content:""; }}
    .toggle-section summary::before {{ content:""; width:0; height:0; border-top:5px solid transparent; border-bottom:5px solid transparent; border-left:7px solid var(--muted); transform:rotate(0deg); transition:transform .12s ease; }}
    .toggle-section[open] summary::before {{ transform:rotate(90deg); }}
    .toggle-section summary h2 {{ margin:0; }}
    .toggle-section .panel {{ margin-top:12px; }}
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
    <h2>Kanban</h2>
    {render_kanban(state.get("issues", []))}
    <details class="toggle-section" open>
      <summary><h2>Issue Tree</h2></summary>
      <section class="panel">{render_tree(state.get("issues", []))}</section>
    </details>
    <h2>Final Validation</h2>
    <section class="panel validation">
      <strong>{html.escape(validation.get("status", "pending"))}</strong>
      <code>{html.escape(validation.get("command", ""))}</code>
      <span>{html.escape(validation.get("summary", ""))}</span>
    </section>
    <details class="toggle-section" open>
      <summary><h2>Execution History</h2></summary>
      <section class="panel">{render_events(state.get("events", []))}</section>
    </details>
  </main>
  <script>
    const refreshDelay = {auto_refresh_ms};
    document.querySelectorAll(".toggle-section").forEach((section, index) => {{
      const key = `dashboard-toggle-${{index}}`;
      const saved = localStorage.getItem(key);
      if (saved === "open") section.open = true;
      if (saved === "closed") section.open = false;
      section.addEventListener("toggle", () => {{
        localStorage.setItem(key, section.open ? "open" : "closed");
      }});
    }});
    window.setInterval(() => {{
      if (document.visibilityState === "visible") {{
        window.location.reload();
      }}
    }}, refreshDelay);
  </script>
</body>
</html>
"""


def parse_issue(raw: str) -> dict[str, Any]:
    parts = raw.split("|")
    while len(parts) < 8:
        parts.append("")
    issue_id, title, url, status, issue_type, blocked_by, summary, execution_time = parts[:8]
    issue = {
        "id": issue_id,
        "title": title,
        "url": url,
        "status": status or "backlog",
        "type": issue_type or "AFK",
        "blocked_by": [item.strip() for item in blocked_by.split(",") if item.strip()],
        "summary": summary,
    }
    if execution_time:
        issue["execution_time"] = execution_time
    return issue


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
    init.add_argument(
        "--issue",
        action="append",
        default=[],
        help="id|title|url|status|type|blocked_by_csv|summary|execution_time",
    )

    issue_cmd = sub.add_parser("issue")
    issue_cmd.add_argument("--id", required=True)
    issue_cmd.add_argument("--status", choices=STATUSES)
    issue_cmd.add_argument("--summary")
    issue_cmd.add_argument("--execution-time")
    issue_cmd.add_argument("--started-at")
    issue_cmd.add_argument("--finished-at")

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
                if args.execution_time is not None:
                    issue["execution_time"] = args.execution_time
                if args.started_at is not None:
                    issue["started_at"] = args.started_at
                if args.finished_at is not None:
                    issue["finished_at"] = args.finished_at
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
