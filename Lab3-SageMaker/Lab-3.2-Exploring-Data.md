# Lab 3.2 — Amazon SageMaker: Exploring Data
### Personal AWS account edition

> **Prerequisite:** Lab 3.1 must have created `vertebral_column.csv`.

**Duration:** ~30 minutes  **Extra AWS cost:** $0 (notebook instance only)

---

## Objectives

By the end of this lab you will be able to:

- Explore and display statistics using pandas
- Use charts to explore the characteristics of a dataset
- Look for correlation between features

## What changes from the official lab

| Official lab | This version | Why |
|---|---|---|
| Notebook provided by the lifecycle config | You upload `3_2-machinelearning.ipynb` yourself | No Vocareum lifecycle config |
| `MyNotebook` on `ml.m5.xlarge` | `MyNotebook` on `ml.t3.medium` | Cost |

Nothing else changes. **This lab is pure pandas and Matplotlib — it makes no
AWS API calls at all**, so it behaves identically anywhere, including on your
own laptop.

---

## Task 1 — Open your notebook instance

1. Console → **Amazon SageMaker AI**
2. Left navigation → **Applications and IDEs → Notebooks**
3. If `MyNotebook` is **Stopped**, select it and choose **Start**, then wait
   for `InService` (~2 minutes)
4. Choose **Open JupyterLab**

## Task 2 — Open the lab notebook

1. Open **`3_2-machinelearning.ipynb`**
2. Kernel: **`conda_python3`**
3. Run the cells in order

> If you get `FileNotFoundError: vertebral_column.csv`, either Lab 3.1 was not
> run, or the instance was **deleted** rather than stopped. Re-run Lab 3.1.

---

## Working through the notebook

### Step 1 — Structure (`df.info()`)

310 rows, 6 float features, 1 object target, no nulls.

**Worth noting:** real datasets are rarely this clean. "Zero missing values" is
the exception, not the rule — Lab 3.3 shows you the normal case.

### Step 1b — Class balance

```
Abnormal    210  (67.7%)
Normal      100  (32.3%)
```

**This is the single most important number in the module.** A model that
blindly answers "Abnormal" every time scores **67.7% accuracy** while being
completely useless.

Compare every accuracy figure from here on against 67.7%, not against 0%. You
will come back to this in Lab 3.6.

### Step 2 — Summary statistics (`df.describe()`)

Watch `degree_spondylolisthesis`: its maximum sits far above the 75th
percentile. That is a genuine outlier.

### Step 3 — Histograms

Most features are roughly normal. `degree_spondylolisthesis` is strongly
right-skewed.

### Step 3b — Box plots by class ← **the key chart**

Look at each panel and ask yourself: *which features separate the two classes?*

- **`degree_spondylolisthesis`** — dramatic separation. The strongest single
  predictor.
- **`pelvic_incidence`**, **`sacral_slope`**, `lumbar_lordosis_angle` — clear
  separation
- **`pelvic_radius`** — the boxes overlap heavily; weak on its own

In Lab 3.4 you will print the feature importances from the trained model. They
match this chart. Watch for that: *what you saw in the exploration is what the
model went on to learn.*

### Step 4 — Outliers

The notebook computes the IQR fence and lists the rows above it.

**Note that the extreme value is kept, deliberately.** It is a real
measurement, not a typo, and **XGBoost is tree-based**, so it splits on rank
rather than magnitude and is barely affected. A linear model, or anything
distance-based (k-NN, SVM, k-means), would need this handled. *The right
outlier treatment depends on the algorithm you intend to use.*

### Step 5 — Correlation ← **the interesting finding**

The heatmap shows `pelvic_incidence` strongly correlated with both
`sacral_slope` and `pelvic_tilt`. This is not a coincidence — it is anatomy:

```
pelvic_incidence = sacral_slope + pelvic_tilt
```

The notebook verifies it, printing a maximum deviation of about zero.

**Why it matters:** one feature is perfectly determined by two others, so it
adds no information. This is **perfect multicollinearity**, and it:

- breaks the coefficient estimates of linear and logistic regression
- is harmless for tree models, though it splits importance arbitrarily between
  the correlated features

Watch for the payoff in Lab 3.4: `pelvic_incidence` is **absent from the
feature-importance chart entirely**. The trees never needed it — the
information was already available through the other two.

### Step 6 — Pair plot

Every pairwise scatter, coloured by class. Look for pairs where the two colours
form distinct clusters: those combinations are what the model exploits.

---

## Check your understanding

1. Why is 84% accuracy only moderately good on this dataset?
   *Answer: because the baseline — always guessing the majority class — is
   already 67.7%.*
2. `pelvic_radius` overlaps heavily between classes. Should you drop it?
   *Answer: not necessarily. It may still be useful in combination with other
   features; the pair plot helps you decide.*
3. If you had to keep only two features, which would you keep?
   *Answer: almost certainly `degree_spondylolisthesis` plus one of the pelvic
   angles.*
4. Which correlated feature would you drop for a logistic regression, and why
   does the choice barely matter for XGBoost?
   *Answer: drop any one of `pelvic_incidence`, `sacral_slope` or `pelvic_tilt`
   — the third is redundant by construction. Trees are unaffected because they
   split on one feature at a time and never invert a design matrix.*

## Before you leave

- [ ] **Stop** the notebook instance if you are pausing

**Next:** [Lab 3.3 — Encoding Categorical Data](Lab-3.3-Encoding-Categorical-Data.md)
