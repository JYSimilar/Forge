# Brainstorm To MVP

Use this when the user has a fuzzy idea, wants options, asks for naming, or needs a first version scoped.

## Brainstorm Everywhere

First diverge, then converge.

Brainstorming is allowed at every stage:

- Idea stage: users, scenarios, product angles, differentiators.
- MVP stage: different first-version scopes and non-goals.
- Architecture stage: technical routes, module boundaries, extension points.
- Implementation stage: smallest safe change paths.
- Testing stage: normal, error, boundary, compatibility, recovery cases.
- Interface stage: HTTP, gRPC, CLI, SDK, webhook, plugin, config, or local API.
- Documentation stage: user, developer, deployment, API caller, reviewer.
- Submit stage: reviewer questions, risk notes, rollback story.
- Iteration stage: feature, stability, performance, docs, compatibility, UX priorities.

If there is ambiguity or a meaningful choice, briefly brainstorm before acting. If the user says "直接做", "不要发散", or the task is mechanical, skip the brainstorm and execute.

## Brainstorm Pattern

For lightweight decisions, output:

1. Current problem
2. Three options
3. Recommended option
4. Reason
5. Risk and next step

For open-ended brainstorming, output:

1. Interpreted goal
2. Possible users and scenarios
3. Ten distinct directions
4. Three strongest directions
5. Minimum prototype for each
6. Main value and demo appeal
7. Main risk
8. Recommended direction
9. Lowest-cost validation step

## Idea Categories

Cover several types instead of repeating similar ideas:

- Low-cost quick demo
- Portfolio/showcase
- Engineering-skill practice
- AI-enhanced workflow
- Hardware, robotics, simulation, or device integration
- Product-experience value
- Long-term platform
- Commercial potential
- Unusual or memorable angle

## Scoring

When ranking ideas, score 1-5:

- User value
- Prototype speed
- Demo effect
- Technical fit
- Extensibility
- Differentiation
- Engineering training value
- Risk control

Classify the result as: most recommended, backup option, or not recommended now.

Use `scripts/idea_ranker.py ideas.csv` if the user provides structured CSV ideas.

## Deferred Ideas

When brainstorming produces useful but not-current ideas, separate them from rejected ideas.

- Selected idea -> MVP scope.
- Valuable but too early -> Idea Backlog.
- Harmful, low-value, or misaligned -> not recommended now.

For backlog candidates, include the idea, why it is deferred, when to revisit, possible target version, and main risk. Use `references/idea-backlog.md` and `assets/templates/IDEA_BACKLOG.md` for larger planning work.

## MVP Scope

Turn the selected idea into:

- Target user
- Core scenario
- One-sentence value
- Smallest closed loop
- First version must-haves
- First version non-goals
- Deferred ideas worth parking in Idea Backlog
- Mock, fake-data, simulator, or manual replacements
- Demo script
- Acceptance criteria
- Next iteration path

## Constructive Opposition

When asked to push back, or when the idea is too large, address:

- Is this a real need or a self-exciting idea?
- Why would users not use existing solutions?
- Is the first version too large?
- What data, device, account, approval, model, API, or integration might be unavailable?
- What is most likely to fail during a demo?
- What smaller experiment can validate the idea?

Be specific without being discouraging.

## Naming

Suggest short names that are easy to say, type, remember, and explain. Include meaning, fit, and possible issues.
