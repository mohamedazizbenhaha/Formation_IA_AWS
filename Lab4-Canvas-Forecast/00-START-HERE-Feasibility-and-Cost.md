# Lab 4 — Setup, Feasibility & Cost
### Creating a forecast with Amazon SageMaker Canvas

**Read this before you open Canvas.** Canvas is the most expensive thing you
have run in this course, and it has a cost trap that none of the other labs
have. Ten minutes here protects your credits.

---

## 1. The short answer: yes, proceed — but this one actually costs money

**You can run this on your account.** Canvas needs no `ml.*` quota increase,
and your $100 credit balance is ample.

But be clear-eyed about the difference in scale:

| Activity | Cost |
|---|---|
| Module 3 (all 7 labs) | ~$0.22 |
| Labs 5 + 6 | ~$0.10 |
| **Lab 4 (Canvas forecast)** | **~$2–$6** |

That is **20–60× everything else in the course combined** — and still only
about 2–6% of your balance. It is affordable. It is just not free, and it is
the first thing in this course where carelessness has a real price.

### Why Canvas costs more

Every other lab used either a cheap instance or a per-request API. Canvas bills
two things at once:

| Component | Rate | Notes |
|---|---|---|
| **Workspace session** | **~$1.90/hour** | Runs until you explicitly **Log out** |
| **Model build (training)** | **~$2–$19** per build | AWS's published examples for tabular/time-series datasets |

The workspace rate is roughly **38× the `ml.t3.medium`** notebook instance you
used in Module 3.

### The free tier helps a lot

New Canvas users get **160 workspace session-hours per month for 2 months**.
That very likely covers your entire session cost, leaving only the build
charge.

> ⚠️ **The free tier covers session hours only — not the model build.** Expect
> to pay the build charge regardless.

---

## 2. 🔴 The one thing that can actually hurt you

> ### Canvas bills by the hour until you click **Log out**.
> **Closing the browser tab does not stop it. Signing out of the AWS console
> does not stop it. Shutting your laptop does not stop it.**

This is worse than the SageMaker endpoint trap in Lab 3.5, because the hourly
rate is far higher.

| Workspace left running | Cost |
|---|---|
| Overnight (14 hrs) | **$26.60** |
| A weekend (60 hrs) | **$114** — *more than your whole balance* |
| A week | **$319** |
| A month | **$1,368** |

Your 160 free hours = **6.7 days**. A workspace forgotten on a Friday burns
through the free tier and into real charges before you are back on Monday.

**The rule: the very last thing you do in Canvas, every single time, is
click your profile icon → Log out.** Not close the tab. Log out.

The guide reminds you at every natural stopping point.

---

## 3. Cost-minimising choices this lab makes

| Decision | Why | Saves |
|---|---|---|
| **Quick build**, not Standard | 2–20 min vs **2–4 hours** | The single biggest lever |
| Small dataset (2,190 rows) | Build cost scales with data size | Keeps you at the low end of $2–$19 |
| Dataset prepared in advance | No Data Wrangler session time | ~30 min of workspace time |
| Log out during any long wait | Builds continue without the workspace | ~$1.90/hr of idle time |
| Delete the domain afterwards | Removes lingering EFS storage | Pennies/month, but tidy |

### Quick build vs Standard build

| | Quick build | Standard build |
|---|---|---|
| Time | **2–20 minutes** | **2–4 hours** |
| Accuracy | Good | Generally better |
| Models tried | Fewer | Up to 250 |
| Workspace cost if you wait | ~$0.60 | **~$4–8** |

**Use Quick build.** For a teaching lab the workflow is the point, not
the last percent of accuracy. Quick build *is* supported for time-series
forecasting — you do not have to use Standard.

> If you ever do run a Standard build: **start it, then log out.** The build
> continues on separate training infrastructure. Log back in when it is done.
> Sitting in the workspace watching a 4-hour progress bar costs ~$7.60 in
> session time for nothing.

---

## 4. Before you start — a 5-minute setup

**Step 1 — Region.** Top-right of the console: **US East (N. Virginia) /
`us-east-1`**.

