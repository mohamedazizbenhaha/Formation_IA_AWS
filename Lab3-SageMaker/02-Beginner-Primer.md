# Beginner Primer
### Everything assumed but never explained by the official labs

**Read this if AWS, Jupyter, or machine learning are new to you.** The official
AWS Academy labs assume you already know all of this. Nothing here is difficult
— it is just never stated.

You do **not** need to memorise it. Skim it once, then use it as a reference
when a lab uses a word you do not recognise.

---

## Part 1 — AWS basics

### What AWS actually is

Amazon Web Services rents computers and software services by the hour over the
internet. You do not buy hardware; you ask for a machine, use it, and switch it
off. You pay for the time it existed.

**The AWS Management Console** is the website where you click buttons to create
and destroy those resources. That is the URL you signed in with.

### Regions — the thing that confuses everyone first

AWS runs data centres in **regions** around the world: `us-east-1` (Northern
Virginia), `eu-west-1` (Ireland), and so on.

> **Critical:** resources exist **inside one region only**. A notebook you
> create in `us-east-1` is **completely invisible** if your console is set to
> `eu-west-1`. It has not been deleted — you are simply looking in the wrong
> place.

The region selector is in the **top-right corner** of the console, next to your
account name.

**Use `US East (N. Virginia) / us-east-1` for everything in this module.** It
has the widest instance availability and the lowest prices. If a resource ever
"disappears", check the region selector first — it is nearly always that.

### The services you will touch

| Service | What it is | Used for |
|---|---|---|
| **SageMaker AI** | AWS's machine-learning platform | Everything in Module 3 |
| **S3** | Object storage — files in "buckets" | Training data and model files (Track A only) |
| **IAM** | Permissions system | The role your notebook uses |
| **Service Quotas** | Limits on what you may create | Checking you *can* create instances |
| **Billing** | Costs and credits | Watching your credit balance |

### Instance types — decoding `ml.t3.medium`

An **instance** is a virtual machine. Its **type** describes its size.

```
ml . t3 . medium
│    │     └── size: medium, large, xlarge, 2xlarge ...
│    └──────── family: t3 = burstable/cheap, m5 = balanced, p3 = GPU
└───────────── ml = a SageMaker machine-learning instance
```

Bigger = faster = more expensive. **For 310 rows of data, `ml.t3.medium` is
plenty.** See the Cost Control Playbook for why bigger is not faster here.

### IAM roles — the permissions thing

**IAM** = Identity and Access Management.

A **role** is a bundle of permissions that a *service* assumes — not a person.
Your notebook instance "wears" a role whenever it calls another AWS service.

That is why the create form asks for one: without a role, your notebook has no
permission to read or write S3, and training jobs cannot run.

You create it once, in the **IAM** console, and reuse it forever. Do not use
the "Create a new role" link inside the notebook form — on current accounts it
leads to Amazon SageMaker Role Manager, which has been retired and will not
create the role. See section 5, Step 1b of the setup guide for the exact
click-path.

### Service quotas — the invisible limit

AWS caps how much of each resource a new account may create, to limit damage
from mistakes and abuse. **New accounts often have a quota of `0` for `ml.*`
instances.**

You discover this when creation fails with `ResourceLimitExceeded`. Requesting
an increase is free but **not instant** — minutes to a couple of business days.

**Check before you need it.** See section 4 of the setup guide.

### Stop vs Delete — memorise this one

| | **Stop** | **Delete** |
|---|---|---|
| Hourly charge | Ends | Ends |
| Your files | ✅ **Kept** | ❌ **Gone forever** |
| Getting back | Start it, ~2 min | Recreate from scratch |

**Stop between sessions. Delete when the module is finished.**

If your files vanish between sessions, the instance was deleted, not stopped.
Re-run Lab 3.1 to regenerate them.

---

## Part 2 — Jupyter notebooks

### What a notebook is

A document mixing **runnable code** with **formatted text**, split into
**cells**. You run cells one at a time and see output immediately underneath.
It is the standard tool for data science because you can explore, see a result,
and adjust — without re-running everything.

**JupyterLab** is the web interface. **`.ipynb`** is the file extension.

### Cell types

