# Lab 3.5 — Amazon SageMaker: Deploying a model
### Personal AWS account edition

> **Prerequisite:** Lab 3.4.

**Duration:** ~30 minutes
**Extra AWS cost:** Track B **$0** · Track A ~**$0.02** *if you delete the
endpoint promptly*

---

## ⚠ Read this first — the budget risk in this module is in this lab

A **real-time endpoint bills for every hour it exists**, whether or not you
send it a single request. It does not stop by itself. It does not stop when you
close the notebook, stop the notebook instance, or close your browser.

**One forgotten endpoint left overnight:**

```
ml.t2.medium  ~$0.056/hr × 14 hr ≈ $0.78
ml.m4.xlarge  ~$0.28/hr  × 14 hr ≈ $3.90   (the official lab's instance type)
```

Left for a **month**, an `ml.m4.xlarge` endpoint costs roughly **$200** — twice
a typical credit balance. This is the most common way people lose their
credits, and learning to avoid it is the single most valuable operational
lesson in the module.

**If you have credits, run Track A here** — a correctly managed endpoint costs
about **one cent**, and watching a real endpoint go live and then be deleted is
exactly the habit you want to build.

**But do not walk away mid-lab.** Run the deploy cell, the predict cell and the
delete cell in one sitting. If you have to stop partway, delete the endpoint
first. If you cannot guarantee that, use Track B — it never creates an endpoint
at all.

---

## Objectives

By the end of this lab you will be able to:

- Deploy a machine learning model
- Get a prediction from it
- Delete the endpoint
- Use batch transform on the test dataset

## What changes from the official lab

| Official lab | This version | Why |
|---|---|---|
| Notebook from the lifecycle config | You upload `3_5-machinelearning.ipynb` | No Vocareum config |
| Endpoint on `ml.m4.xlarge` | **`ml.t2.medium`** on Track A | ~$0.056/hr vs ~$0.28/hr — 5× cheaper |
| — | **Track B: no endpoint at all** | Zero cost, zero risk |
| — | Adds a verification cell that lists live endpoints | Proves nothing is still billing |
| Delete endpoint | `delete_endpoint(delete_endpoint_config=True)` | Also removes the config |

---

## Task 1 — Open the notebook

1. Console → **SageMaker AI → Notebooks** → start `MyNotebook` if it is stopped
2. **Open JupyterLab** → **`3_5-machinelearning.ipynb`** → kernel
   `conda_python3`
3. Set `USE_MANAGED_SAGEMAKER` to match what you used in Lab 3.4

> **If you ran Lab 3.4 on Track B and want Track A from here on**, that is
> fine — you do not have to go back. Track A needs `sm_context.json`, which
> only Lab 3.4's Track A cell writes; if it is missing, the Step 1 cell in
> this notebook runs that training job for you (~4 min, ~$0.01) and carries
> on. You will see `sm_context.json not found` followed by the job running.
> That message is informational, not an error.

## Task 2 — Model setup

As in the official lab, the model is rebuilt here so that the notebook stands
alone — on **both** tracks.

- **Track B** reloads `xgboost-model.json` from Lab 3.4, or retrains in about
  two seconds if it is missing.
- **Track A** reloads `sm_context.json` from Lab 3.4, or runs the managed
  training job here if it is missing (~4 min, ~$0.01).

---

## Task 3 — Deploy and predict

### Track B

No endpoint is created. The model is called in-process:

```python
def predict_proba(frame):
    return booster.predict(xgb.DMatrix(frame[feature_cols]))
```

This is exactly what the container does behind an endpoint — the network hop
and the hourly bill are the only things removed.

Expected output:

```
Predicted probability of Abnormal: 0.7578
Predicted class: Abnormal
Actual class   : Abnormal
```

### Track A

`model.deploy(...)` creates a persistent HTTPS endpoint on `ml.t2.medium`. It
takes 5–8 minutes. **Billing starts when it reaches `InService`.**

The invocation sends one CSV row and receives a probability back — the same
number Track B computes locally.

**Note the payload format:** CSV, features only, no label, no header. A
mismatch between what the model was trained on and what you send at inference
time is a very common source of silently wrong predictions.

## Task 4 — Delete the endpoint ← **do not skip this**

```python
predictor.delete_endpoint(delete_endpoint_config=True)
```

The notebook then **verifies** with a cell that lists every live endpoint in
your account:

```
No endpoints running. Nothing is billing.
```

If it instead prints `WARNING - endpoints still running`, go to
**SageMaker → Inference → Endpoints** and delete them by hand, now.

> Make this cell a habit, not a formality. Run it at the end of every session.

---

## Task 5 — Batch transform

A batch transform scores a whole file at once: SageMaker starts an instance,
processes the input, writes results to S3, and **terminates the instance
automatically**.

| | Real-time endpoint | Batch transform |
|---|---|---|
| Billing | Per hour, continuously, until deleted | Only while the job runs |
| Shuts down by itself | **No** | **Yes** |
| Latency | Milliseconds | Minutes of startup |
| Use when | Predictions on demand, low latency | You have a file to score |
| Budget risk | **High** | Low |

**The decision rule:** if you do not need a prediction in under a second for a
live user, you do not need an endpoint. Most coursework, analytics and
reporting workloads are batch problems. Reach for batch transform first.

For this lab's 31 test records, batch transform is both the correct tool and
the cheaper one.

Expected output (Track B):

```
Scored 31 records
Accuracy on the test set: 83.9%
```

The notebook writes `test_predictions.csv` for Lab 3.6.

---

## Check your understanding

1. Your model scores loan applications overnight in a nightly batch. Endpoint
   or batch transform?
   *Answer: batch — there is no latency requirement.*
2. Your model powers a "recommended for you" widget on a web page. Which?
   *Answer: an endpoint — a user is waiting for the answer.*
3. An endpoint sits idle all weekend. What do you pay?
   *Answer: the full hourly rate for every one of those hours. Idle time is not
   free.*
4. How would you serve an endpoint that gets traffic only during business
   hours?
   *Answer: autoscaling with a minimum of zero, a scheduled delete and
   recreate, or SageMaker Serverless Inference.*

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `FileNotFoundError: sm_context.json` | You are on Track A but Lab 3.4 was run on Track B, so no managed model exists | Just run the Step 1 cell — it recreates it. If you skipped that cell, go back and run it |
| `ResourceLimitExceeded` on deploy | No endpoint quota | Request `ml.t2.medium for endpoint usage`, or use Track B |
| Deploy hangs past 10 minutes | Normal-ish, or a failed image pull | Check **Inference → Endpoints** for the status and reason |
| `ModelError` on predict | Payload shape mismatch | Features only, no label, no header |
| Verification shows a stray endpoint | An earlier run left one behind | Delete it in the console immediately |
| `NoSuchKey` downloading batch output | The job wrote a different filename | List the output prefix in S3 and adjust the key |

## Before you leave — non-negotiable checklist

- [ ] The endpoint verification cell reports **no endpoints running**
- [ ] Console → **Inference → Endpoints** is empty
- [ ] `test_predictions.csv` exists (Lab 3.6 needs it)
- [ ] **Stop** the notebook instance if you are pausing

**Next:** [Lab 3.6 — Model Performance Metrics](Lab-3.6-Model-Performance-Metrics.md)
