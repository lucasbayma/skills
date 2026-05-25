---
name: candango-design
description: Candango Design. Use for UI, layout, screen, flow, design artifact, design system, component, styling, or visual polish work. Read candango-setup design config first. Find and reuse the repo design system. Delegate execution to an existing UI/design skill. If no design system is found, ask where it is or whether it exists. If it does not exist, run candango-discover only for design-system questions.
---

# Candango Design

Start from repo. Reuse design system. No blank-canvas UI.

Use `$caveman` for user-facing text when configured.

## Workflow

1. Read `$candango-setup` config:
   `docs/agents/feature-design.md` first; then `docs/agents/feature-docs.md`, `AGENTS.md`, `CLAUDE.md`.

2. Use configured work location:
   - Product UI -> existing app/codebase.
   - Artifacts -> `docs/features/<feature-slug>/design/`.
   - Figma/screenshots/other -> only if configured/requested.
   - No config -> default artifacts path above; report missing setup config.
   - Still unclear -> ask: `Where should design work live? Recommended: existing codebase for real UI; docs/features/<feature-slug>/design/ for artifacts.`

3. Find design system before designing:
   - Search paths: `packages/ui`, `src/components`, `app/components`, `components`, `ui`, `design-system`, `theme`, `tokens`, `styles`, `storybook`, `tailwind.config.*`, CSS vars, nearby component examples.
   - Check `package.json`: local UI packages, Storybook, Tailwind, shadcn/ui, Radix, MUI, Chakra, Mantine, Ant Design, CSS modules, styled-components, Emotion, vanilla-extract.
   - Read nearby screens with same component family.

4. If found: name exact files/components/tokens. Reuse components, tokens, spacing, type, colors, states, layout. Add new pieces only when no local pattern fits.

5. If missing: ask where it lives or whether it exists. If exists, wait for path/package/Figma/screenshots/access. If absent, run `$candango-discover` design-system-only: component source, tokens, type, color, spacing, radius, elevation, breakpoints, states, accessibility baseline, artifact/code location. No business, rollout, tracker, slicing.

6. Delegate:
   - Repo-named UI skill -> use it.
   - Web/app/product UI -> `$frontend-design`.
   - Interaction polish -> `$make-interfaces-feel-better`.
   - Accessibility/WCAG -> `$accessibility`.
   - Local frontend changed -> browser verify when target exists.

This skill coordinates discovery/place. It does not replace detailed UI skills.

## Output

Report: config + path; design-system refs; execution skill; files/artifacts changed; verification done/needed.
