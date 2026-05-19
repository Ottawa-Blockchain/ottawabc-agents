# Pulse

Community engagement bot for the Ottawa Blockchain public Discord channel. Keeps the server alive with news, quizzes, and follow-ups — without spamming.

## What Pulse Does

- **Posts** blockchain news + discussion questions (Mondays)
- **Runs quizzes** — beginner-friendly multiple choice, opens into real conversation (Wednesdays)
- **Follows up** with community members about projects they mentioned (Fridays + ongoing)
- **Responds to @mentions** in the public channel at any time

## Workspace Files

| File | Purpose |
|------|---------|
| `workspace/SOUL.md` | Identity, tone, post types, community rules |
| `workspace/MEMORY.md` | Community members, what they're building, engagement history |
| `workspace/HEARTBEAT.md` | Scheduled post logic (Mon/Wed/Fri) |
| `workspace/skills/` | Self-built skills (post-quiz, community-followup, member-memory) |

## Configuration

### Environment variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Pulse needs its own separate Discord bot (separate application from Archie's).

### No team roster needed

Pulse learns community member Discord IDs from message metadata automatically — no manual setup required.

## Verification Checklist

After `docker compose up --build pulse`:

- [ ] Pulse appears online in Discord server
- [ ] Pulse responds when @mentioned in the public channel
- [ ] Scheduled posts fire on Mon/Wed/Fri at 10 AM ET
