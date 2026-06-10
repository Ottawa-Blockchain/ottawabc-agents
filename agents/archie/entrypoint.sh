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

# DM allowlist: comma-separated Discord IDs in .env (keeps real IDs out of the public repo).
# Falls back to just the owner if unset. Rendered into the config as a JSON array.
allowlist = [x.strip() for x in os.environ.get("DISCORD_ALLOWLIST", "").split(",") if x.strip()]
if not allowlist:
    allowlist = [discord_owner_id]

with open("/app/openclaw-template.json") as f:
    content = f.read()

content = content.replace("REDACTED_GATEWAY_TOKEN",      gateway_token)
content = content.replace("REDACTED_DISCORD_BOT_TOKEN",  discord_bot_token)
content = content.replace("REDACTED_DISCORD_GUILD_ID",   discord_guild_id)
content = content.replace("REDACTED_DISCORD_CHANNEL_ID", discord_channel_id)
content = content.replace("REDACTED_DISCORD_OWNER_ID",   discord_owner_id)
# Replace the quoted placeholder with a real JSON array (note: quotes included in the match).
content = content.replace('"REDACTED_DISCORD_ALLOWLIST"', json.dumps(allowlist))

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
# 2. Start the OpenClaw gateway in the background, then wait for it to be ready.
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
# 3. Upgrade the CLI device to full operator scope — but only AFTER the gateway
#    has auto-paired it and written devices/paired.json. Running this before the
#    gateway starts (the old order) no-ops on a fresh boot, leaving the device
#    under-scoped so cron seeding fails. Wait for the file, then upgrade.
# ---------------------------------------------------------------------------
python3 - <<'PYEOF'
import json, os, time

path = "/app/devices/paired.json"
for _ in range(10):          # wait up to 10s for auto-pairing to write the file
    if os.path.exists(path):
        break
    time.sleep(1)
if not os.path.exists(path):
    print("[entrypoint] no devices file yet — skipping scope upgrade", flush=True)
    raise SystemExit(0)

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
