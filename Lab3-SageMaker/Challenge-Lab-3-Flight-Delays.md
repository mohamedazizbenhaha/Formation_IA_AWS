# Challenge Lab 3 — Predicting Airplane Delays
### Personal AWS account edition, scaled down

**Duration:** ~90 minutes (the official lab allows 300)
**Extra AWS cost:** **$0** on the default settings — notebook instance only

> **Independent of Labs 3.1–3.7.** Different dataset, self-contained. But it
> applies everything from them, so run it last.

---

## ⚠ Two setup differences before you start

### 1. You need a bigger volume

The default 5 GB is not enough. Either:

- **Create a new instance** with **Volume size = 25 GB**, or
- Edit `MyNotebook` (it must be **Stopped** first) → **Additional
  configuration → Volume size → 25**, then Start it

`ml.t3.medium` is still fine for the CPU. Volume size is the constraint, and
EBS is cheap (a 25 GB volume is a few cents per month).

### 2. This version downloads far less data

| | Official lab | **This version** |
|---|---|---|
| Period | 2013–2018, 72 monthly files | **2 months** (Jan + Jul 2018) |
| Download | ~1.7 GB compressed | **~50 MB** |
| Expanded | Several GB | ~250 MB |
| Instance | `ml.m4.xlarge` | `ml.t3.medium` |
| Runtime | Well over an hour | ~15 minutes |

**Know the trade-off you are making:** with two months of data you cannot see
seasonal or year-over-year patterns, and the model is somewhat weaker than one
trained on six years. Every step of the pipeline is identical.

To scale up, edit one line — but each extra month adds ~25 MB and processing
time:

```python
MONTHS = [(2018, 1), (2018, 7)]                          # default
MONTHS = [(2018, m) for m in range(1, 13)]               # a full year
```

---

## Business scenario

You work for a travel booking website that wants to warn customers at booking
time whether a flight to or from a busy US airport is likely to be delayed. You
have US DOT on-time performance data. Build a model that predicts delays.

## Objectives

By the end of this lab you will be able to:

- Process and create a dataset from downloaded ZIP files
- Perform exploratory data analysis
- Establish a baseline model
- Perform hyperparameter optimisation
- Use metrics to compare model performance

---

## Task 1 — Open the notebook

Console → **SageMaker AI → Notebooks** → start your instance → **Open
JupyterLab** → **`Flight_Delay-Student.ipynb`** → kernel `conda_python3`

---

## Working through the notebook

### Step 1 — Download

From the Bureau of Transportation Statistics. Two ZIPs, one CSV each. It takes
a few minutes.

### Step 2 — Load selected columns ← **two important lessons**

**Lesson 1 — do not load what you do not need.** These files have well over 100
columns. `usecols` cuts memory and load time dramatically. On a small instance
this is the difference between working and running out of RAM.

**Lesson 2 — target leakage.** This is the most important concept in the
challenge lab.

Columns like `ArrDelay`, `DepDelay`, `WheelsOff`, `TaxiOut` and
`ActualElapsedTime` are **only known after the flight has happened**. Including
any of them produces a model with near-perfect scores that is **completely
useless in production**, because at booking time those values do not exist.

`DepDelay` is especially seductive: it correlates almost perfectly with the
target, because the target *is derived from it*. A model handed that column
learns "a flight is delayed if it departed late" — true, circular, worthless.

**The rule: use only information that is available at prediction time.** Ask of
every feature, "would I actually have this when the customer clicks Book?"

### Step 3 — Target and cleaning

The target is `DepDel15` — the DOT's own flag for departing 15 or more minutes
late. Cancelled and diverted flights are removed (they are a different problem,
with unreliable fields).

Expected: 1,215,455 rows loaded → 1,183,906 after cleaning, ~20% delayed.

### Step 3b — Focus on busy airports

The business requirement says *busiest airports*. Filtering to the top 15
origins and destinations makes the problem more relevant and the data lighter.

Expected: 166,618 rows after filtering.

### Step 4 — Exploratory data analysis

Four charts. The **departure-hour** chart is the striking one: delay rates
climb steadily through the day as disruptions cascade through aircraft
rotations. Early-morning flights are far more reliable.

That single insight carries much of the model's predictive power — and it is
actionable advice a booking site could surface directly.

### Step 5 — Feature engineering

