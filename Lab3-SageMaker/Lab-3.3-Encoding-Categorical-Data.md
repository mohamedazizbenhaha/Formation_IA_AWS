# Lab 3.3 — Amazon SageMaker: Encoding Categorical Data
### Personal AWS account edition

**Duration:** ~30 minutes  **Extra AWS cost:** $0 (notebook instance only)

> **No dependency on Labs 3.1 or 3.2.** This lab uses a different dataset and
> can be run standalone or out of order.

---

## Objectives

By the end of this lab you will be able to:

- Encode **ordinal** categorical data
- Encode **non-ordinal (nominal)** categorical data

## What changes from the official lab

| Official lab | This version | Why |
|---|---|---|
| Notebook from the lifecycle config | You upload `3_3-machinelearning.ipynb` | No Vocareum config |
| — | Adds missing-value handling before encoding | The raw file uses `?`; encoders reject NaN |
| — | Adds a high-cardinality section (`make`) | The realistic case that one-hot handles badly |

Like Lab 3.2, this lab makes **no AWS API calls**.

---

## Task 1 — Open the notebook

1. Console → **SageMaker AI → Notebooks** → start `MyNotebook` if it is stopped
2. **Open JupyterLab**
3. Open **`3_3-machinelearning.ipynb`**, kernel `conda_python3`

---

## The concept, stated plainly

Machine learning algorithms consume numbers. Categorical text must be
converted — and **the right conversion depends on whether the categories have
an inherent order.** Choose wrong and you inject false information that the
model will faithfully learn.

| Type | Example | Correct encoding |
|---|---|---|
| **Ordinal** — has an order | `small` < `medium` < `large` | Integer encoding, order specified |
| **Nominal** — no order | `red`, `green`, `blue` | One-hot encoding |

---

## Working through the notebook

### Step 1 — Load the automobile dataset

205 cars, 26 columns, from UCI. Two loading details matter:

- **There is no header row** — you supply the column names manually
- **Missing values are the literal string `?`** — handled with
  `na_values='?'`

**Why that second point matters:** without `na_values='?'`, pandas types
`price`, `horsepower` and `bore` as `object`, because of a handful of `?`
values. Numeric columns silently become text. Always check `df.dtypes` after
loading.

### Step 2 — Identify categorical columns

`select_dtypes(include='object')` finds them. The notebook prints the
cardinality of each column — the number that decides your encoding strategy.

### Step 3 — Handle missing values *first*

Encoders throw on NaN. Categorical NaN → mode, numeric NaN → median.

### Step 4 — Ordinal encoding ← **the key lesson**

Two genuinely ordinal columns:

- `num_of_doors`: `two` < `four`
- `num_of_cylinders`: `two` < `three` < `four` < `five` < `six` < `eight` < `twelve`

The critical line:

```python
ord_enc = OrdinalEncoder(categories=[door_order, cyl_order])
```

**Without an explicit `categories=`, scikit-learn sorts alphabetically.** The
notebook prints both mappings side by side:

| Value | Alphabetical (**wrong**) | Explicit (**correct**) |
|---|---|---|
| `eight` | 0 | 5 |
| `five` | 1 | 3 |
| `four` | 2 | 2 |
| `six` | 3 | 4 |
| `twelve` | 4 | 6 |
| `two` | 5 | 0 |

The alphabetical mapping claims an eight-cylinder engine has *fewer* cylinders
than a two-cylinder one. The model has no way to detect this — it will simply
learn a nonsensical relationship.

**This is the single most valuable thing in Lab 3.3.** It is a silent bug: no
error, no warning, just a worse model.

### Step 5 — One-hot encoding for nominal data

`body_style` — `convertible`, `hatchback`, `sedan`, `wagon`, `hardtop` —
cannot be ranked. Integer-encoding it would assert that `wagon` (4) > `sedan`
(3), which is meaningless.

One-hot creates one binary column per category. The notebook shows both ways:

```python
OneHotEncoder(sparse_output=False)     # scikit-learn, for pipelines
pd.get_dummies(df[nominal])            # pandas, convenient in notebooks
```

> The notebook wraps `sparse_output=` in a `try/except`, because scikit-learn
> renamed it from `sparse=` in version 1.2. It works on both.

**On `drop_first=True`:** it drops one category per feature to avoid the
**dummy variable trap** — with all *k* columns present, any one of them is
perfectly predictable from the others. That breaks linear model coefficients.
**Tree models do not care.**

### Step 5b — High cardinality

`make` has 22 values. One-hot on a 205-row dataset would add 22 columns — a
poor ratio of features to samples, which invites overfitting.

Options shown in the notebook:

1. **Group rare categories into `Other`** (used here — the top 8 are kept)
2. Target or frequency encoding
3. Use a model with native categorical support

### Step 6 — Assemble the final matrix

Numeric + ordinal + one-hot, concatenated, then verified as all-numeric.

---

## Reference table

| Situation | Technique | Why |
|---|---|---|
| Ordered categories | `OrdinalEncoder(categories=[...])` | Integer order carries meaning |
| Unordered, few values | `OneHotEncoder` / `get_dummies` | Avoids a false ranking |
| Unordered, many values | Group rare → `Other`, or target encoding | One-hot explodes dimensionality |
| Binary target label | `LabelEncoder` | Two classes → 0/1 |

> **A common exam-style trap:** `LabelEncoder` is for the **target**, not for
> input features. Applied to a nominal feature it produces exactly the
> alphabetical-ordering bug from Step 4.

---

## Check your understanding

1. `symboling` is an insurance risk rating from -3 to +3, already numeric. Is
   it ordinal, nominal, or continuous?
   *Answer: ordinal — the order is meaningful, but the gaps are not necessarily
   equal.*
2. Why does one-hot encoding hurt tree models less than you might expect, but
   still slow them down?
   *Answer: correctness is unaffected, but each binary column is another split
   candidate, so training gets slower and individual splits get weaker.*
3. `engine_location` has 202 `front` and 3 `rear`. Is it worth keeping?
   *Answer: probably not on its own — with 3 examples the model cannot learn
   anything reliable from `rear`, and the column mostly adds noise. If domain
   knowledge says rear-engine cars behave very differently, keep it and be
   honest that predictions for them are unreliable.*

## Before you leave

- [ ] **Stop** the notebook instance if you are pausing

**Next:** [Lab 3.4 — Training a Model](Lab-3.4-Training-a-Model.md)
