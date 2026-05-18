#!/usr/bin/env python3
"""
Seed OpenClaw cron jobs from JSON config files.

Reads from two sources (in order):
  1. /app/openclaw-crons.json  — static jobs baked into the image
  2. /app/workspace/dynamic-crons.json  — agent-written persistent jobs

Env vars in `deliver_to` fields are resolved at runtime using str.format(**os.environ),
so cron configs can reference e.g. "discord:{DISCORD_CHANNEL_ID}" without hardcoding IDs.
"""

import json, os, subprocess, sys

SOURCES = [
    "/app/openclaw-crons.json",
    "/app/workspace/dynamic-crons.json",
]


def seed_job(job: dict, source: str) -> None:
    # Resolve env vars in deliver_to (e.g. "discord:{DISCORD_CHANNEL_ID}")
    try:
        deliver_to = job["deliver_to"].format(**os.environ)
    except KeyError as e:
        print(f"[seed-crons] FAIL: {job['name']} — missing env var {e}", flush=True)
        return

    cmd = [
        "openclaw", "cron", "add",
        "--name",        job["name"],
        "--description", job.get("description", ""),
        "--cron",        job["schedule"],
        "--tz",          job["timezone"],
        "--session",     job["session"],
        "--to",          deliver_to,
    ]

    if "systemEvent" in job:
        cmd += ["--system-event", job["systemEvent"]]
    else:
        if job.get("announce", True):
            cmd.append("--announce")
        cmd += ["--message", job["message"]]

    if job.get("lightContext"):
        cmd.append("--light-context")
    if job.get("timeoutSeconds"):
        cmd += ["--timeout-seconds", str(job["timeoutSeconds"])]

    result = subprocess.run(cmd, capture_output=True, text=True)
    status = "OK" if result.returncode == 0 else "FAIL"
    print(f"[seed-crons] {status}: {job['name']} (from {source})", flush=True)
    if result.returncode != 0:
        print(f"  {result.stderr.strip()[:300]}", flush=True, file=sys.stderr)


for source in SOURCES:
    if not os.path.exists(source):
        continue
    with open(source) as f:
        data = json.load(f)
    for job in data.get("jobs", []):
        seed_job(job, source)