One-hot encode `Origin`, `Dest` and `Reporting_Airline` — exactly the nominal
case from Lab 3.3. Derived features: `dep_hour`, `arr_hour`, `is_weekend`.

### Step 6 — Stratified split

70/15/15, the same approach as Lab 3.4.

### Step 7 — Baselines ← **the payoff**

Expected results:

```
                naive  xgb baseline  class-weighted   tuned
accuracy       0.8011        0.8165          0.6998  0.7254
precision      0.0000        0.6860          0.3627  0.3875
recall         0.0000        0.1428          0.6725  0.6558
f1             0.0000        0.2364          0.4712  0.4872
auc            0.5000        0.7528          0.7490  0.7619
```

**Read the second column carefully.** The plain XGBoost baseline has the
*highest accuracy of any model* — 81.7% — while catching only **14%** of actual
delays. It achieves that score almost entirely by predicting "on time" for
everything. As a product it is worthless: it would essentially never warn
anyone.

**Now the third column.** `scale_pos_weight` tells XGBoost to weight the
minority class. Accuracy *drops* to 70%, and recall jumps to **67%**. It now
catches two-thirds of delays.

> **This is the clearest demonstration in the whole module of why your metric
> must match your business goal.** By accuracy, the model got worse. By
> usefulness, it got dramatically better. A team optimising accuracy would have
> shipped the useless model and reported a success.

### Step 8 — Hyperparameter optimisation

Randomised search, 12 candidates, 3-fold CV, optimising AUC. `n_iter` is kept
small because each fit is a full training run on 166k rows.

Tuning lifts AUC from 0.749 to **0.762** — a real, if modest, gain. Notice that
this is a clearer improvement than you got in Lab 3.7, because there is far
more data to learn from here. That contrast is the point.

### Step 9 — Feature importance

Airline and airport identity dominate, with `dep_hour` and `Month` also
contributing. Some carriers and some airports are simply less punctual.

---

## Step 10 — Interpreting the result honestly

**AUC ≈ 0.76.** Real signal, well above random — but not a solved problem.

### Why the ceiling is low

**The biggest single cause of departure delays is weather, and this dataset
contains no weather data at all.** You are predicting a weather-driven outcome
without observing the weather. Schedule, airport and airline are proxies for
it.

### What would actually improve it

1. **Historical weather by airport and hour** — the largest missing signal
2. **The delay status of the aircraft's previous flight that day** — delays
   cascade through aircraft rotations, and this is usually the strongest
   available predictor
3. **Airport congestion** — scheduled departures in the same hour
4. **The full six years**, for seasonal and yearly patterns

### Would you ship it?

At AUC ≈ 0.76 with ~39% precision on the class-weighted model, a "likely
delayed" warning would be wrong most of the times it fired. That would annoy
customers and erode trust.

**The honest recommendation is to gather weather and aircraft-rotation data
before productionising.** Recognising that — and being willing to say it — is a
better answer than reporting a number and declaring victory. This professional
judgement is what the challenge lab is really assessing.

---

## Your deliverable

Write a short summary covering:

1. Which features you used, and **which you deliberately excluded to avoid
   leakage**
2. Your baseline, and why a naive baseline matters
3. Which metric you optimised, **and why**, given the business goal
4. Your tuning result, and whether the gain justified the compute
5. A clear recommendation: ship it, or gather more data first — with your
   reasoning

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `No space left on device` | 5 GB volume | Resize to 25 GB (the instance must be Stopped) |
| Download times out | Large file, slow link | Re-run the cell — completed files are skipped |
| `MemoryError` | Too many rows | Lower `SAMPLE_ROWS`, or use fewer `MONTHS` |
| The search takes forever | `n_iter` × `cv` × rows | Lower `n_iter` or `SAMPLE_ROWS` |
| Suspiciously perfect scores | **Target leakage** | Check for `DepDelay`/`ArrDelay` in `USE_COLS` |
| Recall near zero | Class imbalance | Use `scale_pos_weight` — this is Step 7's point |

## Before you leave

- [ ] Delete `flight_data/` if you are keeping the instance (last cell,
      commented out)
- [ ] No endpoints running
- [ ] Notebook instance **Stopped** or **Deleted**
- [ ] Consider shrinking the volume back, or deleting the instance entirely

---

*Dataset: Bureau of Transportation Statistics, Airline On-Time Performance
Data — <https://www.transtats.bts.gov/>*
