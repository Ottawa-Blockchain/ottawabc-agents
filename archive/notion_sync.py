"""
Task data source. Currently reads from tasks.json.
When ready to connect Notion, implement fetch_from_notion() below and
swap the call in fetch_tasks(). The returned list format stays the same.
"""

import json
from pathlib import Path


def fetch_tasks() -> list[dict]:
    return _fetch_from_file()


def save_tasks(tasks: list[dict]) -> None:
    Path("tasks.json").write_text(json.dumps(tasks, indent=2))


def mark_done(task_id: str) -> bool:
    tasks = fetch_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            save_tasks(tasks)
            return True
    return False


def _fetch_from_file() -> list[dict]:
    path = Path("tasks.json")
    if not path.exists():
        return []
    return json.loads(path.read_text())


# --- Notion integration (fill in when ready) ---
# def _fetch_from_notion() -> list[dict]:
#     from notion_client import Client
#     import os
#
#     notion = Client(auth=os.getenv("NOTION_TOKEN"))
#     db_id = os.getenv("NOTION_DATABASE_ID")
#     response = notion.databases.query(database_id=db_id)
#
#     tasks = []
#     for page in response["results"]:
#         props = page["properties"]
#         tasks.append({
#             "id": page["id"],
#             "name": props["Name"]["title"][0]["plain_text"] if props["Name"]["title"] else "",
#             "assigned_to": props["Assigned To"]["select"]["name"] if props["Assigned To"].get("select") else "",
#             "due_date": props["Due Date"]["date"]["start"] if props["Due Date"].get("date") else None,
#             "status": props["Status"]["select"]["name"].lower() if props["Status"].get("select") else "pending",
#             "notes": props["Notes"]["rich_text"][0]["plain_text"] if props["Notes"].get("rich_text") else "",
#         })
#     return tasks
