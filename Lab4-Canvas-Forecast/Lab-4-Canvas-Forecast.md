# Lab 4 — Creating a Forecast with Amazon SageMaker Canvas
### Personal AWS account edition — full step-by-step

> **Read first:** [`00-START-HERE-Feasibility-and-Cost.md`](00-START-HERE-Feasibility-and-Cost.md)
> This exercise costs **~$2–$6**, and has a **$1.90/hour** meter that only
> stops when you click **Log out**.

**Duration:** ~60 minutes (about 20 minutes of that is waiting for the build)
**Cost:** ~$2–$6 · **Quota needed:** none

---

## What you are building

A **time-series forecasting model**, with no code, that predicts daily unit
sales for three retail products 30 days into the future — then using it to
answer a business question: *what happens to sales if we cut the price?*

## Objectives

- Create a SageMaker Domain and launch Canvas
- Import a dataset
- Configure a time-series forecast (target, item ID, timestamp, horizon)
- Build a model with **Quick build**
- Interpret forecasting accuracy metrics
- Read single-item and all-item forecasts
- Run a what-if analysis
- **Shut everything down properly**

## The business scenario

You manage stock for a convenience store chain. You have two years of daily
sales for three products:

| Product | Behaviour |
|---|---|
| `BEV-COLA-330` | Cola — strong weekends, strong summer |
| `SNK-CHIPS-150` | Crisps — steady all year *(the control)* |
| `ICE-VANIL-500` | Ice cream — **heavily** seasonal |

You need a 30-day forecast to decide what to order.

---

# Part 1 — Set up Canvas

## Step 1 — Create a SageMaker Domain

Canvas runs inside a **SageMaker Domain** — a workspace holding user profiles,
storage and permissions. You need one before Canvas will open.

1. Console → search **SageMaker AI** → open it
2. Confirm the region is **US East (N. Virginia)** (top right)
3. Left navigation → **Domains**
4. **Create domain**
5. Choose **Set up for single user (Quick setup)**
6. **Create**

**This takes 3–10 minutes.** AWS provisions a domain, a default user profile, an
execution role, and an EFS volume behind the scenes.

> **Quick setup is right here.** The custom path asks about VPCs, subnets and
> encryption — all unnecessary for this exercise.

> **No charge yet.** A domain costs nothing to exist. Billing starts only when
> the Canvas *application* launches in Step 2. (The EFS volume costs a few cents
> a month; the cleanup section removes it.)

**If it fails:** the most common cause is a brand-new account with no default
VPC. Console → **VPC → Create default VPC**, then retry.

## Step 2 — Launch Canvas ⏱️ THE METER STARTS HERE

1. **Domains → your domain → User profiles** tab
2. On the `default-...` profile row: **Launch → Canvas**

Canvas opens in a new tab. First launch takes **1–3 minutes**.

> ### 🔴 From this moment you are billed ~$1.90/hour.
> It stops when — and only when — you click **Log out** (Step 12).
> Closing this tab does **not** stop it.

**Glance at the clock now and note the time.** Knowing you started at 14:20
makes it obvious later whether you are 40 minutes or 4 hours in.

---

# Part 2 — Import the data

## Step 3 — Upload the dataset

1. Canvas left navigation → **Data Wrangler** (or **Datasets** in some versions)
2. **Import data → Tabular**
3. Choose **Local upload** *(or Amazon S3 if you prefer)*
4. Select **`data/retail_sales_history.csv`**

   > Want to try the **what-if** feature in Step 10? Upload
   > **`retail_sales_with_future.csv`** instead — it adds 60 future rows with
   > `price` and `promotion` filled in but `units_sold` blank.

5. **Import**

Upload takes a few seconds — the file is about 100 KB.

## Step 4 — Check the data landed correctly

Click the dataset to preview it. Confirm:

- [ ] **2,190 rows** (730 days × 3 products)
- [ ] **6 columns**: `date`, `item_id`, `units_sold`, `price`, `promotion`, `day_of_week`
- [ ] `date` is recognised as a **date/timestamp**, not a string
- [ ] No missing values

