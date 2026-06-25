# Reference Scout: Open-source And Product Design Research

Use this when the user wants to find existing open-source projects, similar products, standard feature designs, implementation references, or when a new project would benefit from seeing how others solved the same problem before building.

Core rule: learn from references, then converge into the user's own MVP. Do not copy blindly. Do not stop at a list of links.

## When To Trigger

Trigger this workflow for requests such as:

- "有没有开源项目可以参考"
- "别人一般怎么做这个功能"
- "帮我找竞品"
- "这个产品怎么设计"
- "有没有现成方案"
- "参考 GitHub 项目"
- "先别写代码，先看看类似产品"
- "我想做一个类似 X 的工具"

Also use it lightly during MVP scoping, technology selection, API design, docs design, compatibility checks, and rewrite/refactor decisions when real-world references would reduce risk.

## Tool And Source Rule

If the environment has web/search tools, use them for current public information and cite sources in the final answer when required by the host system. If no search tool is available, produce search queries and a research checklist, then ask the user to paste candidate links or results.

Prefer sources in this order:

1. Official documentation and API docs
2. Active open-source repositories
3. Package registries: npm, PyPI, crates.io, Maven, Docker Hub, etc.
4. Product docs, help centers, changelogs, pricing pages, public demos
5. Issues, discussions, roadmap pages, release notes
6. Technical blogs and case studies
7. App/plugin marketplace listings and user reviews

Do not rely only on memory for freshness-sensitive details such as maintenance status, pricing, licenses, APIs, and product features.

## Open-source Research Flow

1. Define what kind of reference is needed:
   - full product
   - library/component
   - architecture example
   - API design
   - UI/UX flow
   - deployment example
   - docs example

2. Generate search queries:
   - Chinese product keywords
   - English product keywords
   - technical keywords
   - GitHub/package keywords
   - "awesome ..." and "open source ..." queries when useful

3. Screen candidates by:
   - maintenance: recent commits/releases
   - activity: stars/forks/issues/discussions are signals, not proof
   - docs: README, Quick Start, examples
   - demo: screenshots, live demo, sample data
   - install friction: can a normal user run it?
   - stack fit: does it match the user's current skills/project?
   - license: permissive, restrictive, unknown
   - extension fit: can it be adapted without fighting the design?
   - platform fit: Windows/macOS/Linux/Docker/device compatibility

4. Classify each candidate:
   - Direct use: can be used as-is
   - Wrapper: use it behind an adapter/API
   - Fork/reference: useful but needs modification
   - Learn only: good ideas but do not copy
   - Reject: poor fit, stale, risky license, or too complex

5. Converge into the user's project:
   - What to borrow
   - What not to borrow
   - What to mock in v0.1
   - What to build ourselves
   - What to defer
   - First runnable loop
   - Risks and validation steps

## License And Ethics

Always check license risk when referencing open-source code.

Simple guidance:

- MIT / Apache-2.0 / BSD: usually permissive, but preserve notices.
- GPL / AGPL: risky for closed-source/commercial distribution; do not casually copy.
- LGPL: depends on linking and distribution; be careful.
- No license: do not copy code. Treat as all rights reserved.
- Commercial product: learn product flow and concepts, but do not copy code, private APIs, assets, icons, branding, visual design, or paid content.

Allowed: learn concepts, architecture, public API style, documentation structure, feature prioritization, and UX flow.

Avoid: copying proprietary code, scraping protected services, bypassing auth/paywalls, cloning brand identity, or hiding license obligations.

## Product / Competitor Design Teardown

When analyzing existing products, decompose them by:

1. Target users
2. Core pain point
3. First-run experience
4. Main user path
5. Inputs and outputs
6. Core features
7. Nice-to-have features
8. Differentiators
9. Pricing or growth model when relevant
10. Docs/onboarding quality
11. API/integration surface
12. What is too complex for v0.1
13. What the user's MVP should copy as a pattern, not as proprietary implementation

Use a matrix when comparing several products.

## Output: Reference Scout Report

For open-source research, output:

1. Requirement understanding
2. Search keywords
3. Candidate projects/products
4. Candidate table: purpose, stack, maintenance, docs, license, fit, risk
5. Best reference and why
6. What to borrow
7. What not to borrow
8. Build / wrap / fork / learn-only decision
9. MVP plan based on references
10. Next verification steps

## Output: Product Design Teardown

For product/competitor design, output:

1. Product direction
2. Target user
3. Similar products
4. Feature matrix
5. Standard features
6. Features to cut from v0.1
7. Differentiation opportunities
8. Recommended first user path
9. Demo story
10. Iteration roadmap

## Common Calls

- `Forge: 先别写代码，先帮我找开源参考。`
- `Forge: 看看同类产品一般怎么设计这个功能。`
- `Forge: 帮我做竞品功能矩阵，然后收敛成 MVP。`
- `Forge: 这个功能有没有现成方案，能不能直接用？`
- `Forge: 帮我分析这些 GitHub 项目哪个最适合快速做原型。`
- `Forge: 参考已有产品，但不要照搬，帮我做自己的第一版。`

## Integration With Other Forge Abilities

- Brainstorm: use references to widen better options.
- MVP: cut from competitor feature sets into a first closed loop.
- Prototype: reuse mature components when license and complexity allow.
- Engineering: check dependency, license, maintenance, and compatibility risk.
- API/docs: borrow structure from high-quality public docs, not proprietary content.
- Diff review: flag copied code, unexplained dependencies, and license files missing when new open-source code is introduced.
