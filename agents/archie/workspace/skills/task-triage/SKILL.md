---
name: task-triage
description: Capture and route a new task from chat into Notion. Use when someone drops a task, action item, or to-do in the channel.
---

# Task Triage

When a task, action item, or to-do is mentioned in chat, process it immediately without asking for information you can infer.

## Step 1 — Extract

Pull from the message:
- **Task name**: short, verb-first (e.g. "Confirm venue for June event")
- **Owner**: infer from TEAM.md ownership areas — one of Nolan, Adrian, Aiden, Bender, Sara, Karim, Nathan. If genuinely ambiguous, pick the most likely person and state your assumption.
- **Due date**: use what's stated. If none given, leave blank — do not ask.
- **Description**: any relevant context from the message (optional).

Never ask who owns what. Never ask for a Discord ID. It's all in TEAM.md.

## Step 2 — Write to Notion

Follow **notion.md** — it has the exact tool, property names, and field formats. In short: use
`API-post-page` to create a page in the Task Tracker DB (`c59f9f1e-ce90-8313-b022-0196cf2ec33b`) with:
- `Task name` (title)
- `Status` → `To do` (a **status**-type property: `{"status": {"name": "To do"}}`)
- `Owner` → the person's first name as a **select** (`{"select": {"name": "Adrian"}}`); omit if unassigned
- `Due date` (if provided)
- `Description` (if any)

Do **not** use the `Assignee`/`Person` people-fields — the team aren't Notion members. Then append
the new task to `/app/workspace/TASKS.json` (cache format in notion.md). Before creating, check the
cache for a near-duplicate by name — update instead of duplicating.

## Step 3 — Confirm in Discord

One short message. Example:
- "Added — <@695714324827734077> owns 'Confirm venue', due Friday."
- "Logged. Assigned to <@1282820043994038293> — no due date set."

Do not repeat the full task back. Do not ask for confirmation unless the owner is genuinely unclear.

## Edge Cases

- **Multiple tasks in one message**: process all of them, confirm in one message.
- **Task already exists**: check Notion first if the wording sounds familiar. Update rather than duplicate.
- **Owner truly ambiguous**: tag Nolan (<@712636536755060777>) in Discord with a one-liner: "Who's owning X?"
