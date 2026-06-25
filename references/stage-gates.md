# Stage Gates

Forge treats projects as stages, not as one undifferentiated task. Before recommending large work, identify the current stage and the next gate.

## Stage Map

| Stage | Goal | Must be true before moving on | Do not do yet | Common mistakes | Forge should output |
|---|---|---|---|---|---|
| idea | Clarify what should exist and why | Target user, pain, scenario, input, output, and success signal are clear | Code, architecture, tool debates | Building before knowing the user; making every idea equally important | 3 directions, assumptions, key questions, strongest direction |
| reference | Learn from existing projects, products, docs, and standards | Relevant references are found or search plan is explicit; evidence is separated from guesses | Copying code/UI blindly; choosing a dependency by popularity alone | No license check; trusting stale repos; copying commercial product details | Search keywords, candidate matrix, evidence, reusable lessons, risks |
| mvp | Reduce scope to the smallest closed loop | Must-do and explicit do-not-do lists are clear; first user path is defined | Login, payments, full admin, microservices, broad platform support unless essential | Making v0.1 too large; no validation path | MVP scope, first loop, not-do list, DoD |
| prototype | Make a runnable/demoable first version | It can run, show value, and be verified by a simple manual path | Big refactors, perfect architecture, heavy automation | Local-only paths; missing README; unclear mock/demo limits | Run steps, demo steps, quick tests, known limits |
| stabilize | Turn demo into a dependable project | Obvious bugs, config, errors, logs, tests, docs, and cleanup are being handled in small steps | New feature sprawl; full rewrite | Optimizing before fixing startup/config; no regression tests | Prioritized iteration plan and verification checklist |
| delivery | Prepare for another person/reviewer/user | Tests/checks run, docs updated, diff reviewed, known limits stated, handoff is clear | Submit with hidden risks or no run path | No commit/MR explanation; no fallback demo | Submit readiness verdict, MR text, handoff, DoD status |
| maintenance | Keep project understandable and extensible | Project state, decisions, changelog, risks, and next steps are maintained | Repeated ad-hoc patches without state update | Context loss; undocumented decisions; stale setup docs | PROJECT_STATE updates, decision log, backlog, retrospective |

## Gate Rules

- If the idea stage lacks user, pain, scenario, input, or output, use `clarify-first.md` before coding.
- If the task resembles an existing product, library, hardware workflow, API, or common feature, use Reference Scout before implementation.
- If MVP scope does not include a clear “do not do” list, use `scope-control.md`.
- If a task is claimed done but has no run/verify path, use `definition-of-done.md`.
- If the user only asks “下一步做什么”, use `route-selector.md`.

## Compact Output Template

```text
当前阶段：【idea/reference/mvp/prototype/stabilize/delivery/maintenance】
阶段目标：...
进入下一阶段前必须完成：...
暂时不建议做：...
下一步最小动作：...
```
