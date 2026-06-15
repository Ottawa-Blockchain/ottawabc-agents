# Skill: x-social

Manage OB's X presence — browse the watchlist, repost selectively, and post on OB's behalf.

## When to run

- On the `x-browse` cron (twice daily)
- When a team member asks you to post something to X via Discord DM
- When a team member asks you to check what's been reposted or what's trending in the watchlist

## Browser session

Use the browser plugin. You are already logged into OB's X account (`@OttawaBlockchain`) via a persistent session. Do not log out. Do not navigate to login pages unless the session has expired — if it has, DM Nolan.

## Browsing the watchlist

Read the watchlist from `x-social/watchlist.md` in your workspace. For each account:

1. Navigate to `https://x.com/<handle>`
2. Read the 5–10 most recent posts
3. Note anything posted since your last browse (check `x-social/last-browse.md` for the timestamp)
4. Evaluate each post against the repost criteria below

After browsing all accounts, update `x-social/last-browse.md` with the current timestamp.

## Repost criteria

Repost a post if **all** of the following apply:

- **On-brand**: relates to blockchain, Web3, crypto, Ottawa/Canada tech scene, community events, or open-source
- **Credible**: from a source the OB community would respect — not sensationalist, not scammy
- **Fresh signal**: adds information or perspective, not just hype or price talk
- **Not already reposted**: check `x-social/repost-log.md`

When in doubt, skip it. One strong repost beats three mediocre ones.

## Reposting

1. Navigate to the post
2. Click the repost button (the two-arrow icon under the post)
3. Select "Repost" (not "Quote" unless you have something to add)
4. Log the repost in `x-social/repost-log.md`: `YYYY-MM-DD HH:MM | @handle | post URL | one-line reason`

## Posting original content

Only post original content when a team member explicitly asks via Discord DM. Do not initiate unprompted.

- Keep it short — X is not a blog
- Match OB's voice: professional but approachable, community-focused, never hype-y
- Confirm the draft with the requester before posting
- Log the post in `x-social/repost-log.md` with source: `[original]`

## What not to do

- Do not engage with replies or mentions unless Nolan explicitly asks
- Do not follow or unfollow accounts
- Do not like posts
- Do not post anything about price, investment advice, or "don't miss this"
- Do not post more than 3 times per day total (reposts + originals)
