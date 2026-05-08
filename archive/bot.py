import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from scheduler import setup_scheduler
from claude_handler import ClaudeHandler
from notion_sync import fetch_tasks, mark_done

load_dotenv()

CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", 0))
OWNER_ID = os.getenv("BOT_OWNER_DISCORD_ID", "")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
claude = ClaudeHandler()


@bot.event
async def on_ready():
    print(f"Archie is online as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"Slash command sync failed: {e}")
    setup_scheduler(bot)


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if message.channel.id != CHANNEL_ID:
        return

    # Respond when @mentioned or message starts with "archie"
    mentioned = bot.user in message.mentions
    addressed = message.content.lower().startswith("archie")

    if mentioned or addressed:
        async with message.channel.typing():
            response = await claude.handle_message(message.content, message.author.display_name)
        await message.channel.send(response)

    await bot.process_commands(message)


# --- Slash commands ---

@bot.tree.command(name="status", description="Show current action items")
@app_commands.describe(user="Optional: show tasks for a specific team member")
async def status(interaction: discord.Interaction, user: discord.Member = None):
    await interaction.response.defer()

    tasks = fetch_tasks()
    active = [t for t in tasks if t.get("status") != "done"]

    if user:
        person_tasks = [t for t in active if t["assigned_to"].lower() == user.display_name.lower()]
        if not person_tasks:
            await interaction.followup.send(f"No pending tasks for {user.mention}.")
            return
        lines = [f"**{user.display_name}'s tasks:**"]
        for t in person_tasks:
            emoji = {"pending": "⏳", "in-progress": "🔄", "blocked": "🔴"}.get(t.get("status", ""), "⏳")
            due = f" *(due {t['due_date']})*" if t.get("due_date") else ""
            lines.append(f"{emoji} {t['name']}{due}")
        await interaction.followup.send("\n".join(lines))
        return

    if not active:
        await interaction.followup.send("All clear — no pending action items.")
        return

    # Group by person
    by_person: dict[str, list] = {}
    for t in active:
        by_person.setdefault(t["assigned_to"], []).append(t)

    lines = ["📋 **Current Action Items**\n"]
    for person, person_tasks in by_person.items():
        lines.append(f"**{person}**")
        for t in person_tasks:
            emoji = {"pending": "⏳", "in-progress": "🔄", "blocked": "🔴"}.get(t.get("status", ""), "⏳")
            due = f" *(due {t['due_date']})*" if t.get("due_date") else ""
            lines.append(f"{emoji} {t['name']}{due}")
        lines.append("")

    await interaction.followup.send("\n".join(lines))


@bot.tree.command(name="done", description="Mark one of your tasks as done")
@app_commands.describe(task_id="The task ID (visible in /status)")
async def done(interaction: discord.Interaction, task_id: str):
    success = mark_done(task_id)
    if success:
        await interaction.response.send_message(f"Marked task `{task_id}` as done. Nice work.")
    else:
        await interaction.response.send_message(f"Couldn't find task with ID `{task_id}`. Check `/status` for IDs.")


@bot.tree.command(name="remind", description="Trigger the full team digest now (owner only)")
async def remind(interaction: discord.Interaction):
    if OWNER_ID and str(interaction.user.id) != OWNER_ID:
        await interaction.response.send_message("Only the bot owner can trigger this.", ephemeral=True)
        return
    await interaction.response.defer()
    from scheduler import post_weekly_digest
    await post_weekly_digest(bot)
    await interaction.followup.send("Digest posted.", ephemeral=True)


if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_BOT_TOKEN not set in .env")
    bot.run(token)