| Type | Contains | Output |
|---|---|---|
| **Code** | Python | Result printed below, labelled `Out [n]` |
| **Markdown** | Formatted text | Rendered as styled text |
| **Raw** | Plain text | Nothing |

### Running cells

- **`SHIFT + ENTER`** — run this cell, move to the next *(use this one)*
- **`CTRL + ENTER`** — run this cell, stay put
- The **▶** button in the toolbar
- **Run → Run All Cells** — run the whole notebook

### Reading the `In [ ]` marker

To the left of each code cell:

| Marker | Meaning |
|---|---|
| `In [ ]` | Never run |
| `In [*]` | **Running right now** — wait |
| `In [5]` | Finished; it was the 5th cell run |

**Those numbers are execution order, not position.** `In [5]` above `In [2]`
means you ran them out of order.

### ⚠ The mistake every beginner makes

**Cells run in the order *you* run them, not top to bottom.** A variable
defined in a cell you skipped does not exist. A variable from a cell you edited
and did not re-run still holds the *old* value.

Symptoms: `NameError`, a value that "should have changed" but did not, results
that do not match the person next to you.

> **The fix, and the first thing to try whenever a notebook behaves
> strangely:**
> **Kernel → Restart Kernel and Run All Cells**
>
> This clears everything and runs the notebook cleanly from the top.

### The kernel

The **kernel** is the Python process running your code. It holds every variable
you have created.

- **`conda_python3`** is the kernel to choose for every notebook in this pack.
- The **circle at the top right** shows status: hollow = idle, filled =
  running.
- **Kernel → Interrupt** stops a cell that is stuck.
- **Kernel → Restart** wipes all variables and starts fresh.

### Keyboard shortcuts

Press **`ESC`** first (command mode), then:

| Key | Action |
|---|---|
| `A` | Insert cell **a**bove |
| `B` | Insert cell **b**elow |
| `M` | Convert to **M**arkdown |
| `Y` | Convert to code |
| `D D` | **D**elete cell (press D twice) |
| `Z` | Undo delete |

Press **`ENTER`** to go back to editing inside a cell.

### Saving

`CTRL + S`, or File → Save. Notebooks also autosave periodically.

**Your files live on the instance's disk**, so they survive a *stop* but not a
*delete*. To keep a notebook permanently: right-click it in the file browser →
**Download**.

---

## Part 3 — Machine learning vocabulary

Everything the labs use, in the order you meet it.

### The data

| Term | Meaning |
|---|---|
| **Feature** | An input column. Here: `pelvic_incidence`, `pelvic_tilt`, … |
| **Target / label** | The column you are predicting. Here: `Normal` / `Abnormal` |
| **Row / sample / record** | One example. Here: one patient |
| **Categorical** | A text category (`sedan`, `hatchback`) |
| **Ordinal** | A category *with an order* (`small` < `medium` < `large`) |
| **Nominal** | A category *without* an order (`red`, `green`, `blue`) |

### The splits (Lab 3.4)

| Split | Share | Purpose |
|---|---|---|
| **Training** | 80% | The model learns from this |
| **Validation** | 10% | Tune settings, decide when to stop |
| **Test** | 10% | Final honest score — **used once, at the end** |

> **Why three?** If you judge the model on data it learned from, you are
> measuring memorisation. Validation guides your choices; test gives an
> unbiased final number. **Never tune against the test set** — the moment you
> choose anything based on it, it stops being unbiased.

**Stratified split** — keeps the class ratio (here 67.7% Abnormal) identical in
all three parts. Without it, a small test set may barely contain the minority
class and every metric becomes noise.

### The algorithm

**XGBoost** builds many small decision trees in sequence, each correcting the
previous one's mistakes. It is the standard first choice for tabular data:
fast, accurate, and robust to outliers and unscaled features.

| Term | Meaning |
|---|---|
| **Parameter** | Learned from the data during training (tree split values) |
| **Hyperparameter** | Set *before* training; controls *how* it learns (`max_depth`, `eta`) |
| **Overfitting** | Memorising the training data; great train scores, poor test scores |
| **Early stopping** | Halt when validation stops improving — prevents overfitting |

### The metrics (Lab 3.6)

With `Abnormal` = the positive class:

|  | Predicted Normal | Predicted Abnormal |
|---|---|---|
| **Actually Normal** | True Negative | **False Positive** (false alarm) |
| **Actually Abnormal** | **False Negative** (missed case) | True Positive |

