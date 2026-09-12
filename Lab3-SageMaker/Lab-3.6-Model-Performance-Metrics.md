# Lab 3.6 — Amazon SageMaker: Generating model performance metrics
### Personal AWS account edition

> **Prerequisite:** Labs 3.4 and 3.5.

**Duration:** ~30 minutes  **Extra AWS cost:** $0 in **both** tracks

---

## Objectives

By the end of this lab you will be able to:

- Use the test data to generate predictions
- Generate a confusion matrix
- Generate performance metrics for the model

## What changes from the official lab

| Official lab | This version | Why |
|---|---|---|
| Notebook from the lifecycle config | You upload `3_6-machinelearning.ipynb` | No Vocareum config |
| — | Regenerates predictions if `test_predictions.csv` is missing | The notebook stands alone |
| — | Adds a ROC curve and AUC | Threshold-independent, and the fair metric on imbalanced data |
| — | Adds a threshold-sweep table | Makes the precision/recall trade-off concrete |
| — | Adds an explicit small-test-set caution | 31 rows is not many, and you should know it |

**This lab is pure analysis** — no AWS API calls in either track, so it runs
identically anywhere.

---

## Task 1 — Open the notebook

Console → **SageMaker AI → Notebooks** → start `MyNotebook` → **Open
JupyterLab** → **`3_6-machinelearning.ipynb`** → kernel `conda_python3`

---

## The concepts

### The confusion matrix

With `Abnormal` as the positive class:

|  | Predicted Normal | Predicted Abnormal |
|---|---|---|
| **Actually Normal** | True Negative | **False Positive** |
| **Actually Abnormal** | **False Negative** | True Positive |

In this medical-screening framing the two errors are not equally bad:

- **False positive** — a healthy patient is sent for unnecessary follow-up.
  Costly and stressful, but recoverable.
- **False negative** — a patient with a spinal abnormality is told they are
  fine. Clinically far more serious.

**That asymmetry is the whole reason accuracy alone is insufficient.** Accuracy
treats both errors as equally bad. Almost no real problem does.

### Expected results

```
                 Pred Normal  Pred Abnormal
Actual Normal              7              3
Actual Abnormal            2             19

TN:  7  - healthy, correctly cleared
FP:  3  - healthy, wrongly flagged
FN:  2  - abnormal, MISSED
TP: 19  - abnormal, correctly caught
```

```
Accuracy     83.9%
Precision    86.4%
Recall       90.5%
Specificity  70.0%
F1 score     88.4%
AUC          0.919

Majority-class baseline accuracy: 67.7%
Improvement over baseline:        +16.1%
```

### Reading the metrics

| Metric | Formula | Question it answers | Here |
|---|---|---|---|
| **Accuracy** | (TP+TN)/all | What fraction of predictions were right? | 83.9% |
| **Precision** | TP/(TP+FP) | When it says Abnormal, how often is it right? | 86.4% |
| **Recall** | TP/(TP+FN) | Of all abnormal cases, how many did it catch? | 90.5% |
| **Specificity** | TN/(TN+FP) | Of all normal cases, how many did it clear? | 70.0% |
| **F1** | harmonic mean of P and R | One number balancing both | 88.4% |

**Always quote accuracy against the baseline.** 83.9% sounds decent in
isolation; what makes it meaningful is that guessing the majority class scores
67.7%. The model adds **16 percentage points** — real, but not miraculous.

**Notice the weakest number: specificity, 70%.** The model is much better at
catching abnormal cases (90.5%) than at correctly clearing healthy ones. It
leans toward predicting Abnormal — a sensible bias for a screening tool, but
one you should state openly rather than let it hide behind a good F1.

### ROC and AUC

The 0.5 cutoff is a **choice**, not a property of the model. The model outputs
a probability; you decide where to draw the line.

The ROC curve sweeps that threshold from 0 to 1. **AUC** summarises it:

- 0.5 = random guessing
- 1.0 = perfect separation
- **0.919 here** — strong

AUC is threshold-independent and insensitive to class balance, which makes it
the fairest single summary on an imbalanced dataset. It is also the metric you
will optimise in Lab 3.7.

### The threshold sweep

The notebook prints accuracy, precision, recall, F1, missed cases and false
alarms at thresholds from 0.2 to 0.8.

Lowering the threshold flags more patients as Abnormal: **more true cases
caught, more false alarms**. Raising it does the reverse.

There is no mathematically correct row. The choice depends on the relative cost
of the two errors — **a clinical and business decision, not a modelling one.**
For screening, where a missed case is worse than a false alarm, a threshold
below 0.5 is usually justified.

---

## An important caution about these numbers

The test set is **31 records**. One record changing sides moves accuracy by
about **3.2 percentage points**.

What follows from that:

- Treat these numbers as indicative, not precise
- Be sceptical of small differences between models in Lab 3.7
- With data this small, **k-fold cross-validation** is far more trustworthy
  than a single held-out split — which is exactly what Lab 3.7 uses

---

## Check your understanding

1. A model scores 99% accuracy detecting a disease affecting 1% of patients.
   Is it good?
   *Answer: probably useless — always predicting "healthy" scores 99% too.
   Check recall.*
2. Would you rather raise precision or recall for cancer screening?
   *Answer: recall — missing a case is far worse than a false alarm.*
3. What about spam filtering?
   *Answer: precision — a real email lost in the spam folder is worse than a
   spam message in the inbox.*
4. Why is AUC fairer than accuracy here?
   *Answer: it is threshold-independent and insensitive to class balance.*
5. Specificity is only 70%. What does that mean for a healthy patient?
   *Answer: roughly a 30% chance of being wrongly flagged.*

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `FileNotFoundError: test.csv` | Lab 3.4 not run | Run Lab 3.4 |
| `FileNotFoundError: feature_cols.json` | Same | Run Lab 3.4 |
| Predictions missing | Lab 3.5 not run | The notebook regenerates them automatically |
| Metrics differ slightly from above | A different `random_state`, or a re-run split | Expected; keep `random_state=42` for identical numbers |
| Precision and recall are 0, with a warning | The model predicted one class only | Check the target encoding in Lab 3.4 |

## Before you leave

- [ ] `baseline_metrics.json` written (Lab 3.7 compares against it)
- [ ] **Stop** the notebook instance if you are pausing

**Next:** [Lab 3.7 — Hyperparameter Tuning](Lab-3.7-Hyperparameter-Tuning.md)
