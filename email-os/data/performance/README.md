# Performance data

The analyst writes one file per month, `YYYY-MM.yaml`, from Klaviyo campaign reports
(and Triple Whale for revenue attribution). The planner points every calendar row's `why`
at a row here: `perf:2026-10#<row id>`.

```yaml
month: 2026-10
source: [klaviyo:get_campaign_report, triplewhale:pixel-attribution]
rows:
  - id: w42-duo-everyday            # stable id the calendar can cite
    klaviyo_name: KA_W42_Oct13_T01
    market: eu
    sent: 2026-10-13
    hero_product: 2x-duo-minimal-set-for-him
    angle: "Two bracelets. Every day."
    recipients: 0                   # numbers copied from the report, never estimated
    open_rate: 0.0
    click_rate: 0.0
    orders: 0
    revenue: 0.0
    currency: EUR
takeaways:                          # one line each, each citing row ids
  - "…"
```
