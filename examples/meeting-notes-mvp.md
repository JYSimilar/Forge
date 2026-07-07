# Meeting Notes MVP Example

This example shows how Forge helps an ordinary user turn a vague idea into a first usable version, then into a bounded Safe Work Order.

## User Input

```text
I want to build a small tool that turns meeting notes into useful summaries.
I am not sure what the first version should include.
```

## Forge Output

### Goal

Build the smallest useful version of a meeting-notes tool that can turn pasted meeting text into a structured Markdown summary.

### MVP Scope

Do first:

- paste meeting text into one input;
- generate a short summary;
- extract action items, owners, and due dates when they are present;
- copy the result as Markdown.

Defer:

- login and accounts;
- team collaboration;
- audio transcription;
- calendar, Slack, or email integration;
- long-term storage.

### Safe Work Order

Goal:
Build a local single-page prototype for pasted meeting notes.

Required Context:

- current app framework or empty project choice;
- one sample meeting transcript;
- preferred output format.

Do Not Load:

- unrelated generated files;
- large design references;
- external API docs unless the user asks for integrations.

Limits:

- no account system;
- no backend unless the current project already has one;
- no external paid API without confirmation;
- stop after the first runnable prototype.

Acceptance Checks:

- user can paste sample meeting text;
- output includes summary and action items;
- action items include owner and due date when present in the input;
- result can be copied as Markdown;
- README explains how to run and verify the prototype.

Verification:

- run the app locally;
- paste the sample transcript;
- compare output against the acceptance checks;
- record any missing owner or due date as a known limitation.

Stop Condition:

- stop when the prototype runs and the first sample passes or fails with a clear reason.

Review Gate:

- summarize what was built;
- list verification evidence;
- name risks and limitations;
- offer 2-3 next options.

## Next Options

1. Build the local prototype first.
   This proves the core value with the lowest token and engineering cost.

2. Add sample data and README after the prototype works.
   This makes the project easier for another person or agent to verify.

3. Only then decide whether integrations are worth adding.
   This prevents the first version from becoming too large before the core workflow is proven.
