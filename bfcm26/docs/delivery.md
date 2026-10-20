# Delivery ("push to clickup and frame")

- **Frame.io:**
  - **Login:** the token broker on Eli's Cloudflare (`https://frameio-broker.eli-054.workers.dev`, code in `bfcm26/tools/frameio-broker/`) holds the Adobe login and renews it daily, so no codes are needed.
    - Helpers get an access token with `client.token()`. It authenticates via an HMAC of `FRAMEIO_OAUTH_CLIENT_SECRET`, so run it in a fresh helper session that has the Brilanc keys.
    - `client.status()` shows the health.
    - If it ever says it's not connected, Eli opens `/login` once.
    - Never print tokens.
  - Then use the V4 API `https://api.frame.io/v4` with a custom User-Agent (the default Python UA gets 403). Project `9db7c232-de65-4e59-99e7-4fd3c3155ac7`.
  - The batch folder link is the Creatives field on the ClickUp batch task. Inside it, the version with text goes to the existing `EN` folder and the clean version to `No Text`. Never create folders.
- **ClickUp (Cavaier → Ads → Ads, under the week task, e.g. "Week 40"):**
  - **Batch task** fields:

    | Content | Field name | Field ID |
    |---|---|---|
    | Primary text | Preview Text | `2d5ca05c` |
    | Headline | Subject Line | `7d30ba47` |
    | Description | Description | `b416b8ee` |

  - **URLs go on the C rows, never on the batch task (Eli, Oct 15):** set EU URL `f2627d19` and US URL `5d08f6f8` on each C1–C3 row, pointing at the color variant shown in that ad (`?variant=<id>`, size Medium). The batch task's EU/US URL fields stay empty; clear them if they are filled. Check the finish in the ad itself (frames or photo), not the copy note. Variant ids (Medium):

    | Product | Color | EU variant | US variant |
    |---|---|---|---|
    | 2x-duo-minimal-set-for-her | Gold | 54997777088858 | 67679698518329 |
    | 2x-duo-minimal-set-for-her | Silver | 54997776990554 | 67679698420025 |
    | 2x-duo-minimal-set-for-her | Black | 54997776892250 | 67679698321721 |
    | 2x-duo-minimal-set-for-him | Gold | 54745039634778 | 54444623298873 |
    | 2x-duo-minimal-set-for-him | Silver | 54745039536474 | 54444623200569 |
    | 2x-duo-minimal-set-for-him | Black | 54745039438170 | 54444623102265 |
    | 3x-minimal-stack-set-for-her | Gold | 54372825530714 | 53480346583353 |
    | 3x-minimal-stack-set-for-her | Silver | 54372825629018 | 53480346681657 |
    | 3x-minimal-stack-set-for-her | Black | 54326091907418 | 53480346485049 |

    Other products (e.g. the men's stack): read the ids from `https://<store>/products/<handle>.js`.
  - **C1–C3 rows:** set Creative Style `751230a2`, Angle `80f8a7e8`, Creative Origin `1971e67f` (Imitation for IM8-based work, video versions included), Funnel Stage `498a0712` and Offer `1ce1ec23`. For Black Friday (BFCM) work, Creative Style and Angle are always the "Black Friday" option (Style `904046e4`, Angle `64f25149`). Add one short, clean comment: the IM8 ad it imitates plus what it tests. No tool names (Seedance, Claude). No Frame links in the rows. Don't rename rows or change Editor/status unless asked.
  - **Mother status after Frame:** when every creative of the batch (EN and No Text) has uploaded to Frame.io without any issue, set the batch task (mother) status to "ads for review", but only if it is currently "to do". Any other status stays as it is.
  - **Batch task (mother) mirrors the rows:** for each of those five fields (Style, Angle, Origin, Funnel, Offer; never the URLs), if C1, C2 and C3 all have the same value, set that same value on the batch task too. If they differ, leave the batch task's field as it is.
