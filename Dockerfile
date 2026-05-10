FROM node:22-slim

WORKDIR /app

RUN npm install -g openclaw@latest

COPY config/openclaw.json.template ./openclaw.json.template
COPY workspace/ ./workspace/
COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

ENV OPENCLAW_CONFIG_PATH=/app/openclaw.json
ENV OPENCLAW_STATE_DIR=/app

ENTRYPOINT ["./entrypoint.sh"]
