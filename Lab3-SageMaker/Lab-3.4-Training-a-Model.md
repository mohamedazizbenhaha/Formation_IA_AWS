# Lab 3.4 — Amazon SageMaker: Training a model
### Personal AWS account edition

> **Prerequisite:** Lab 3.1 must have created `vertebral_column.csv`.

**Duration:** ~30 minutes
**Extra AWS cost:** Track B **$0** · Track A ~**$0.01**

---

## Objectives

By the end of this lab you will be able to:

- Split data into training, validation and test datasets
- Train an XGBoost model

## What changes from the official lab

| Official lab | This version | Why |
|---|---|---|
| Notebook from the lifecycle config | You upload `3_4-machinelearning.ipynb` | No Vocareum config |
| Managed training job only | **Two tracks** — in-notebook or managed | Track B needs no S3, no IAM, no `ml.*` training quota, and costs nothing |
| Training on `ml.m4/m5.xlarge` | `ml.m5.large` on Track A | Roughly half the hourly rate |
| — | Adds `max_run=1200` to the estimator | A hard cost ceiling if a job hangs |
| — | Saves `feature_cols.json` | The CSVs are headerless; later labs need the column names |

**This is the first lab where the two tracks diverge.** Read the track table
below, or section 5 of the setup guide, before you run anything.

---

## Task 1 — Open the notebook

1. Console → **SageMaker AI → Notebooks** → start `MyNotebook` if it is stopped
2. **Open JupyterLab** → open **`3_4-machinelearning.ipynb`** → kernel
   `conda_python3`

## Task 2 — Choose your track

The second code cell contains:

```python
USE_MANAGED_SAGEMAKER = False    # <-- set True for the managed-job track
TRAIN_INSTANCE    = 'ml.m5.large'
ENDPOINT_INSTANCE = 'ml.t2.medium'
```

| | **Track B** (`False`) | **Track A** (`True`) |
|---|---|---|
| Where training runs | In this notebook | A separate managed instance |
| Extra cost | **$0** | ~$0.01 per job |
| Needs an S3 bucket | No | Yes |
| Needs an IAM role with S3 access | No | Yes |
| Needs `ml.m5.large` training quota | No | **Yes** |
| Time | ~2 seconds | ~4 minutes (mostly provisioning) |

Every subsequent cell checks this flag and skips itself if it does not apply,
so **you can safely run all cells top to bottom** either way.

> ### 👉 If you have credits, run **Track A**.
>
> This is the lab where Track A earns its keep. You watch a real training job
> appear in the SageMaker console, provision an instance, run, write a model
> artifact to S3, and tear itself down. That managed workflow is the point of
> Module 3, and it costs about **one cent**.
>
> It requires `ml.m5.large` **training** quota — see section 4 of the setup
> guide.
>
> **Keep Track B as your safety net.** If your quota is denied, or something
> breaks, flip the flag to `False` and everything still runs, with identical
> results.

---

## Working through the notebook

### Step 1 — Encode the target

`Abnormal → 1`, `Normal → 0`.

**Abnormal is the positive class.** Every precision and recall figure in Lab
3.6 reads against that convention: "recall" means *the fraction of genuinely
abnormal patients the model caught*.

### Step 2 — Reorder columns

The built-in SageMaker XGBoost algorithm requires CSV input with:

- the **target in the first column**
- **no header row**
- **no index column**

> **A classic failure:** forget `index=False` and pandas writes the row number
> as column 0. XGBoost then treats the index as the label and trains on noise.
> The job succeeds; the model is garbage. Nothing warns you.

### Step 3 — Split 80 / 10 / 10

Two arguments matter:

- **`stratify=...`** preserves the 67.7% / 32.3% class ratio in every split.
  Without it, a 31-row test set could easily end up with only 3 or 4 `Normal`
  cases, and every metric in Lab 3.6 becomes noise.
- **`random_state=42`** makes the split reproducible, so your numbers match the
  ones quoted in these guides.

Expected output:

```
train       248 rows (80%)  abnormal share 67.7%
validation   31 rows (10%)  abnormal share 67.7%
test         31 rows (10%)  abnormal share 67.7%
```

