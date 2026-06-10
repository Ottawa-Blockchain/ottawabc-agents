# Archie — Ottawa Blockchain Accountability Bot

OpenClaw-based Discord accountability bot for the Ottawa Blockchain private team channel. Tracks action items, sends smart reminders based on due dates, learns from conversations, and routes questions to the right team member.

**Read `PLAN.md` first** — it has the full setup walkthrough for a fresh VPS.

## Quick Start (on the dedicated VPS)

```bash
# 1. Install OpenClaw
npm install -g openclaw@latest

# 2. Clone this repo
git clone https://github.com/nolandruid/ottawabc-bot.git
cd ottawabc-bot

# 3. Run the onboard wizard
openclaw onboard --install-daemon

# 4. Symlink workspace
mv ~/.openclaw/workspace ~/.openclaw/workspace.bak
ln -s ~/ottawabc-bot/workspace ~/.openclaw/workspace
openclaw gateway restart

# 5. Verify
openclaw gateway status
```

## Workspace Files

| File | Purpose |
|------|---------|
| `workspace/SOUL.md` | Archie's identity, tone, routing rules |
| `workspace/MEMORY.md` | Auto-updated by Archie as he learns |
| `workspace/HEARTBEAT.md` | Proactive reminder logic |
| `workspace/TEAM.md` | Team roster + Discord IDs |

## Action Items

Edit `tasks.json` directly until Notion is connected. See `PLAN.md` for Notion setup steps.

## Team Roster

Copy the template and fill in real names + Discord user IDs (`<@ID>`):

```bash
cp agents/archie/workspace/TEAM.example.md agents/archie/workspace/TEAM.md
```

`TEAM.md` is gitignored (it holds real member info) — it stays local and is never committed.
Also list the same Discord IDs in `DISCORD_ALLOWLIST` in `agents/archie/.env` so they can DM Archie.

## Architecture

- **Runtime:** OpenClaw on dedicated DigitalOcean VPS
- **Channel:** Discord (Ottawa Blockchain private accountability channel)
- **Model:** claude-sonnet-4-6
- **Tasks:** tasks.json → Notion (later)
- **Memory:** workspace/MEMORY.md (auto-updated)
- **Proactivity:** OpenClaw heartbeat system + HEARTBEAT.md
