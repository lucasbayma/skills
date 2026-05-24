# CONTEXT.md Format

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

## Single vs Multi-Context

Single context: root `CONTEXT.md`.

Multi-context: root `CONTEXT-MAP.md` points to context-specific `CONTEXT.md` files.

When multiple contexts exist, infer relevant context. If unclear, ask.
