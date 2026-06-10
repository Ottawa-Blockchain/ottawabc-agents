FROM node:22-slim

WORKDIR /app

# Set state dir early so plugin installs land in /app, matching the runtime env.
ENV OPENCLAW_STATE_DIR=/app

# System deps: Python is needed for entrypoint.sh and seed-crons.py
RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# mcp-proxy bridges the OpenClaw gateway to HTTP-based MCP servers
RUN pip3 install mcp-proxy --break-system-packages

# OpenClaw runtime + Notion MCP server (pre-installed — avoids slow npx download on every start)
# Pin openclaw to a known-good version; bump deliberately.
# 2026.5.28 is the version proven against the two gpt-5 patches below (matches Melody).
# Note: @notionhq/notion-mcp-server registers the `notion-mcp-server` binary.
# OPENCLAW_STATE_DIR is set above so the Discord plugin installs to /app, not ~/.openclaw.
RUN npm install -g \
    openclaw@2026.5.28 \
    @notionhq/notion-mcp-server \
    && openclaw plugins install @openclaw/discord

# Clamp the OpenClaw gateway timeout floor from 1ms → 5000ms.
# gpt-5 can return a timeoutMs < 1 which triggers spurious "gateway timeout after 1ms" errors.
RUN cd /usr/local/lib/node_modules/openclaw/dist && \
    sed -i -E \
    's/Math\.max\(1, Math\.floor\((opts|gateway)\.timeoutMs\)\)/Math.max(5000, Math.floor(\1.timeoutMs))/g' \
    gateway-*.js message-*.js

# Force store:true on the OpenAI Responses send path. The transport REPLAYS prior reasoning
# items (rs_*) and their response ids every turn but hard-codes storeMode:"disable", so those
# items are never persisted — the next round-trip 404s ("Item with id 'rs_...' not found") and
# EVERY gpt-5 reply fails. "provider-policy" resolves explicitStore=true for native OpenAI
# responses models (gpt-5), so replayed items resolve. The trailing `! grep` makes the build
# fail loudly if the target string ever moves in a future OpenClaw version.
RUN cd /usr/local/lib/node_modules/openclaw/dist && \
    sed -i 's/storeMode: "disable"/storeMode: "provider-policy"/' openai-transport-stream-*.js && \
    ! grep -l 'storeMode: "disable"' openai-transport-stream-*.js

# Config is baked into the image at build time.
# Secrets are injected at runtime via entrypoint.sh — never stored in image layers.
# The workspace directory is bind-mounted at runtime (see docker-compose.yml).
COPY config/openclaw-docker.json ./openclaw-template.json
COPY config/openclaw-crons.json  ./openclaw-crons.json
COPY entrypoint.sh               ./entrypoint.sh
COPY seed-crons.py               ./seed-crons.py
RUN chmod +x /app/entrypoint.sh

ENV OPENCLAW_CONFIG_PATH=/app/openclaw.json

ENTRYPOINT ["/app/entrypoint.sh"]
