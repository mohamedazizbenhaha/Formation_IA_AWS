# Lab 3.7 — Amazon SageMaker: Hyperparameter Tuning
### Personal AWS account edition

> **Prerequisite:** Labs 3.4, 3.5 and 3.6.

**Duration:** ~30 minutes
**Extra AWS cost:** Track B **$0** · Track A ~**$0.04** (capped at 4 jobs)

---

## ⚠ This is the most expensive lab in the module

A tuning job runs **many** training jobs — each one a separately billed
instance. The official lab's defaults can launch 10 or more.

**This version caps Track A at 4 jobs, 2 in parallel.** That is enough to show
you how the mechanism works, and it keeps the cost around 4 cents.

**Never raise `max_jobs` without doing the multiplication first:**

```
cost ≈ max_jobs × job_duration × instance_hourly_rate
20 jobs × 5 min × $0.115/hr ≈ $0.19   ... and 20 jobs on ml.m5.xlarge ≈ $0.38
```

Track B does the same search inside the notebook for **$0**, and — on a dataset
this small — actually does it *better*, because it uses 5-fold
cross-validation instead of a single validation split.

---

## Objectives

By the end of this lab you will be able to:

- Create a hyperparameter tuning job
- Tune an XGBoost model
- Compare a tuned model against a baseline using performance metrics

## What changes from the official lab

| Official lab | This version | Why |
|---|---|---|
| Notebook from the lifecycle config | You upload `3_7-machinelearning.ipynb` | No Vocareum config |
| Managed tuning job only | **Two tracks** | Track B is free and needs no quota |
| Default `max_jobs` (10+) | **`max_jobs=4`, `max_parallel_jobs=2`** | Cost control |
| Tuning on `ml.m4/m5.xlarge` | `ml.m5.large` | Roughly half the rate |
| Single validation split | Track B uses **5-fold CV** | Far more reliable on 310 rows |
| — | Adds a top-10 results table | Shows how close the candidates are |
| — | Adds an honest "tuning may not help" section | On this dataset, it genuinely does not help much |

---

## Task 1 — Open the notebook

Console → **SageMaker AI → Notebooks** → start `MyNotebook` → **Open
JupyterLab** → **`3_7-machinelearning.ipynb`** → kernel `conda_python3`

> On Track A, the **Track A setup check** cell near the top reuses the S3 data
> and container image that Lab 3.4 recorded in `sm_context.json`. If you ran
> Lab 3.4 on Track B, that cell recreates them for you (~4 min, ~$0.01)
> instead of failing.

---

## The concept

A **parameter** is learned from data during training — the split values inside
each tree.

A **hyperparameter** is set *before* training and controls how learning
happens.

| Hyperparameter | Effect | Typical range |
|---|---|---|
| `max_depth` | Tree depth. Deeper = more complex, overfits sooner | 3–10 |
| `eta` / `learning_rate` | Contribution per tree. Lower = slower, more robust | 0.01–0.3 |
| `min_child_weight` | Minimum data per leaf. Higher = more conservative | 1–10 |
| `gamma` | Minimum gain to split. Higher = simpler trees | 0–5 |
| `subsample` | Row fraction per tree | 0.5–1.0 |
| `num_round` / `n_estimators` | Number of trees | 50–500 |

Tuning searches this space for the best **validation** score. The test set
stays sealed until the very end — otherwise you are tuning against your own
final exam.

### Search strategies

| Strategy | How it works | Trade-off |
|---|---|---|
| **Grid search** | Every combination | Exhaustive, explodes combinatorially |
| **Random search** | Random samples | Usually finds near-best far faster — **Track B** |
| **Bayesian** | Each round informs the next | Fewest jobs for a given quality — **Track A** |

---

## Working through the notebook

### Track B — randomised search with cross-validation

40 candidates, 5-fold stratified CV, optimising **ROC AUC** (not accuracy — the
classes are imbalanced).

`cv=5` means each candidate is scored on 5 different train/validation folds and
the results averaged. On 310 rows this is dramatically more reliable than a
single 31-row validation split.

### The top-10 table ← **pause here**

Expected output:

```
rank   mean_test_score
1          0.9264
2          0.9236
3          0.9218
4          0.9214
5          0.9209
...
10         0.9196
```

**The best and the tenth-best differ by 0.007 AUC.** That gap is smaller than
the noise in the data.