> **If `date` shows as string/object**, Canvas may still accept it — the format
> is `YYYY-MM-DD`, which is on Canvas's supported list. If it complains later,
> set the column type to timestamp in Data Wrangler.

**Do not spend time exploring here.** Data Wrangler is powerful but it runs on
the same $1.90/hour meter, and this dataset is already clean. Everything worth
seeing is in `dataset_preview.png`, which costs nothing to look at.

---

# Part 3 — Build the model

## Step 5 — Create the model

1. Left navigation → **My Models** → **New model**
2. **Model name:** `retail-demand-forecast`
3. **Problem type:** **Predictive analysis**
4. **Create**
5. Select your dataset → **Select dataset**

## Step 6 — Configure the forecast ← the important screen

This is where the exercise actually happens. Four settings:

### 6a. Target column

Set **Target column** to **`units_sold`**.

This is what you are predicting. Canvas should now suggest **Time series
forecasting** as the model type, because it has detected a date column and
repeated item identifiers.

### 6b. Choose the model type

If not already selected, choose **Time series forecasting**, then
**Configure**.

### 6c. The three time-series settings

| Setting | Choose | What it means |
|---|---|---|
| **Item ID column** | `item_id` | Which column separates one series from another. Canvas builds a forecast *per item*. |
| **Time stamp column** | `date` | Which column carries time. |
| **Forecast horizon** | **30** | How many periods ahead to predict. Data is daily, so 30 = 30 days. |

> **The item ID is the concept people miss.** You are not building one model
> over 2,190 rows. You are building forecasts for **three separate series** of
> 730 days each. Without `item_id`, Canvas would blend three unrelated products
> into one meaningless average.

> **On horizon:** accuracy degrades the further out you predict. 30 days on 730
> days of history is a sensible ratio. Asking for 365 days from 730 would be
> optimistic — a good discussion point.

### 6d. Holidays (optional)

If offered a **holiday schedule**, you may add a country. It genuinely helps
retail forecasts. Skip it if you want to keep this run simple.

**Save** the configuration.

## Step 7 — Preview the model (free, 2 minutes, worth it)

If a **Preview model** button is available, click it.

This runs a fast estimate and shows **column impact** — which columns carry
predictive signal — **without doing a full billed build**. Two minutes here can
save you a build on a badly-configured model.

Expect `price`, `promotion` and the date-derived features to matter, and
`day_of_week` to be partly redundant (Canvas derives day-of-week from `date`
itself).

## Step 8 — Quick build ⏱️

1. Click **Quick build**

> ### Choose Quick build, not Standard.
> | | Quick | Standard |
> |---|---|---|
> | Time | **2–20 min** | **2–4 hours** |
> | Workspace cost while waiting | ~$0.60 | **~$4–8** |
>
> Quick build fully supports time-series forecasting. Standard build buys a
> modest accuracy gain for roughly 10× the wait.

**While it builds (10–20 minutes):**

- ☕ **Stay logged in.** For a 20-minute Quick build, logging out and back in
  wastes more time than it saves.
- Do **not** start a second build "to compare" — that doubles the cost.
- If it somehow exceeds ~40 minutes, something is wrong: log out, and
  investigate before rebuilding.

---

# Part 4 — Read the results

## Step 9 — Interpret the accuracy metrics

When the build finishes you land on the **Analyze** tab.

### The metrics, in plain language

| Metric | Full name | What it means | Better |
|---|---|---|---|
| **wQL** | Weighted Quantile Loss | Average error across prediction *intervals*, not just the middle guess. Canvas's headline metric for forecasting. | Lower |
| **MAPE** | Mean Absolute Percentage Error | Average error as a **percentage**. MAPE 0.15 = about 15% off. | Lower |
| **WAPE** | Weighted Absolute Percentage Error | Like MAPE but weighted by volume, so high-selling items count more. Far more robust when some values are near zero. | Lower |
| **RMSE** | Root Mean Squared Error | Error in **units sold**. Punishes big misses hard. | Lower |
| **MASE** | Mean Absolute Scaled Error | Error **relative to a naive forecast**. **< 1 means you beat naive; > 1 means you did worse.** | Lower |

