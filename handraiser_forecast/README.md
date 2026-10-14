# Softened handraiser growth for FY27

This folder turns quarterly handraiser actuals into a growth rate for next year. The rate starts from the latest year-over-year change, then three guards pull a steep quarter back toward something that can be used as a target.

The count is handraisers. The files call that count `leads` because the forecast multiplies it. It is not every Salesforce lead.

## What went into the count

A handraiser is one person responding to one of these campaigns:

- n8n Embed Contact Us Form
- n8n Talk to Sales Web Form
- n8n license@n8n.io inbound email
- n8n sales@n8n.io inbound email

Paid LinkedIn campaigns are excluded. The date is `first_responded_date`. A person can be a lead, a contact, or an email, and is counted once per quarter. Suspects, deleted leads, free-mail domains, and n8n test addresses are excluded.

Employee count sets the segment: Self-Service 0–100, Commercial 101–1,000, Mid-Market 1,001–5,000, Enterprise 5,001+, Unknown when no count is on file. Region is US+LATAM+ANZ, EMEA+ASIA, or Unknown. The fiscal year starts in January, so the quarters are calendar quarters.

History runs from 2025 Q1 through 2026 Q3. 2026 Q4 is still open and is not in the file. That is seven quarters. Eight trailing year-over-year rates are the preferred anchor, and this file does not have them yet, so the anchor is 0%. The column `ttm_yoy` is the rate actually used. Today that is the same quarter versus a year earlier (2026 Q3 versus 2025 Q3). A trailing-twelve-month comparison needs 2024, which these campaigns do not have.

## How the rate is softened

For each region, a segment’s year-over-year rate is blended toward that region’s all-segments rate. The blend trusts a segment in proportion to its trailing volume. `k` is the volume that counts as half trust. Left unset, `k` is the median segment volume in that region.

The blended rate then fades toward the anchor. One quarter ahead keeps 75% of the gap to the anchor, two quarters ahead keep 75% of that, and so on through quarter four. The faded rate is held inside −20% to +25%. When the hold binds, `clamped_flag` is true.

Three scenarios change only that fade, and in one case the anchor:

| Scenario | Fade (`phi`) | Anchor |
| --- | --- | --- |
| Conservative | 0.60 | The eight-quarter median, and never above 0% |
| Neutral | 0.75 | The eight-quarter median, which is 0% until eight rates exist |
| Optimistic | 0.85 | The eight-quarter median |

The handraiser forecast is last year’s same quarter times one plus the faded rate, rounded half up. FY27 Q4 has a rate and a blank count: FY26 Q4 has not closed, so there is no base to multiply. `All segments` is the sum of the rounded segment counts. It is not grown on its own.

## FY27 Q1–Q3 for the focus cells

Neutral, handraisers. Q4 is blank in the file on purpose.

| Region | Segment | 2026 Q3 vs 2025 Q3 | After blend | 2027 Q1 | 2027 Q2 | 2027 Q3 | Q1–Q3 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| US+LATAM+ANZ | Mid-Market | −72.7% | −69.8% | 244 | 174 | 130 | 548 |
| US+LATAM+ANZ | Enterprise | −63.7% | −65.4% | 224 | 153 | 158 | 535 |
| EMEA+ASIA | Mid-Market | −47.4% | −54.6% | 232 | 174 | 172 | 578 |
| EMEA+ASIA | Enterprise | −45.7% | −53.4% | 256 | 198 | 173 | 627 |

Those Q1–Q3 counts are −20% versus the same three quarters of FY26. The fade from a −45% to −70% start is still below −20% three quarters out, so the floor sets every published quarter. Neutral and optimistic therefore publish the same Q1–Q3 counts for these four cells. Conservative fades faster, comes off the floor in Q3, and lands a little higher: US Mid-Market 556, US Enterprise 547, EMEA Mid-Market 596, EMEA Enterprise 647.

The full grid, including Self-Service, Commercial, and the blank Q4 rates, is in `output/forecast_growth.csv`.

## Unknown region

Do not use the Unknown region as a demand target. In 2026 Q3, Unknown-region Self-Service is 1,404 handraisers, against 368 a year earlier. From August 2026, responses with no country started receiving an employee count, so people moved between Unknown and a named size. The +25% cap then carries that jump forward (1,755 in the neutral 2027 Q3 cell). Named regions also show the other side of that move: the Unknown employee-count segment falls to a handful of people in 2026 Q2 and Q3.

## Did softening fit the recent quarters better?

A four-quarter holdout needs eight earlier quarters. This file can score two: 2026 Q2 and 2026 Q3, using only the rate known at the end of 2026 Q1. That Q1 rate was the jump off a small 2025 Q1 base, so both methods guessed too high.

Mean absolute percent error, two quarters:

| Region | Segment | Plain year-over-year | Softened |
| --- | --- | --- | --- |
| US+LATAM+ANZ | Mid-Market | 535% | 251% |
| US+LATAM+ANZ | Enterprise | 345% | 193% |
| EMEA+ASIA | Mid-Market | 270% | 121% |
| EMEA+ASIA | Enterprise | 194% | 93% |

Softened was closer on all four focus cells, and still about twice to three times the actual. Across all 15 region and segment cells, softened was worse on 4. The painful ones are the Unknown employee-count segment in US+LATAM+ANZ (4,300% plain, 17,344% softened) and in EMEA+ASIA (10,476% plain, 27,171% softened). Blending those collapses toward the regional total hid a real drop in people with no employee count. Self-Service in those two regions was only slightly worse. Detail is in `output/backtest_mape.csv` and `output/backtest_detail.csv`.

## Change the assumptions

All of the knobs live in the `CONFIG` dictionary at the top of `growth_softening.py`.

- `phi` — how fast a shock fades. Allowed range is 0.50 to 0.95. Lower fades toward the anchor sooner.
- `k` — volume that counts as half trust. `None` uses the median segment trailing volume in the region. Set a number to force one threshold.
- `anchor_mode` — `median_8q` uses the median of the last eight trailing-twelve-month rates, and uses 0% until those eight exist. `zero` forces 0%. Any other word uses `fixed_anchor`.
- `floor` and `cap` — the hold, as decimals. Defaults are −0.20 and 0.25.
- `scenarios` — each entry can set `phi` and `anchor_cap_at_zero`. Add a scenario by adding a key.

Refresh the history by running `forecast.sql` in BigQuery for quarters that have fully closed, and saving the result as `data/quarterly_handraisers.csv` with columns `region`, `segment`, `fiscal_year`, `fiscal_quarter`, `leads`. Keep the `All segments` row. Then, from this folder:

```bash
python3 -m pytest
python3 growth_softening.py
```

The second command rewrites the three files in `output/`.
