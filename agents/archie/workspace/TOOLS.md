# Tools

Archie's environment-specific notes. Skills define how tools work — this file documents what's actually wired up.

## Notion MCP

Connected via `notion-mcp-server` (pre-installed in the Docker image).

**Task database ID:** `c59f9f1e-ce90-8313-b022-0196cf2ec33b`

Use this for all task operations:
- Query tasks by status, owner, or due date
- Create a new task when one surfaces in conversation
- Update task status (pending → in-progress → done → blocked)
- Assign tasks to team members by name (must match TEAM.md)

**Expense database ID:** to be added — see issue #1.

Query patterns to prefer:
- Batch reads: fetch all relevant tasks in one query, not one per task
- Filter by due date range when doing heartbeat checks
- Filter by assignee when someone asks "what's on my plate"

## Owner Commands (Discord DM only)

Nolan can send these via Discord DM. Run the command immediately, reply with one line confirming.

- `/new` — reset session context (keeps tokens lean)
- `/model [name]` — switch active model

## Channel

- Primary: private team accountability channel (scoped in config)
- DMs: any team member listed in TEAM.md
- Never post in the public community channel — that's Pulse's space
