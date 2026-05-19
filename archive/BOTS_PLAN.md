# Ottawa Blockchain — Bot Roster & Plan

## Context

The server was quiet. This plan adds a second bot (Pulse) alongside Archie to generate consistent community activity — news, quizzes, project follow-ups, and discussion. Starting with 2 bots keeps cost low. More can be added using the same pattern.

---

## Bot Roster

### Archie — Private Accountability Bot
- **Channel:** Private team channel
- **Model:** gpt-5
- **Job:** Task reminders, due-date nudges, weekly digest, routes questions to right team member
- **Schedule:** Daily 9 AM ET check, Monday digest
- **Workspace:** `agents/archie/workspace/`
- **Status:** Built, needs `.env` filled + Discord bot token

### Pulse — Public Community Bot
- **Channel:** Public general / community channel
- **Model:** gpt-4o (cheaper — routine content generation)
- **Job:** Posts news + discussion questions, beginner quizzes, follows up on members' projects
- **Schedule:** Mon/Wed/Fri 10 AM ET + always-on @mention responses
- **Workspace:** `agents/pulse/workspace/`
- **Status:** Built, needs `.env` filled + Discord bot token

---

## What Pulse Does

| Day | Post type |
|-----|-----------|
| Monday | Blockchain/Web3 news + discussion question |
| Wednesday | Beginner quiz (multiple choice → answer + follow-up) |
| Friday | Hot take, community check-in, or project follow-up |
| Anytime | Responds to @mentions and replies |
| 2+ weeks after someone mentions a project | Light follow-up tag |

**Quiz flow example:**
> Pulse: "Quick one — what does 'gas' mean in Ethereum? A) Transaction fee  B) Network speed  C) Block size"
> Someone answers
> Pulse: "It's A — transaction fee. Basically what you pay miners/validators to process your transaction. Anyone here ever had a tx fail because gas was too low?"

**Project follow-up example:**
> "Hey <@ID>, you mentioned you were building a DEX a couple weeks back — how's that going?"

---

## Cost Estimate

| Bot | Model | Est. monthly |
|-----|-------|-------------|
| Archie | gpt-5 | ~$5–15 |
| Pulse | gpt-4o | ~$2–6 |
| **Total** | | **~$7–21/month** |

VPS: ~$6–12/month (DigitalOcean basic droplet)

---

## Setup Checklist

### For Archie
- [ ] Fill `agents/archie/.env` (copy from `.env.example`)
- [ ] Fill Discord IDs in `team.json` and `agents/archie/workspace/TEAM.md`
  - Right-click username in Discord → Copy User ID (needs Developer Mode on)
- [ ] Replace placeholder tasks in `tasks.json` with real ones

### For Pulse
- [ ] Create a second Discord bot at discord.com/developers/applications
- [ ] Fill `agents/pulse/.env` (copy from `.env.example`)
- [ ] No member IDs needed — Pulse learns them from messages automatically

### Launch both
```bash
docker compose up --build -d
docker compose logs -f          # watch both at once
```

---

## Repo Structure

```
ottawabc-bot/
├── agents/
│   ├── archie/
│   │   ├── config/openclaw.json.template
│   │   ├── workspace/ (SOUL, HEARTBEAT, TEAM, MEMORY)
│   │   └── .env.example
│   └── pulse/
│       ├── config/openclaw.json.template
│       ├── workspace/ (SOUL, HEARTBEAT, MEMORY)
│       └── .env.example
├── Dockerfile          (parameterized via AGENT build arg)
├── docker-compose.yml  (both services)
├── entrypoint.sh
├── tasks.json          (Archie's task list — edit directly until Notion connected)
├── team.json           (team roster with Discord IDs)
├── PLAN.md             (Archie setup guide)
└── BOTS_PLAN.md        (this file)
```

---

## Future Bots (same pattern, one session each)

| Bot | Job |
|-----|-----|
| **Event** | Auto-posts Ottawa Blockchain events from Luma/Eventbrite |
| **Debate** | Takes strong positions on blockchain topics to spark argument |
| **Learn** | Dedicated quiz bot with leaderboards — if Pulse's quiz feature outgrows Pulse |
| **Recap** | Friday summary of what was discussed in the server that week |

Adding any of these: create `agents/[name]/`, add service to `docker-compose.yml`, done.
