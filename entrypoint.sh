#!/bin/sh
set -e

# Substitute env vars into config template → live config
envsubst < /app/openclaw.json.template > /app/openclaw.json

exec openclaw gateway run
