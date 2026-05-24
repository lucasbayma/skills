# Feature context.md Format

## Structure

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
{A one or two sentence description of the term}
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account
```

## Rules

- Be opinionated. Pick canonical term and list aliases to avoid.
- Flag conflicts explicitly in `Flagged ambiguities`.
- Keep definitions tight: one or two sentences.
- Define what term is, not implementation behavior.
- Show relationships and cardinality when obvious.
- Include only project-specific domain terms.
- Group under subheadings when natural.
- Add example dialogue when it clarifies boundaries.

## Location

Feature grill output lives at:

`docs/features/<feature-slug>/context.md`

Root `CONTEXT.md` and `CONTEXT-MAP.md` are inputs only unless the user explicitly asks to update global domain docs.

When multiple contexts exist, infer relevant source context and cite it in the feature context file. If unclear, ask.