All three at 67.7% — stratification working exactly as intended.

**What each split is for:**

| Split | Purpose | When it is used |
|---|---|---|
| **Train** | Fit the trees | Lab 3.4 |
| **Validation** | Early stopping; choosing hyperparameters | Labs 3.4, 3.7 |
| **Test** | Final honest evaluation | Labs 3.6, 3.7 — **once, at the end** |

> **The cardinal rule:** never tune against the test set. The moment you choose
> anything based on test performance, it stops being an unbiased estimate.

### Step 4 — Write the CSVs

`train.csv`, `validation.csv`, `test_features.csv`, `test_labels.csv`,
`test.csv`, plus `feature_cols.json` (the CSVs are headerless, so the column
names have to be stored separately).

### Step 5 — Train

**Track B** uses the `xgboost` library directly — the same library the AWS
container runs internally, with the same hyperparameters. Only the *location*
differs.

**Track A** uploads to S3, retrieves the AWS XGBoost container image, and runs
a managed training job on a separate instance that terminates automatically.

The hyperparameters are identical in both tracks:

| Parameter | Value | Meaning |
|---|---|---|
| `objective` | `binary:logistic` | Binary classification, outputs a probability |
| `num_round` | 100 | Maximum number of trees |
| `max_depth` | 5 | Tree depth — higher overfits |
| `eta` | 0.2 | Learning rate |
| `subsample` | 0.8 | Row fraction per tree |
| `min_child_weight` | 6 | Minimum data per leaf |
| `gamma` | 4 | Minimum gain to split |
| `early_stopping_rounds` | 10 | Stop if validation has not improved in 10 rounds |

**Early stopping is the one to pay attention to here.** Expected output:

```
[0]   train-error:0.32258   validation-error:0.32258
[10]  train-error:0.10081   validation-error:0.12903
[18]  train-error:0.08871   validation-error:0.12903
Best iteration: 8
```

It stopped at round 18 of a possible 100. Training error was still falling
while validation error had stalled — **that gap is overfitting starting**.
Early stopping caught it and kept the round-8 model.

### Step 6 — Feature importance (Track B)

Expected output:

```
degree_spondylolisthesis    25.74
lumbar_lordosis_angle        9.53
pelvic_radius                9.48
sacral_slope                 8.22
pelvic_tilt                  8.14
```

Two things to notice:

1. **`degree_spondylolisthesis` dominates**, at nearly 3× the next feature —
   exactly what the Lab 3.2 box plots predicted. Your exploration and your
   model agree.
2. **`pelvic_incidence` is absent entirely.** The trees never split on it once.
   This is the multicollinearity from Lab 3.2 paying off: since
   `pelvic_incidence = sacral_slope + pelvic_tilt`, the information was already
   available and the feature was redundant.

That second point is worth sitting with — a finding from the exploration lab
explaining a result in the training lab.

---

## Track A only — before you run

Confirm:

- [ ] Your execution role can read and write S3 (`AmazonS3FullAccess` is
      simplest)
- [ ] **Service Quotas → SageMaker →** `ml.m5.large for training job usage` ≥ 1
- [ ] You accept ~$0.01 for the job

The instance terminates automatically when the job finishes. `max_run=1200`
caps it at 20 minutes as a safety net.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `FileNotFoundError: vertebral_column.csv` | Lab 3.1 not run | Run Lab 3.1 |
| `AccessDenied` on `get_execution_role()` | Restricted role | Use Track B |
| `ResourceLimitExceeded` on `fit()` | No training quota | Request an increase, or use Track B |
| `ClientError` on `upload_data` | Role lacks S3 access | Attach S3 permissions, or use Track B |
| Training error 0.0, validation much worse | Overfitting | Expected on 248 rows; early stopping handles it |
| `ModuleNotFoundError: sagemaker` | Not running on a SageMaker instance | Track B works anywhere |

## Before you leave

- [ ] Track A: the training job shows `Completed` (the instance has already
      terminated)
- [ ] **Stop** the notebook instance if you are pausing

**Next:** [Lab 3.5 — Deploying a Model](Lab-3.5-Deploying-a-Model.md)
