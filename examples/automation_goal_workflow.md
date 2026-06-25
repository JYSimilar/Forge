# Example: Controlled Automation Workflow

## User Input

```text
Forge: 我想自动完成这个目标，先给我几个可选路线，我选一个。
```

## Forge Should Do

1. Clarify the goal and stop conditions.
2. Offer options: fastest, stable, low-tech, extensible.
3. Ask the user to choose or add constraints if none fit.
4. Create a small task queue.
5. Execute or guide one small batch at a time.
6. Pause before destructive, external, paid, deployment, or submission actions.

## Optional Script

```bash
python scripts/automation_initializer.py /path/to/project
```

## Expected Output

- OPTION_SET.md
- AUTOMATION_PLAN.md
- TASK_QUEUE.md
- next batch with expected result and verification
