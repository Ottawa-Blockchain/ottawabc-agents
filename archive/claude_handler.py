import os
import json
from pathlib import Path
import anthropic


class ClaudeHandler:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-sonnet-4-6"

    def _build_system_prompt(self) -> str:
        soul = Path("workspace/SOUL.md").read_text() if Path("workspace/SOUL.md").exists() else ""
        team_doc = Path("workspace/TEAM.md").read_text() if Path("workspace/TEAM.md").exists() else ""
        team_data = json.loads(Path("team.json").read_text()) if Path("team.json").exists() else {}
        return f"{soul}\n\n{team_doc}\n\nTeam roster (JSON):\n{json.dumps(team_data, indent=2)}"

    async def handle_message(self, content: str, author_name: str) -> str:
        system = self._build_system_prompt()
        response = self.client.messages.create(
            model=self.model,
            max_tokens=400,
            system=system,
            messages=[{"role": "user", "content": f"{author_name}: {content}"}],
        )
        return response.content[0].text

    async def check_if_update(self, recent_messages: list[str], task_name: str, person_name: str) -> bool:
        """Return True if recent chat history suggests person already gave an update on their task."""
        if not recent_messages:
            return False
        messages_text = "\n".join(recent_messages[-20:])
        response = self.client.messages.create(
            model=self.model,
            max_tokens=10,
            system="You analyze Discord messages to check if a team member posted a status update about a specific task. Reply only 'yes' or 'no'.",
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Has {person_name} mentioned or given any update on their task '{task_name}' "
                        f"in the following recent messages?\n\n{messages_text}"
                    ),
                }
            ],
        )
        return response.content[0].text.strip().lower().startswith("yes")