### How to actually judge your model

**Look at MASE first.** It is the only metric that answers the question that
matters: *is this model better than doing nothing?*

The naive forecast is "tomorrow will be like today" (or like last week). A model
with **MASE ≥ 1 has failed** — it is worse than a rule a shopkeeper could apply
in their head. This is the same lesson as the majority-class baseline in
Lab 3.6: **a number is only meaningful against a baseline.**

Then look at **WAPE** for a business-readable error, and prefer it to MAPE here
because ice cream sales drop near zero in winter — and MAPE behaves badly when
actual values approach zero.

> **A realistic result on this dataset:** WAPE in the region of 0.10–0.25
> (10–25% average error) and MASE below 1. If MASE is above 1, check that
> `item_id` was set correctly — blending the three products is the usual cause.

### Column impact

The **Column impact** panel shows what the model leaned on. Check it against
what you know is really in the data:

| Should matter | Because |
|---|---|
| `price` | Real elasticity is built in |
| `promotion` | Promotions roughly **2.4×** sales |
| `date` | Weekly + annual seasonality |

If `promotion` shows near-zero impact, the model missed a pattern you *know*
exists. That is a genuine finding, not a failure of the exercise — and a good
thing to point out to students.

## Step 10 — Look at the forecasts

Go to the **Predict** tab.

### Single item

1. Choose **Single item**
2. Select **`ICE-VANIL-500`** first — it is the most visually dramatic

You get a line chart: history, then the forecast, wrapped in a shaded
**confidence interval** (typically p10–p90).

**Teach the confidence interval.** The band is not decoration. It says *"we
expect the true value to land in here most of the time."* A forecast with a
huge band is telling you it does not really know — and a wide band is often
more honest and more useful than a confident single line. For stock ordering,
you would order against the upper bound of the band, not the middle.

Now compare:

| Item | What to look for |
|---|---|
| `ICE-VANIL-500` | Strong seasonal swing; did the model continue it? |
| `BEV-COLA-330` | Weekly sawtooth — weekend peaks should persist |
| `SNK-CHIPS-150` | Flat. A boring forecast here is the **correct** one |

That last row matters. Students often assume a flat forecast means the model
failed. For crisps, flat is right — the data really is flat. **A good model
mirrors the structure that exists, and no more.**

### All items

Switch to **All items** for a combined view, then **Download** the predictions
as CSV if you want them.

## Step 11 — What-if analysis *(only with `retail_sales_with_future.csv`)*

This is the payoff — the part that turns a forecast into a business tool.

1. In the **Predict** tab, find **What-if analysis**
2. Select `BEV-COLA-330`
3. Change a future **`price`** value — try cutting it by 25%
4. Watch the forecast respond

Because price elasticity is genuinely present in the data, a price cut should
visibly lift predicted units.

**The business question this answers:** *"If we discount cola 25% next month,
how many extra units do we sell — and is the extra volume worth the lost
margin?"* That is a question a spreadsheet cannot answer and a forecast can.

Try the same with `promotion` set to `1` on future dates.

---

# Part 5 — Shut down ⛔ DO NOT SKIP

## Step 12 — Log out of Canvas

> ### This is the single most important step in this guide.

1. In Canvas, click your **profile icon (bottom-left)**
2. Click **Log out**

**Not** closing the tab. **Not** signing out of AWS. **Log out, inside Canvas.**

| If you forget | Cost |
|---|---|
| Overnight | **$26.60** |
| A weekend | **$114** |
| A week | **$319** |

## Step 13 — Verify it actually stopped

Never trust step 12 alone.

