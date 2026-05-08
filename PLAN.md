# Archie — Ottawa Blockchain Accountability Bot (OpenClaw)

## Context

Archie is the Ottawa Blockchain team's Discord accountability bot. It manages action items for a 5–10 person team in a private Discord server channel — posting smart reminders based on due dates, learning from conversations, and routing questions to the right team member. Built on OpenClaw (same framework as Julia and Simon), deployed on a **dedicated VPS separate from Julia/Simon's VPS**, with the `ottawabc-bot` GitHub repo as the workspace config source of truth.

This plan is written for a fresh Claude session on the new VPS. Clone the repo, read this file, and execute in order.

---

## Architecture

**OpenClaw on dedicated VPS + Discord channel**

- OpenClaw handles: heartbeat, memory, cron jobs, proactive posting, tool use, auto-learning
- Discord channel: OpenClaw connects to the Ottawa Blockchain private server channel
- @mentions: Archie composes `<@DISCORD_USER_ID>` in message text — IDs stored in `workspace/TEAM.md`
- Tasks: `tasks.json` locally until Notion is connected
- Workspace config is version-controlled in this repo

**Why a separate VPS:**
- Keeps Ottawa Blockchain infrastructure isolated from Nolan's personal agents (Julia, Simon)
- Cleaner security boundary — Ottawa Blockchain team may eventually need access
- Follows containerization principle: one agent, one environment

---

## Repo Structure (this repo)

```
ottawabc-bot/
├── PLAN.md                    ← this file — read first on new VPS
├── README.md                  ← setup steps
├── workspace/
│   ├── SOUL.md                ← Archie's identity, tone, routing rules
│   ├── MEMORY.md              ← auto-updated by Archie as he learns
│   ├── HEARTBEAT.md           ← proactive behavior checklist
│   └── TEAM.md                ← team roster + Discord IDs + ownership
├── tasks.json                 ← action items (Notion stub — replace later)
├── config/
│   └── openclaw.json          ← sanitized OpenClaw config (no secrets)
├── .env.example               ← required environment variables
└── archive/                   ← original discord.py implementation (reference only)
```

---

## New VPS Setup — Step by Step

### Phase 0 — Provision the VPS

