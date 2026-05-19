FROM node:22-slim

WORKDIR /app

# System deps: Python is needed for entrypoint.sh and seed-crons.py
RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*

# mcp-proxy bridges the OpenClaw gateway to HTTP-based MCP servers
RUN pip3 install mcp-proxy --break-system-packages

# OpenClaw runtime + Notion MCP server (pre-installed — avoids slow npx download on every start)
# Pin openclaw to a known-good version; bump deliberately.
# Note: @notionhq/notion-mcp-server registers the `notion-mcp-server` binary.
RUN npm install -g \
    openclaw@2026.5.12 \
    @notionhq/notion-mcp-server

# Clamp the OpenClaw gateway timeout floor from 1ms → 5000ms.
# gpt-5 can return a timeoutMs < 1 which triggers spurious "gateway timeout after 1ms" errors.
RUN cd /usr/local/lib/node_modules/openclaw/dist && \
    sed -i -E \
    's/Math\.max\(1, Math\.floor\((opts|gateway)\.timeoutMs\)\)/Math.max(5000, Math.floor(\1.timeoutMs))/g' \
    gateway-*.js message-*.js

# Config is baked into the image at build time.
# Secrets are injected at runtime via entrypoint.sh — never stored in image layers.
# The workspace directory is bind-mounted at runtime (see docker-compose.yml).
COPY config/openclaw-docker.json ./openclaw-template.json
COPY config/openclaw-crons.json  ./openclaw-crons.json
COPY entrypoint.sh               ./entrypoint.sh
COPY seed-crons.py               ./seed-crons.py
RUN chmod +x /app/entrypoint.sh

ENV OPENCLAW_CONFIG_PATH=/app/openclaw.json
ENV OPENCLAW_STATE_DIR=/app

ENTRYPOINT ["/app/entrypoint.sh"]
