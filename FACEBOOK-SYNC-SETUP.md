# Facebook announcement sync — setup

The website side is already live. The announcement card is on both
`index.html` and `announcements.html`, and it reads `announcement.json`.

The automated Facebook update needs one credential that only the Page owner
can create: a **Facebook Page access token** for Page ID `100064645061857`
with the `pages_read_engagement` permission.

The workflow deliberately skips while that token is missing, so it does not
email a failure every 30 minutes.

---

## 1. Get a Page access token

### Option A — permanent System User token (recommended)

Use this for a token that keeps working without maintenance.

1. Open <https://business.facebook.com/settings>.
2. Go to **Users → System Users → Add**.
3. Name it something clear, for example `RPAI Website`.
4. Click **Assign Assets** and give it:
   - the Meta app: **Full control**
   - the Facebook Page **ROYAL Priesthood** (`100064645061857`): **Manage Page** or **Full control**
5. Click **Generate New Token**, choose the app, and tick:
   - `pages_show_list`
   - `pages_read_engagement`
   - `business_management`
6. Set the expiry to **Never** if Meta offers it.
7. Copy the token. Do not paste it into a file in this repository.

If you already created a System User for the WhatsApp bot, you can reuse it:
add the Facebook Page asset and the two `pages_*` permissions, then generate a
new token.

### Option B — Graph API Explorer (quick test)

Use this to test the setup today. The token may expire, so replace it with a
System User token before relying on the schedule.

1. Create or open a Meta app at <https://developers.facebook.com/apps>.
2. Open <https://developers.facebook.com/tools/explorer>.
3. Select the app in the top-right.
4. Click **Get User Access Token** (or **Generate Access Token**) and grant
   `pages_show_list` and `pages_read_engagement`.
5. Run this query:

   ```text
   me/accounts
   ```

6. Find the Page named **ROYAL Priesthood** with ID `100064645061857`.
7. Copy the `access_token` value next to that Page.

To check how long the token lasts, paste it into
<https://developers.facebook.com/tools/debug/accesstoken> and click **Debug**.

---

## 2. Validate the token before adding it

Open this URL in a browser, replacing `YOUR_TOKEN`:

```text
https://graph.facebook.com/v26.0/100064645061857/posts?fields=message,updated_time&limit=1&access_token=YOUR_TOKEN
```

A working token returns JSON beginning with:

```json
{
  "data": [
    {
      "message": "...",
      "updated_time": "...",
      "id": "..."
    }
  ]
}
```

If you see an error, fix the token or permissions before adding the secret.

---

## 3. Add the token to GitHub

1. Open
   <https://github.com/NDUWAMAKINKA/royal-priesthood-assemblies-int-l/settings/secrets/actions>.
2. Click **New repository secret**.
3. Name: `FB_PAGE_ACCESS_TOKEN`
4. Value: the Page access token.
5. Click **Add secret**.

The Page ID is already built into the workflow. You only need `FB_PAGE_ID` as
an optional secret if the church ever moves to a different Facebook Page.

---

## 4. Run the sync once

1. Open
   <https://github.com/NDUWAMAKINKA/royal-priesthood-assemblies-int-l/actions/workflows/sync-announcements.yml>.
2. Click **Run workflow**.
3. Choose the `main` branch and click **Run workflow** again.

A successful run either:

- commits a new `announcement.json`, or
- says `announcement.json is already current. Nothing to do.` when the newest
  Facebook text post is not newer than the current announcement.

After that, the workflow runs every 30 minutes. GitHub may delay scheduled runs
at busy times, and it disables schedules after 60 days without repository
activity. Run the workflow manually once if the site has been quiet for a long
time.

---

## Troubleshooting

| Message | Meaning | Fix |
|---------|---------|-----|
| `FB_PAGE_ACCESS_TOKEN is not configured` | The GitHub secret is missing | Add the secret in step 3 |
| `OAuthException`, code `190` | Token expired or was revoked | Generate a new token; prefer a System User token |
| `(#10) ... pages_read_engagement` | Permission missing or not approved | Grant the permission to the app/System User; complete App Review if Meta asks |
| `No text announcement on the Page` | The newest posts are photo-only or empty | Publish a text update, or wait for the next text post |
| `announcement.json is already current` | The Facebook post is older than the current manual notice | Publish a newer post, or make the timestamp in `announcement.json` older |
| Push fails with `protected branch` | Branch protection blocks GitHub Actions | Allow the Actions bot to push to `main`, or relax the rule for this workflow |
| `Resource not accessible by integration` | Workflow permissions are too narrow | Keep `permissions: contents: write` in the workflow |

---

## Manual fallback

The site does not depend on Facebook. To publish immediately, edit
`announcement.json`:

```json
{
  "message": "Sunday service moves to 8am from 1 December.",
  "timestamp": "2026-10-25T21:35:00Z"
}
```

Commit and push. Both announcement cards refresh from that file on the next
page load. The card also keeps a static copy, so it still displays if the JSON
request fails.
