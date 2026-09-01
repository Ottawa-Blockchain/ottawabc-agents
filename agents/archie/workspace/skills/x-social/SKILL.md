# Skill: x-social

Manage OB's X presence — browse the watchlist, repost selectively, and post on OB's behalf.

## When to run

- On the `x-browse` cron (twice daily)
- When a team member asks you to post something to X via Discord DM
- When a team member asks you to check what's been reposted or what's trending in the watchlist

## Browser session & authentication

Use the browser plugin. On first run or when the session has expired:

1. Navigate to `https://x.com/login`
2. Log in with the credentials from your environment: `X_USERNAME` and `X_PASSWORD`
3. Complete any verification steps if prompted — if you hit a CAPTCHA or 2FA you can't solve, stop and DM Nolan immediately
4. Once logged in, the session persists — do not log out

On subsequent runs, navigate directly to `https://x.com/home` and verify you're still logged in as `@OttawaBlockchain` before proceeding.

## Browsing the watchlist

Read the watchlist from `x-social/watchlist.md` in your workspace. For each account:

1. Navigate to `https://x.com/<handle>`
2. Read the 5–10 most recent posts
3. Note anything posted since your last browse (check `x-social/last-browse.md` for the timestamp)
4. Evaluate each post against the repost criteria below

After browsing all accounts, update `x-social/last-browse.md` with the current timestamp.

## Repost criteria — OB's vibe

Repost only if the post fits **at least one** of these categories AND passes all the filters below.

**Categories (what OB cares about):**
- Ottawa or Canadian tech/Web3 community news — events, meetups, local ecosystem moves
- Builder and developer content — protocols, open source, dev tools, technical deep dives
- Blockchain education — explainers, threads that inform and don't assume hype
- Meaningful industry news — regulation, significant launches, funding that shifts the space

**Filters (automatic disqualifiers):**
- Price talk, "to the moon", buy/sell signals — skip it
- Influencer hype with no substance — skip it
- Anything that would embarrass a credible community org — skip it
- Already reposted (check `x-social/repost-log.md`) — skip it
- Posted before your last browse timestamp — skip it

**When in doubt, skip.** One strong repost a day beats three mediocre ones. OB's feed should feel like a well-curated community board, not a firehose.

## Reposting

1. Navigate to the post
2. Click the repost button (the two-arrow icon under the post)
3. Select "Repost" (not "Quote" unless you have something genuinely worth adding)
4. Log the repost in `x-social/repost-log.md`: `YYYY-MM-DD HH:MM | @handle | post URL | one-line reason | [repost]`

## Posting original content

Only post original content when a team member explicitly asks via Discord DM. Do not initiate unprompted.

- Keep it short — X is not a blog
- Match OB's voice: community-focused, informative, never hype-y
- Confirm the draft with the requester before posting
- Log the post in `x-social/repost-log.md` with type `[original]`

## Daily limit

Max 3 actions per day (reposts + originals combined). Quality over quantity.

## What not to do

- Do not engage with replies or mentions unless Nolan explicitly asks
- Do not follow or unfollow accounts
- Do not like posts
- Do not post anything about price, investment advice, or "don't miss this"
- Do not store or log credentials anywhere — read them from env vars only