**Step 2 — Budget alarm. Do this one properly this time.**
Billing and Cost Management → **Budgets** → **Create budget**:
- Template: **Monthly cost budget**
- Amount: **$10** *(higher than the $5 used for other labs — Canvas legitimately
  costs more, and you do not want alert fatigue)*
- Alert at **80%**
- Your email — **and confirm the subscription email AWS sends**

**Step 3 — Check your credit balance.** Billing → **Credits**. You should still
see close to $100.00 remaining, expiring 31 Aug 2027.

**Step 4 — Decide your budget for this exercise.** A sensible cap is **$10**.
If you plan to let a class of students each build a model, multiply
accordingly — 20 students × one build each is potentially **$40–$200**. For a
class, **demonstrate it once yourself** rather than having everyone build.

---

## 5. What you need that the official material does not give you

The AWS Academy version of this is a **click-through simulation** — a recorded walkthrough,
not a live AWS environment. It gives you no dataset and no account. To do it for
real you need:

| Needed | Status |
|---|---|
| A forecast-ready dataset | ✅ **Generated** → `data/` |
| A SageMaker Domain | You create it — guide Step 1 |
| Canvas permissions | Comes with the domain's execution role |
| `ml.*` quota | **Not required** |

### The dataset

`data/retail_sales_history.csv` — 2 years of daily sales for 3 products.

| Column | Role in Canvas | Notes |
|---|---|---|
| `date` | **Timestamp** | `YYYY-MM-DD` — an accepted Canvas format |
| `item_id` | **Item ID** | 3 products, 730 rows each |
| `units_sold` | **Target** | What you forecast |
| `price` | Future value | Known in advance → enables what-if |
| `promotion` | Future value | 0/1 flag |
| `day_of_week` | Future value | Derived; optional |

`data/retail_sales_with_future.csv` — the same plus 60 future days per item
where `units_sold` is blank but `price` and `promotion` are filled in. Use this
one if you want the **what-if analysis** feature.

**The data is synthetic, and deliberately so.** It has known, verifiable
structure built into it, which means you can check whether the model found the
right patterns — something you can never do with real data:

| Pattern built in | Verified in the data |
|---|---|
| Weekend uplift | Cola 147 → 220 units (+50%) |
| Promotion uplift | Cola 147 → 359 units (~2.4×) |
| Annual seasonality | Ice cream 17 units (Jan) → 102 (Jun) |
| Upward trend | Cola Aug 2024 192 → Aug 2025 248 |
| Price elasticity | Built in per item |
| Flat-ish item | Chips has weak annual seasonality — a control |

See `dataset_preview.png` for the shape of it.

---

## 6. Honest limits of what was verified

| Verified | How |
|---|---|
| Dataset generated and statistically checked | Executed; all six patterns confirmed present |
| Canvas format requirements | Checked against AWS docs — timestamp/item ID/target columns, accepted date formats |
| Row counts vs Canvas minimums | 730/item, well above the 50-row Standard-build minimum |
| Quick build supported for time series | Confirmed in AWS docs |
| Pricing figures | From AWS's Canvas pricing page |

**Not verified: the Canvas UI itself.** I have not run this in your account, and
Canvas's interface changes more often than most AWS consoles. **Treat button
names and menu positions as a close guide, not gospel** — if a label differs
slightly, the surrounding logic still holds. Rehearse once before teaching it.

---

## 7. The cleanup ritual — non-negotiable

**Every time you finish, in this order:**

1. **Canvas → profile icon (bottom left) → Log out** ← stops the $1.90/hr
2. Console → **SageMaker AI → Domains → your domain → User profiles →**
   confirm no Canvas app shows **InService**
3. When completely finished: **delete the Canvas app**, then the **user
   profile**, then the **domain**
4. **Tomorrow: Billing → Bills** → confirm the figure matches expectations

If step 2 shows an app still `InService`, delete it there. That is your
backstop if the Log out did not take.

---

**Next:** [`Lab-4-Canvas-Forecast.md`](Lab-4-Canvas-Forecast.md)

---

*Prices are us-east-1 and approximate; confirm on the
[SageMaker Canvas pricing page](https://aws.amazon.com/sagemaker-ai/canvas/pricing/).
Adapted for use outside the AWS Academy environment. Original course content
© Amazon Web Services, Inc.*
