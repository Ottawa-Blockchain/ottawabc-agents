# Ottawa Blockchain Agents

Discord agent stack for the Ottawa Blockchain community. Two bots, one server:

| Bot | Channel | Role |
|-----|---------|------|
| **Archie** | Private team channel | Accountability, task management, Notion |
| **Pulse** | Public community channel | News, quizzes, community engagement |

Built on [OpenClaw](https://openclaw.ai), running in Docker.

---

## Quick Start

### Prerequisites

- Docker + Docker Compose
- Discord Developer account (one bot per agent)
- OpenAI API key
- Anthropic API key (Archie fallback model)
- Notion integration token (Archie)

### 1. Clone and configure

```bash
git clone https://github.com/Ottawa-Blockchain/ottawabc-agents.git
cd ottawabc-agents

# Fill in credentials for each agent
cp agents/archie/.env.example agents/archie/.env
cp agents/pulse/.env.example  agents/pulse/.env
# Edit both .env files — see comments inside for where to get each value
```

### 2. Set up your team roster

Edit `agents/archie/workspace/TEAM.md` with your team members' real names and Discord user IDs. This file is gitignored and stays local — never commit it.

### 3. Run

```bash
docker compose up --build -d
docker compose logs -f
```

Both bots should appear online in Discord within ~30 seconds.

---

## Repository Structure

```
ottawabc-agents/
├── agents/
│   ├── archie/               ← Archie's build context and workspace
│   │   ├── Dockerfile
│   │   ├── entrypoint.sh
│   │   ├── seed-crons.py
│   │   ├── config/
│   │   │   ├── openclaw-docker.json   ← OpenClaw config (secrets as REDACTED_*)
│   │   │   └── openclaw-crons.json    ← Scheduled heartbeat jobs
│   │   ├── workspace/                 ← Agent's brain (bind-mounted at runtime)
│   │   │   ├── SOUL.md                ← Identity, behaviour, rules
│   │   │   ├── HEARTBEAT.md           ← Proactive check-in logic
│   │   │   ├── TEAM.md                ← Team roster + Discord IDs (local only)
│   │   │   ├── MEMORY.md              ← Learned context (auto-updated)
│   │   │   └── TOOLS.md               ← Environment notes (Notion, commands)
│   │   ├── persist/                   ← Device pairing tokens (gitignored)
│   │   └── .env.example
│   └── pulse/                ← Pulse's build context and workspace
│       ├── config/
│       ├── workspace/
│       └── .env.example
├── Dockerfile                ← Shared build for Pulse
├── entrypoint.sh             ← Shared entrypoint for Pulse
├── docker-compose.yml
└── LICENSE
```

---

## How It Works

Both agents run on [OpenClaw](https://openclaw.ai) — an AI agent runtime that handles Discord connections, memory, scheduled jobs (heartbeats), and tool use.

**Config is baked into the image at build time.** Secrets (`REDACTED_*` placeholders) are injected at container startup by `entrypoint.sh` — they never appear in image layers or shell history.

**The workspace is bind-mounted from the host.** Archie reads and writes his workspace files (`SOUL.md`, `MEMORY.md`, etc.) live on disk. Changes you make take effect on the next session without a rebuild.

**Crons are seeded at startup.** `seed-crons.py` registers heartbeat jobs with the OpenClaw gateway every time the container starts. If a job already exists it's skipped.

**Persist volumes survive restarts.** Discord bot pairing and gateway identity are stored in `agents/archie/persist/` on the host, so Archie doesn't need to re-pair after a rebuild.

---

## Agents

- [Archie](agents/archie/README.md) — private accountability bot
- [Pulse](agents/pulse/README.md) — public community bot

---

## License

[PolyForm Noncommercial License 1.0](LICENSE) — free to use and adapt for personal, educational, and nonprofit purposes. Commercial use is not permitted.
