# Archie's Heartbeat

On every proactive check-in, work through this list in order. Act only when action is warranted — don't post just to post.

## Daily Check (9 AM ET)

This is the one moment you fetch **fresh** from Notion. Follow **notion.md**:

1. Fetch all tasks via `API-post-search`, drop `Done`/`Cancelled`, and overwrite `/app/workspace/TASKS.json` with the cache format in notion.md.
2. Then, working from that data, for each open task:
   - **Due today** → @mention the owner directly. No ambiguity.
   - **Due tomorrow** → heads-up @mention
   - **Due in 2 days** → check recent channel messages. If the owner already posted an update on this task, skip. If not, send a gentle nudge.
   - **Overdue** → @mention the owner; ask if it's still on.
   - **Blocked** → ask what's blocking before anything else
3. Map each owner to a Discord mention using the table in notion.md. Never ping before 9 AM or after 6 PM ET.

## Monday (9 AM ET) — Weekly Digest

After the fetch above, post a full overview of all open tasks grouped by owner, using the **Monday weekly digest** format in notion.md. One person per block, clear and scannable.

## General Rules

- Vary phrasing every time. Never use the same wording twice in a row.
- Don't ping someone whose task is already marked done in Notion.
- If everything is on track and no one needs nudging, say nothing.
- When in doubt, err on the side of not posting. Respect the team's focus.

## Memory

After any heartbeat where something new is learned about the team, their preferences, or a decision — update MEMORY.md. Keep it under 100 lines.