| Metric | Plain English |
|---|---|
| **Accuracy** | What fraction of all predictions were right? |
| **Precision** | When it says Abnormal, how often is it right? |
| **Recall** | Of all truly Abnormal cases, how many did it catch? |
| **F1** | One number balancing precision and recall |
| **AUC** | How well it separates the classes at *any* threshold. 0.5 = random, 1.0 = perfect |

> **The most important idea in Lab 3.6:** accuracy alone lies. If 68% of
> patients are Abnormal, a model that always answers "Abnormal" scores 68%
> while being useless. **Always compare accuracy to that baseline**, and check
> recall.

### SageMaker terms

| Term | Meaning | Bills |
|---|---|---|
| **Notebook instance** | The VM running JupyterLab | Hourly, until **stopped** |
| **Training job** | A separate VM that trains, saves the model, terminates | Only while running |
| **Model artifact** | The trained model file, in S3 | Storage only (pennies) |
| **Endpoint** | A live HTTPS server for predictions | **Hourly, until deleted** ⚠️ |
| **Batch transform** | Scores a file, then terminates itself | Only while running |

---

## Part 4 — Reading error messages

| Error | Meaning | Fix |
|---|---|---|
| `NameError: name 'df' is not defined` | Cell not run, or kernel restarted | Run the earlier cells; or Restart & Run All |
| `FileNotFoundError: vertebral_column.csv` | Labs run out of order | Run Lab 3.1 first |
| `ModuleNotFoundError: xgboost` | Library missing / wrong kernel | Switch to `conda_python3`, or `!pip install xgboost` |
| `ResourceLimitExceeded` | Quota is 0 | Request an increase — not instant |
| `AccessDenied` | Missing permission | Check the IAM role; or use Track B |
| `ClientError` on S3 | Role lacks S3 access | Attach `AmazonS3FullAccess`, or use Track B |
| `KeyError: 'class'` | Column name typo or wrong file | `print(df.columns)` |
| Kernel keeps dying | Ran out of memory | Use fewer rows, or a bigger instance |

**How to read a Python traceback:** the **last line** states what went wrong.
The lines above show how it got there. Start at the bottom.

---

## Part 5 — Track A vs Track B

Every notebook from 3.4 onward opens with:

```python
USE_MANAGED_SAGEMAKER = False
```

| | **Track B** (`False`) | **Track A** (`True`) |
|---|---|---|
| Training runs | Inside your notebook | On a separate managed instance |
| Extra cost | **$0** | ~$0.07 for the module |
| Needs S3 + IAM role | No | Yes |
| Needs `ml.*` quota | No | Yes |
| Speed | Seconds | Minutes (provisioning) |
| You learn | The ML concepts | ML concepts **+ the SageMaker workflow** |

**Both produce the same model and the same numbers.** Every cell checks the
flag and skips itself when it does not apply, so you can safely run all cells
top to bottom in either mode.

- **You have credits available → run Track A** to see real SageMaker jobs.
- **Something breaks, or quota is denied → flip to `False`** and continue with
  zero AWS dependencies.

---

## Part 6 — Your first session, step by step

1. Sign in at the console. **Set the region to US East (N. Virginia).**
2. **Set a $5 budget alarm** (Billing → Budgets). Two minutes.
3. **SageMaker AI → Notebooks → Create notebook instance**
   - Name: `MyNotebook`
   - Type: **`ml.t3.medium`**
   - Lifecycle configuration: **None**
   - IAM role: select the `SageMakerExecutionRole` you created in IAM
     beforehand (setup guide, section 5, Step 1b — do **not** use the form's
     "Create a new role" link, it leads to the retired Role Manager)
4. Wait for **`InService`** (2–5 min).
5. **Open JupyterLab** → upload the eight `.ipynb` files.
6. Open `3_1-machinelearning.ipynb`, kernel **`conda_python3`**.
7. Run cells with `SHIFT + ENTER`.
8. **When finished: Notebooks → select → Actions → Stop.**

Step 8 is the one people forget. It is the one that costs money.

---

**Next:** [Lab 3.1 — Creating and Importing Data](Lab-3.1-Creating-and-Importing-Data.md)
