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

exec openclaw gateway run
