# Archie

Ambient accountability bot for the Ottawa Blockchain core team. Lives in a private Discord channel, lurks silently, and speaks up when it matters — task reminders, action item logging, weekly digests.

## What Archie Does

- **Lurks** in the private team channel and reads every message
- **Picks up tasks** when someone mentions a deliverable or deadline, logs it to Notion
- **Reminds** the team daily at 9 AM ET — nudges for due/overdue tasks, Monday digest
- **Responds to DMs** — team members can talk to Archie 1-on-1 for task status, creating tasks, or getting a rundown
- **Routes questions** to the right team member based on ownership areas
- **Escalates** ambiguous situations to Nolan via Discord DM rather than posting in channel

## Workspace Files

| File | Purpose |
|------|---------|
| `workspace/SOUL.md` | Identity, tone, lurking rules, task pickup, DM behaviour |
| `workspace/HEARTBEAT.md` | What Archie does on scheduled check-ins |
| `workspace/TEAM.md` | Team roster + Discord IDs + ownership areas *(local only — never commit)* |
| `workspace/MEMORY.md` | Learned context, auto-updated by Archie |
| `workspace/TOOLS.md` | Notion database IDs, owner commands |
| `workspace/notion.md` | Notion integration details |
| `workspace/skills/` | Self-built skills Archie creates over time |

## Configuration

### Environment variables

Copy `.env.example` to `.env` and fill in:

```bash
cp .env.example .env
```

| Variable | Where to get it |
|----------|----------------|
| `DISCORD_BOT_TOKEN` | discord.com/developers/applications → Bot → Token |
| `DISCORD_GUILD_ID` | Right-click server name → Copy Server ID |
| `DISCORD_CHANNEL_ID` | Right-click private channel → Copy Channel ID |
| `DISCORD_OWNER_ID` | Right-click your username → Copy User ID |
| `OPENAI_API_KEY` | platform.openai.com/api-keys |
| `ANTHROPIC_API_KEY` | console.anthropic.com/settings/keys |
| `OPENCLAW_GATEWAY_TOKEN` | Generate: `openssl rand -hex 24` |
| `NOTION_TOKEN` | notion.so/my-integrations → Internal Integration Secret |

### Team roster

Edit `workspace/TEAM.md` with real names and Discord user IDs. Format:

```
**Name** | <@DISCORD_USER_ID> | Role
Owns: area1, area2
```

Get a Discord user ID: Developer Mode on (Settings → Advanced) → right-click username → Copy User ID.

### Notion

Archie's task database ID is documented in `workspace/notion.md`. Make sure your Notion integration has access to that database (Share → Invite the integration).

## Cron Schedule

| Job | Schedule | What it does |
|-----|----------|-------------|
| `session-reset` | Daily 5 AM ET | Resets context to keep token usage lean |
| `daily-heartbeat` | Daily 9 AM ET | Checks Notion, nudges on due tasks; Monday = full digest |

Crons are seeded automatically on container startup. Edit `config/openclaw-crons.json` to change timing or messages.

## Verification Checklist

After `docker compose up --build archie`:

- [ ] Archie appears online in Discord server
- [ ] Archie responds when @mentioned in the private channel
- [ ] Archie responds to a Discord DM
- [ ] Logs show `[seed-crons] OK: daily-heartbeat`
- [ ] Post a message with an action item — Archie logs it to Notion and confirms
- [ ] `docker compose restart archie` — Archie comes back online without re-pairing

## Model

- **Primary:** `openai/gpt-5` (via Pi runtime)
- **Fallback:** `anthropic/claude-sonnet-4-6`
