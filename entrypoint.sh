#!/bin/sh
set -e

# If NOTION_TOKEN is not set, strip the MCP block so openclaw doesn't error on startup
if [ -z "${NOTION_TOKEN:-}" ]; then
  python3 -c "
import json, sys
cfg = json.load(open('/app/openclaw.json.template'))
cfg.pop('mcp', None)
print(json.dumps(cfg, indent=2))
" > /tmp/openclaw.json.notionless
  envsubst < /tmp/openclaw.json.notionless > /app/openclaw.json
else
  envsubst < /app/openclaw.json.template > /app/openclaw.json
fi

# Start gateway in background so we can run channel setup
openclaw gateway run &
GATEWAY_PID=$!

# Wait for gateway to be ready
sleep 20

# Auto-pair Discord on every startup so rebuilds don't break the connection
if [ -n "${DISCORD_BOT_TOKEN:-}" ]; then
  openclaw channels add --channel discord --token "$DISCORD_BOT_TOKEN" 2>&1 || true
fi

# Wait for gateway process
wait $GATEWAY_PID