What that tells you: *many different hyperparameter combinations perform about
equally well.* Hyperparameter tuning usually buys you a modest, incremental
gain — not a transformation. If you were expecting a dramatic jump, this is the
moment to recalibrate.

### Track A — managed tuning job

`HyperparameterTuner` launches `max_jobs` separate training jobs,
`max_parallel_jobs` at a time, using Bayesian optimisation. Results are
available via `tuner.analytics()` and in the console under **Training →
Hyperparameter tuning jobs**.

### Step 3 — Evaluate on the test set

Now, and only now, the test set is used. Track A deploys the best model
briefly, predicts, and **deletes the endpoint immediately**.

### Step 4 — Compare

Expected output:

```
           baseline   tuned  change
accuracy     0.8387  0.8065 -0.0323
precision    0.8636  0.8000 -0.0636
recall       0.9048  0.9524 +0.0476
f1           0.8837  0.8696 -0.0142
auc          0.9190  0.9238 +0.0048

Test set size: 31 records
One record changing sides moves accuracy by 3.2%
```

---

## Interpreting this honestly ← **the real lesson of Lab 3.7**

**Tuning made accuracy go down.** That is not a mistake in the lab, and it is
not something to gloss over.

Read the numbers properly:

- **AUC improved** (+0.005), and AUC is the threshold-independent metric, so
  the tuned model separates the classes marginally better.
- **Recall improved** (+4.8%) — it now catches 20 of 21 abnormal cases instead
  of 19. For a screening tool, that is the number that matters.
- **Accuracy dropped 3.2%** — which is *exactly one record* on a 31-row test
  set. That is noise, not evidence.

### Why tuning often does not help much

1. **The dataset is tiny.** 310 rows in total, 31 in test. There is little
   signal to extract, and the measurement is noisy.
2. **The baseline hyperparameters were already sensible** — they came from the
   AWS lab and are close to good defaults for this problem.
3. **Tuning optimises the validation score, not the test score.** With small
   data a model can fit the validation folds slightly too well.

On larger, messier datasets — like the flight-delay challenge lab — tuning
produces a much clearer gain. Compare the two when you get there.

**The correct takeaway is not "tuning always helps." It is: tune, then verify
honestly on held-out data, and be sceptical of small differences.** That is a
more useful professional habit than a tidy improvement would have given you.

---

## Check your understanding

1. Why optimise AUC rather than accuracy?
   *Answer: the classes are imbalanced, and AUC is threshold-independent.*
2. Why is 5-fold CV better than one validation split here?
   *Answer: 31 validation rows is too few to distinguish candidates reliably.*
3. The top 10 are within 0.007 AUC. What does that tell you about how much
   effort to spend tuning?
   *Answer: returns diminish fast — better to invest in more or better
   features.*
4. Accuracy dropped but recall rose. Which model would you ship for medical
   screening, and why?
   *Answer: the tuned one. In screening, a missed case costs far more than a
   false alarm, and the accuracy difference is one record — noise.*
5. You raise `max_jobs` from 4 to 40. What happens to cost and to expected
   improvement?
   *Answer: cost scales linearly; improvement plateaus quickly.*

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `FileNotFoundError: baseline_metrics.json` | Lab 3.6 not run | Run Lab 3.6 |
| `FileNotFoundError: sm_context.json` | You are on Track A but Lab 3.4 was run on Track B | Run the **Track A setup check** cell — it recreates it (~4 min, ~$0.01) |
| `ResourceLimitExceeded` | Needs quota for `max_parallel_jobs` instances | Set `max_parallel_jobs=1`, or use Track B |
| Track B search is slow | 40 candidates × 5 folds | Reduce `n_iter`; `n_jobs=-1` already parallelises |
| The tuned model scores worse | Expected on this dataset | See the interpretation section above — that result is the lesson |
| Tuning job stuck `InProgress` | Waiting on capacity | Check the console; stop it if it stalls |

---

## Module 3 is complete — final cleanup

- [ ] The endpoint verification cell reports **no endpoints running**
- [ ] Console → **Inference → Endpoints** is empty
- [ ] No training or tuning jobs `InProgress`
- [ ] Notebook instance **Stopped** (or **Deleted** if you are finished for
      good)
- [ ] Optional: empty the `sagemaker-<region>-<account-id>` S3 bucket
- [ ] Check **Billing → Bills** tomorrow to confirm your actual spend

**Optional next:** [Challenge Lab 3 — Flight Delays](Challenge-Lab-3-Flight-Delays.md)
