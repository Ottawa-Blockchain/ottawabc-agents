# Tools

Archie's environment-specific notes. Skills define how tools work — this file documents what's actually wired up.

## Notion MCP

Connected via `notion-mcp-server` (pre-installed in the Docker image).

**All task operations — tools, property names, field formats, cache rules, output formats — live in
[`notion.md`](notion.md). Read it before touching Notion; don't guess.** The essentials:

- **Task DB:** Task Tracker — `c59f9f1e-ce90-8313-b022-0196cf2ec33b` (the only DB shared with the integration)
- **Statuses:** `To do`, `In progress`, `Blocked`, `Done`, `Cancelled` (a Notion **status** field)
- **Owner:** a **select** field (Nolan/Adrian/Aiden/Bender/Sara/Karim/Nathan) — *not* a people-field,
  because the team aren't paid Notion members. Owner → Discord mapping is in notion.md + TEAM.md.
- **List** with `API-post-search` (filter client-side); **create** with `API-post-page`; **update**
  with `API-patch-page`. Cache to `/app/workspace/TASKS.json` and read the cache, not Notion, except
  at the morning heartbeat or on an explicit refresh.

**Expense database:** not set up yet.

## Owner Commands (Discord DM only)

Nolan can send these via Discord DM. Run the command immediately, reply with one line confirming.

- `/new` — reset session context (keeps tokens lean)
- `/model [name]` — switch active model

## Channel

- Primary: private team accountability channel (scoped in config)
- DMs: any team member listed in TEAM.md
- Never post in the public community channel — that's Pulse's space
