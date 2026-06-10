# Notion — Task Tracker operations

Read this file whenever you read or write tasks in Notion. Never guess tool names, property
names, or field paths — they are exact, and Notion rejects anything else.

---

## The database

- **Name:** Task Tracker
- **Database ID:** `c59f9f1e-ce90-8313-b022-0196cf2ec33b`
- It is the only database shared with this integration, so a broad search returns only its pages.

### Property map (exact names + types)

| Property | Type | Notes |
|----------|------|-------|
| `Task name` | title | the task title |
| `Status` | **status** | one of: `To do`, `In progress`, `Blocked`, `Done`, `Cancelled` |
| `Owner` | **select** | one of the seven names below — this is how we track who owns a task |
| `Due date` | date | `YYYY-MM-DD` or unset |
| `Description` | rich_text | optional detail |
| `Tags` | multi_select | `🎨 Design`, `💻 Tech`, `📱 Marketing`, `General` — category, not owner |

> **Do not use** the `Assignee`, `Person`, or `Ass` people-type fields. The team are not paid
> Notion members, so people-fields can't hold them. **Ownership lives in the `Owner` select.**
> `Files & media` is unused too.

### Owner → Discord mention

The `Owner` select value maps to a Discord ID (these mirror TEAM.md — keep them in sync):

| `Owner` | Discord mention |
|---------|-----------------|
| Nolan  | `<@712636536755060777>` |
| Adrian | `<@695714324827734077>` |
| Aiden  | `<@302810491707850763>` |
| Bender | `<@466868422823641088>` |
| Sara   | `<@1067247638803656724>` |
| Karim  | `<@375703603563986955>` |
| Nathan | `<@1282820043994038293>` |

An empty `Owner` = unassigned. Infer the owner from TEAM.md ownership areas when logging a task;
if it's genuinely unclear, ask one short question or tag Nolan.

---

## Which MCP tool to call

This Notion MCP uses the newer data-source API. **Do not use `API-query-data-source`** — it wants
an internal data-source ID (not the database UUID) and returns a 400.

| Action | Tool | Notes |
|--------|------|-------|
| List tasks | `API-post-search` | returns all Task Tracker pages; filter client-side |
| Create a task | `API-post-page` | parent `{ "database_id": "<id above>" }` |
| Update a task | `API-patch-page` | by `page_id`; set Status / Owner / Due date |

### Listing tasks (`API-post-search`)

```json
{ "filter": { "value": "page", "property": "object" }, "query": "" }
```

Then filter the results client-side:
- skip any page where `properties.Status.status.name` is `Done` or `Cancelled`
- skip any page where `in_trash` is `true`

### Reading fields from a result

| Field | Path |
|-------|------|
| Task name | `properties["Task name"].title[0].plain_text` |
| Status | `properties.Status.status.name` |
| Owner | `properties.Owner.select.name` (or `null`) |
| Due date | `properties["Due date"].date.start` (or `null`) |
| Page ID | `id` — needed for write-back |

---

## Task cache (`/app/workspace/TASKS.json`)

Notion is metered and slow. Cache it. **Read the cache, not Notion**, unless it's the morning
heartbeat or someone explicitly says "refresh"/"sync".

```json
{
  "fetched_at": "2026-06-10T09:00:00-04:00",
  "tasks": [
    { "id": "notion-page-uuid", "name": "Confirm venue", "status": "To do",
      "owner": "Nolan", "due": "2026-06-12" }
  ]
}
```

| Trigger | Notion or cache? |
|---------|------------------|
| Daily heartbeat (9 AM) | fetch fresh from Notion → overwrite `TASKS.json` → then nudge |
| Ambient pickup / "what's on my plate" / DM status | read `TASKS.json` |
| Log a new task | create in Notion → append to `TASKS.json` |
| Mark complete | update Notion → update/remove in `TASKS.json` |
| "refresh" / "sync" | fetch fresh → overwrite `TASKS.json` → confirm |

`open` task = `Status` is not `Done` and not `Cancelled`.

---

## Writing

### Create a task (`API-post-page`)

```json
{
  "parent": { "database_id": "c59f9f1e-ce90-8313-b022-0196cf2ec33b" },
  "properties": {
    "Task name": { "title": [ { "text": { "content": "Confirm venue for June event" } } ] },
    "Status":    { "status": { "name": "To do" } },
    "Owner":     { "select": { "name": "Nolan" } },
    "Due date":  { "date": { "start": "2026-06-12" } }
  }
}
```

- Omit `Owner` if unassigned, `Due date` if none. New tasks start at `Status` = `To do`.
- Before creating, scan the cache for a near-duplicate by name — update instead of duplicating.

### Mark complete / update (`API-patch-page`)

```json
{ "page_id": "<id from cache>", "properties": { "Status": { "status": { "name": "Done" } } } }
```

Reassign with `"Owner": { "select": { "name": "Bender" } }`; reschedule with `"Due date"`.
After any write, update `TASKS.json` to match.

---

## Output formats (Discord, plain text — see SOUL.md for voice)

Keep it short and vary phrasing. `@mention` owners with the IDs above. Never start a line with "I".

### Daily nudge (9 AM, Tue–Fri)
Only ping on tasks **due today, tomorrow, or in 2 days, or overdue**. If a task's owner already
posted an update in-channel, skip it. If nothing needs a nudge, say nothing (`NO_REPLY` in cron).
```
<@695714324827734077> — "Confirm venue" is due tomorrow. Still good?
```

### Monday weekly digest (9 AM Mon)
Group open tasks by owner. One block per person.
```
Weekly rundown — open tasks:

<@712636536755060777>
- Sponsorship deck — due Jun 12
- Venue confirmation — overdue (Jun 9)

<@1282820043994038293>
- Website copy — no due date

Unassigned: Photographer role — Jun 13
```
If the board is empty: `Clean board — nothing open.`

### Mark-complete confirmation
```
Done. Marked "Confirm venue" complete.
```

### Manual refresh
```
Synced. 7 open tasks.
```