- Provider: DigitalOcean (or equivalent)
- Size: Basic, 1 GB RAM minimum (same tier as Julia's VPS)
- OS: Ubuntu 22.04 LTS
- Region: Toronto or closest to Ottawa
- SSH key: add Nolan's key during provisioning

### Phase 1 — Base Setup on VPS

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Node (22.x)
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify
node --version   # should be 22.x+
npm --version
```

### Phase 2 — Install OpenClaw

```bash
npm install -g openclaw@latest
openclaw --version
```

### Phase 3 — Clone This Repo

```bash
git clone https://github.com/nolandruid/ottawabc-bot.git
cd ottawabc-bot
```

### Phase 4 — Run OpenClaw Onboard

```bash
openclaw onboard --install-daemon
```

Wizard prompts:
1. Provider → **Anthropic**
2. API key → paste `ANTHROPIC_API_KEY`
3. Channel → **Discord**
4. Discord bot token → paste `DISCORD_BOT_TOKEN`
5. Server/channel → select the Ottawa Blockchain private accountability channel

### Phase 5 — Set Up Workspace

```bash
# Symlink this repo as the OpenClaw workspace (same pattern as Julia)
mv ~/.openclaw/workspace ~/.openclaw/workspace.bak
ln -s ~/ottawabc-bot/workspace ~/.openclaw/workspace
openclaw gateway restart
```

### Phase 6 — Verify

```bash
openclaw gateway status
openclaw logs
```

Post a test message in the Discord accountability channel. Archie should respond.

---

## Workspace Files

### `workspace/SOUL.md`
Archie's identity — loaded every session. Defines tone, routing rules, accountability behavior.

### `workspace/MEMORY.md`
Starts empty. Archie writes to this when he learns something worth keeping:
- Team preferences (e.g. "team prefers nudges Thursday not Tuesday")
- Decisions made in channel (e.g. "June meetup moved to the 18th")
- Context shifts (e.g. "Nolan is handling venue while usual person is away")
- Keep under 100 lines, curate ruthlessly

### `workspace/HEARTBEAT.md`
What Archie does on proactive check-ins (OpenClaw's heartbeat system):
- Check tasks.json for items due today/tomorrow
- Check if anyone is overdue and hasn't posted an update
- Check if it's Monday → post weekly digest
- Vary phrasing, never sound like a cron job

### `workspace/TEAM.md`
Team roster with Discord IDs. Archie uses this to:
- Compose `<@DISCORD_USER_ID>` mentions in messages
- Route questions to the right person by role
- Know who owns what

Format:
```
# Ottawa Blockchain Team

## Members

**Nolan** | <@DISCORD_ID> | Lead / Events / Partnerships
Owns: events, sponsorships, community, partnerships

**[Name]** | <@DISCORD_ID> | [Role]
Owns: [areas]
```

---

## Task Format (`tasks.json`)

```json
[
  {
    "id": "1",
    "name": "Task description",
    "assigned_to": "Name (must match TEAM.md)",
    "due_date": "YYYY-MM-DD",
    "status": "pending",
    "notes": ""
  }
]
```

Status values: `pending`, `in-progress`, `done`, `blocked`

Edit this file directly until Notion is connected.

---

## Reminder Logic (for HEARTBEAT.md)

Archie checks tasks on heartbeat and decides what to post:

| Situation | Action |
|-----------|--------|
| Task due today | Direct @mention — "your X is due today" |
| Task due tomorrow | Heads-up @mention |
| Task due in 2 days + no recent update in channel | Gentle nudge |
| Task due in 2 days + person already posted update | Skip |
| Task marked `done` | Never mention |
| Task marked `blocked` | Ask what's blocking before anything else |
| Monday | Post full weekly digest for all team members |
| Before 9 AM or after 6 PM ET | No pings |

---

## Environment Variables

```
DISCORD_BOT_TOKEN=
DISCORD_GUILD_ID=
DISCORD_CHANNEL_ID=
ANTHROPIC_API_KEY=
BOT_OWNER_DISCORD_ID=

# Notion — fill when ready
# NOTION_TOKEN=
# NOTION_DATABASE_ID=
```

---

## Notion Connection (later)

When ready:
1. Create Ottawa Blockchain Notion workspace (separate from Nolan's personal workspace)
2. Move/duplicate Action Items database into new workspace
3. Create Notion integration at notion.so/my-integrations
4. Share database with integration
5. Add `NOTION_TOKEN` and `NOTION_DATABASE_ID` to `.env`
6. Implement `_fetch_from_notion()` in `archive/notion_sync.py` and wire it up

---

## Security Notes

- This VPS is dedicated to Archie only — no Julia, no Simon, no personal tools
- OpenClaw gateway bound to loopback (`bind: loopback` in openclaw.json)
- Telegram is NOT connected on this VPS — Discord only
- Run `openclaw security audit --deep` after setup
- `.env` is never committed — use `.env.example` as template

---

## Verification Checklist

- [ ] Archie appears online in Discord server
- [ ] Archie responds when @mentioned in the accountability channel
- [ ] MEMORY.md gets updated after conversations where something new is learned
- [ ] Heartbeat fires and Archie proactively posts due-date reminders
- [ ] Monday digest posts with correct `<@ID>` mentions
- [ ] Tier 3 nudge: due in 2 days + no update → nudge sent
- [ ] Tier 3 skip: due in 2 days + person updated → no nudge
- [ ] `openclaw gateway status` shows running
- [ ] Bot survives VPS restart (`sudo systemctl restart openclaw`)

---

## What's Out of Scope (V1)

- Luma / Twitter / Instagram event fetching
- Slash commands (OpenClaw handles via natural language)
- Web dashboard
- Integration with Julia or Simon
- DM-based reminders
