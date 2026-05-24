# ADR Format

ADRs live in `docs/adr/` and use sequential numbering:

`0001-slug.md`, `0002-slug.md`, etc.

Create `docs/adr/` lazily, only when first ADR is needed.

## Template

```md
# {Short title of the decision}

{1-3 sentences: context, decision, why.}
```

Optional sections only when valuable:

- Status: `proposed | accepted | deprecated | superseded by ADR-NNNN`
- Considered Options
- Consequences

## When To Offer ADR

All must be true:

- hard to reverse
- surprising without context
- real trade-off

Skip easy, obvious, or no-alternative decisions.
