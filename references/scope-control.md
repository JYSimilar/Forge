# Scope Control

Forge must protect the first version from becoming too large. Every MVP or prototype plan should include what not to do.

## Scope Buckets

Use these buckets when scoping:

| Bucket | Meaning |
|---|---|
| 第一版必须做 | Required for the smallest useful closed loop |
| 第一版可以顺手做 | Low-cost improvements if they do not delay the loop |
| 第一版明确不做 | Tempting but excluded from v0.1 |
| 后续再做 | Worth keeping on the roadmap; move valuable items to Idea Backlog when useful |
| 不建议做 | Adds risk/complexity without enough value |

## Common Things to Avoid in v0.1

- Full login system unless identity is the core feature.
- Full admin panel.
- Payment or subscription.
- Multi-device sync.
- Complex permissions.
- Microservices.
- Heavy dependency or framework changes.
- Perfect architecture.
- Full cross-platform support before the main loop works.
- Real hardware dependency when simulator/mock can validate value first.

## Scope Output Template

```text
第一版必须做：
- ...

第一版可以顺手做：
- ...

第一版明确不做：
- ...

后续再做 / 延后想法池：
- ...

不建议做：
- ...

为什么这样砍：...
```

## Idea Backlog Link

When a feature is excluded from v0.1 but still has plausible future value, do not simply discard it. Put it in `IDEA_BACKLOG.md` with:

- why it was deferred
- when to revisit it
- target version or stage
- priority, effort, risk, and status

Do not backlog ideas that are clearly harmful, misaligned, or unlikely to be useful. Put those under `不建议做` instead.

## Decision Rule

A feature belongs in v0.1 only if removing it breaks the first useful demo or validation path.