1. Console → **SageMaker AI → Domains → your domain**
2. **User profiles** tab → click the `default-...` profile
3. Look at the **Apps** list

You want the Canvas app showing **Deleted**, or absent. **If it says
`InService`, it is still billing** — click **Delete app** right now.

## Step 14 — Full teardown (when finished for good)

Keeping the domain is fine — a domain with no running app costs only a few
cents a month for EFS. But if you are done:

1. **Delete the Canvas app** (Step 13)
2. **Delete the user profile**
3. **Delete the domain** — SageMaker AI → Domains → select → **Delete**
4. Optionally delete the `sagemaker-...` S3 bucket the domain created

## Step 15 — Check the bill tomorrow

**Billing and Cost Management → Bills → SageMaker.**

Expect roughly **$2–$6**. If you see materially more, something ran longer than
you thought — and now you know to check the app status sooner next time.

---

# Discussion questions

1. **MASE came out below 1. Why does that matter more than a low MAPE?**
   *(It proves the model beats a naive forecast. Low MAPE alone could still be
   worse than "same as last week".)*
2. **Why WAPE rather than MAPE on this dataset?**
   *(Ice cream sales approach zero in winter; percentage error explodes when
   the denominator is tiny. WAPE weights by volume and stays stable.)*
3. **The crisps forecast is almost flat. Good model or bad model?**
   *(Good. The series really is flat. Inventing seasonality that is not there
   would be worse.)*
4. **The confidence band widens further into the future. Why?**
   *(Uncertainty compounds. Each step ahead relies on the last, so errors
   accumulate.)*
5. **You forecast 30 days from 730 days of history. Could you forecast 365?**
   *(You *can*. It would be far less reliable — you would have only two annual
   cycles to learn yearly patterns from.)*
6. **This took ~20 minutes and no code. When would you still write code
   instead?** *(Custom features, unusual loss functions, integration into a
   pipeline, reproducibility under version control, cost at scale.)*
7. **What is missing from this dataset that a real retailer would have?**
   *(Weather, competitor pricing, stock-outs, local events, holidays, marketing
   spend.)*

---

# Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Domain creation fails | No default VPC | VPC → **Create default VPC** → retry |
| Canvas will not launch | Domain still creating | Wait for status **InService** |
| Time series not offered as a model type | No date column detected, or no repeated item IDs | Confirm `date` is a timestamp and `item_id` is set |
| "Not enough data" | Too few rows per item | This dataset has 730/item; Standard build needs ≥50 |
| Build fails immediately | Target column wrong type | `units_sold` must be numeric |
| Build takes > 40 min on Quick | Something is wrong | **Log out**, then investigate |
| MASE > 1 | `item_id` not set — series blended | Reconfigure with `item_id` as Item ID |
| `promotion` shows no impact | Model missed a real pattern | Genuine finding — discuss it |
| What-if greyed out | Wrong file | Needs `retail_sales_with_future.csv` |
| Charges after logging out | App still `InService` | Domains → profile → **Delete app** |

---

# Cost summary

| Item | Cost |
|---|---|
| Domain (idle) | $0 |
| Canvas workspace, ~45 min | ~$1.43 *(likely $0 — free tier covers 160 hrs/mo for 2 months)* |
| Quick build | ~$2–4 |
| Data storage | pennies |
| **Total** | **~$2–$6** |
| *If you leave the workspace running a week* | ***$319*** |

---

## Files in this pack

```
Lab4-Canvas-Forecast/
├── 00-START-HERE-Feasibility-and-Cost.md
├── Lab-4-Canvas-Forecast.md                                  <- this file
├── dataset_preview.png
└── data/
    ├── retail_sales_history.csv        2,190 rows - the main dataset
    └── retail_sales_with_future.csv    2,370 rows - adds future rows for what-if
```

---

*The Canvas UI changes more often than most AWS consoles. Button names and menu
positions here are a close guide, not gospel — the surrounding logic holds even
if a label has moved. Rehearse once before teaching this.*
