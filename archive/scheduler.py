import os
import json
from datetime import date, timedelta
from pathlib import Path

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from notion_sync import fetch_tasks
from claude_handler import ClaudeHandler

ET = pytz.timezone("America/Toronto")

STATUS_EMOJI = {
    "pending": "⏳",
    "in-progress": "🔄",
    "done": "✅",
    "blocked": "🔴",
}


def load_team() -> dict:
    return json.loads(Path("team.json").read_text())


def _mention(member: dict) -> str:
    did = member.get("discord_id", "")
    if did and did != "DISCORD_USER_ID_HERE":
        return f"<@{did}>"
    return f"**{member['name']}**"


async def post_weekly_digest(bot) -> None:
    channel = bot.get_channel(int(os.getenv("DISCORD_CHANNEL_ID", 0)))
    if not channel:
        return

    tasks = [t for t in fetch_tasks() if t.get("status") != "done"]
    team = load_team()

    by_person: dict[str, list] = {}
    for task in tasks:
        by_person.setdefault(task["assigned_to"], []).append(task)

    if not any(by_person.get(m["name"]) for m in team["members"]):
        await channel.send("📋 All clear — no pending action items this week.")
        return

    lines = ["📋 **Ottawa Blockchain — Weekly Action Items**\n"]
    for member in team["members"]:
        person_tasks = by_person.get(member["name"], [])
        if not person_tasks:
            continue
        lines.append(_mention(member))
        for t in person_tasks:
            emoji = STATUS_EMOJI.get(t.get("status", "pending"), "⏳")
            due = f" *(due {t['due_date']})*" if t.get("due_date") else ""
            lines.append(f"• {t['name']}{due} {emoji}")
        lines.append("")

    await channel.send("\n".join(lines))


async def post_daily_check(bot) -> None:
    channel = bot.get_channel(int(os.getenv("DISCORD_CHANNEL_ID", 0)))
    if not channel:
        return

    claude = ClaudeHandler()
    tasks = fetch_tasks()
    team = load_team()
    today = date.today()
    tomorrow = today + timedelta(days=1)
    day_after = today + timedelta(days=2)

    member_map = {m["name"]: m for m in team["members"]}

    for task in tasks:
        if task.get("status") == "done":
            continue
        raw_due = task.get("due_date")
        if not raw_due:
            continue
        try:
            due = date.fromisoformat(raw_due)
        except ValueError:
            continue

        member = member_map.get(task["assigned_to"])
        if not member:
            continue

        mention = _mention(member)

        if due == today:
            await channel.send(f"{mention} your **{task['name']}** is due today.")

        elif due == tomorrow:
            await channel.send(f"{mention} heads up — **{task['name']}** is due tomorrow.")

        elif due == day_after:
            # Collect recent messages from this person and check if they already gave an update
            discord_id = member.get("discord_id", "")
            recent: list[str] = []
            if discord_id and discord_id != "DISCORD_USER_ID_HERE":
                async for msg in channel.history(limit=150):
                    if str(msg.author.id) == discord_id:
                        recent.append(msg.content)
                    if len(recent) >= 25:
                        break

            has_update = await claude.check_if_update(recent, task["name"], member["name"])
            if not has_update:
                await channel.send(
                    f"{mention} just checking in — **{task['name']}** is due {raw_due}. Any updates?"
                )


def setup_scheduler(bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=ET)

    # Monday 9 AM ET — full weekly digest
    scheduler.add_job(
        post_weekly_digest,
        CronTrigger(day_of_week="mon", hour=9, minute=0, timezone=ET),
        args=[bot],
        id="weekly_digest",
    )

    # Tue–Sun 9 AM ET — smart daily due-date check
    scheduler.add_job(
        post_daily_check,
        CronTrigger(day_of_week="tue,wed,thu,fri,sat,sun", hour=9, minute=0, timezone=ET),
        args=[bot],
        id="daily_check",
    )

    scheduler.start()
    return scheduler
