FROM node:22-slim

WORKDIR /app

RUN apt-get update -qq && apt-get install -y -qq python3 gettext-base && rm -rf /var/lib/apt/lists/*

RUN npm install -g openclaw@latest

COPY config/openclaw.json.template ./openclaw.json.template
COPY workspace/ ./workspace/
COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

ENV OPENCLAW_CONFIG_PATH=/app/openclaw.json
ENV OPENCLAW_STATE_DIR=/app

ENTRYPOINT ["./entrypoint.sh"]
