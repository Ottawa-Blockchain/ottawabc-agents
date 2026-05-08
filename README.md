# Archie — Ottawa Blockchain Accountability Bot

Discord accountability bot for the Ottawa Blockchain private team channel. Archie tracks action items, sends smart reminders based on due dates, and routes questions to the right team member.

## Setup

### 1. Discord Bot

1. Go to discord.com/developers/applications → New Application → "Archie"
2. Bot tab → Add Bot → copy the token
3. OAuth2 → URL Generator → select `bot` + `applications.commands`
4. Bot permissions: `Send Messages`, `Read Message History`, `Mention Everyone`, `Use Slash Commands`
5. Invite bot to your server using the generated URL

### 2. Environment

```bash
cp .env.example .env
# Fill in all values in .env
```

Required values:
- `DISCORD_BOT_TOKEN` — from Discord developer portal
- `DISCORD_GUILD_ID` — right-click your server → Copy Server ID
- `DISCORD_CHANNEL_ID` — right-click the accountability channel → Copy Channel ID
- `ANTHROPIC_API_KEY` — from console.anthropic.com
- `BOT_OWNER_DISCORD_ID` — your Discord user ID (right-click yourself → Copy User ID)

### 3. Team Roster

Edit `team.json` with your real team members and their Discord user IDs.

### 4. Action Items

Edit `tasks.json` to add action items until Notion is connected. Format:
```json
{
  "id": "unique-id",
  "name": "Task description",
  "assigned_to": "Name (must match team.json)",
  "due_date": "YYYY-MM-DD",
  "status": "pending",
  "notes": ""
}
```

Status values: `pending`, `in-progress`, `done`, `blocked`

### 5. Run Locally

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/python bot.py
```

### 6. Deploy on VPS

```bash
# Copy files to VPS
scp -r . nolan@your-vps:/home/nolan/ottawabc-bot

# On the VPS
cd /home/nolan/ottawabc-bot
python3 -m venv venv
venv/bin/pip install -r requirements.txt
cp .env.example .env && nano .env   # fill in values

sudo cp ottawabc-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ottawabc-bot
sudo systemctl start ottawabc-bot

# Check logs
journalctl -u ottawabc-bot -f
```

## Slash Commands

| Command | Description |
|---------|-------------|
| `/status` | Show all pending action items |
| `/status @user` | Show tasks for a specific person |
| `/done [task_id]` | Mark a task as done |
| `/remind` | Trigger the full digest now (owner only) |

## Reminder Schedule

| When | What |
|------|------|
| Monday 9 AM ET | Full weekly digest — all tasks, all people |
| Tue–Sun 9 AM ET | Smart daily check — due today/tomorrow get @mentioned; due in 2 days only get nudged if they haven't posted an update |

## Connecting Notion (later)

When ready, see the commented code in `notion_sync.py`. You'll need:
1. A Notion workspace for Ottawa Blockchain
2. An integration token (notion.so/my-integrations)
3. The Action Items database shared with the integration
4. `NOTION_TOKEN` and `NOTION_DATABASE_ID` added to `.env`
