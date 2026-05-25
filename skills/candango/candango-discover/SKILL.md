---
name: candango-discover
description: Candango Discover. Thin Candango wrapper over Matt Pocock's grill-with-docs skill. Use when planning a feature, clarifying ambiguous requirements, preparing candango-plan, or when user wants relentless questions with feature-scoped documentation updates in docs/features using the feature slug.
---

# Candango Discover

Use `$grill-with-docs` as the questioning engine. Pass Candango's feature context path as the docs output target: `docs/features/<feature-slug>/context.md`

## Output

After final question, summarize:

- resolved domain terms
- updated `docs/features/<feature-slug>/context.md`
- business decisions
- technical decisions
- interface/design artifact decision
- UAT signals
- issue slicing implications
- open questions, if any
