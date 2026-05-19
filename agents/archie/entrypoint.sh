#!/bin/sh
set -e

# ---------------------------------------------------------------------------
# 1. Write live config from template.
#
#    Uses Python string replacement instead of sed so token characters like
#    / + & = don't accidentally break the substitution.
#    Secrets are never written to stdout or shell history — only to the file.
# ---------------------------------------------------------------------------
python3 - <<'PYEOF'
import os, json, sys

def require(var):
    val = os.environ.get(var, "")
    if not val:
        print(f"[entrypoint] ERROR: {var} is not set", file=sys.stderr)
        sys.exit(1)
    return val

gateway_token      = require("OPENCLAW_GATEWAY_TOKEN")
discord_bot_token  = require("DISCORD_BOT_TOKEN")
discord_guild_id   = require("DISCORD_GUILD_ID")
discord_channel_id = require("DISCORD_CHANNEL_ID")
discord_owner_id   = require("DISCORD_OWNER_ID")
notion_token       = os.environ.get("NOTION_TOKEN", "")

with open("/app/openclaw-template.json") as f:
    content = f.read()

content = content.replace("REDACTED_GATEWAY_TOKEN",      gateway_token)
content = content.replace("REDACTED_DISCORD_BOT_TOKEN",  discord_bot_token)
content = content.replace("REDACTED_DISCORD_GUILD_ID",   discord_guild_id)
content = content.replace("REDACTED_DISCORD_CHANNEL_ID", discord_channel_id)
content = content.replace("REDACTED_DISCORD_OWNER_ID",   discord_owner_id)

if notion_token:
    content = content.replace("REDACTED_NOTION_TOKEN", notion_token)
else:
    print("[entrypoint] NOTION_TOKEN not set — starting without Notion MCP", flush=True)
    cfg = json.loads(content)
    cfg.pop("mcp", None)
    content = json.dumps(cfg, indent=2)

with open("/app/openclaw.json", "w") as f:
    f.write(content)
PYEOF

# ---------------------------------------------------------------------------
# 2. Upgrade CLI device to full operator scope before the gateway reads it.
#    This ensures the paired device can issue any command (e.g. /new, /model)
#    without needing a re-pair after each container rebuild.
# ---------------------------------------------------------------------------
python3 - <<'PYEOF'
import json, os

path = "/app/devices/paired.json"
if not os.path.exists(path):
    exit(0)

full = ["operator.admin", "operator.pairing", "operator.read", "operator.write"]

with open(path) as f:
    data = json.load(f)

changed = False
for dev in data.values():
    if dev.get("scopes") != full:
        dev["scopes"]         = full
        dev["approvedScopes"] = full
        for tok in dev.get("tokens", {}).values():
            tok["scopes"] = full
        changed = True

if changed:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print("[entrypoint] upgraded device scopes to operator.admin", flush=True)
PYEOF

# ---------------------------------------------------------------------------
# 3. Start the OpenClaw gateway in the background, then wait for it to be ready.
#    bind lan so other containers on the Docker network can reach it.
# ---------------------------------------------------------------------------
openclaw gateway run --port 18789 --bind lan &
GATEWAY_PID=$!

echo "[entrypoint] waiting for gateway..."
for i in $(seq 1 90); do
    if openclaw cron list >/dev/null 2>&1; then
        echo "[entrypoint] gateway ready after ${i}s"
        break
    fi
    sleep 1
done

# ---------------------------------------------------------------------------
# 4. Seed cron jobs. Retry up to 3 times — the gateway can take a moment to
#    fully initialise channel connections after it reports as ready.
# ---------------------------------------------------------------------------
for attempt in 1 2 3; do
    echo "[entrypoint] seeding crons (attempt $attempt)..."
    output=$(python3 /app/seed-crons.py 2>&1)
    echo "$output"
    if echo "$output" | grep -q "FAIL"; then
        echo "[entrypoint] some crons failed, retrying in 10s..."
        sleep 10
    else
        break
    fi
done

# ---------------------------------------------------------------------------
# 5. Hand control back to the gateway — keeps the container alive.
# ---------------------------------------------------------------------------
wait $GATEWAY_PID
