# Lab 3.1 — Amazon SageMaker: Creating and importing data
### Personal AWS account edition

> **Before this lab:**
> 1. [`00-START-HERE-Setup-and-Feasibility.md`](00-START-HERE-Setup-and-Feasibility.md) — required
> 2. [`01-Cost-Control-Playbook.md`](01-Cost-Control-Playbook.md) — 10 minutes, saves you from the one expensive mistake
> 3. [`02-Beginner-Primer.md`](02-Beginner-Primer.md) — only if AWS or Jupyter are new to you

**Duration:** ~30 minutes  **Extra AWS cost:** $0 (notebook instance only)

---

## Objectives

By the end of this lab you will be able to:

- Launch an Amazon SageMaker notebook instance
- Launch JupyterLab and run code and Markdown cells
- Download data from an external source
- Save your work so it survives between sessions

## What changes from the official lab

| Official lab | This version | Why |
|---|---|---|
| Instance type `ml.m5.xlarge` | **`ml.t3.medium`** | ~$0.05/hr vs ~$0.23/hr. The dataset is 310 rows |
| Lifecycle configuration `...ml-pipeline` | **None** — you upload the notebooks yourself | Vocareum-only; it does not exist in your account |
| `PythonCheatSheet.ipynb` provided | Not present | Provisioned by the lifecycle config |
| Sample `linear_learner_mnist.ipynb` (Task 3) | **Skipped** | The official lab tells you that you cannot run it anyway (it needs an S3 bucket) |
| Type the import code by hand (Task 4) | Already written in `3_1-machinelearning.ipynb` | Read it and run it rather than retyping it |
| "Choose Start Lab" | Just sign in to your account | There is no Vocareum lab controller |

---

## Task 1 — Create the notebook instance

1. In the console search bar, find and open **Amazon SageMaker AI**.
2. In the left navigation, choose **Notebooks**.
3. Choose **Create notebook instance**.
4. **Notebook instance name:** `MyNotebook`
5. **Notebook instance type:** `ml.t3.medium`
   > Not `ml.m5.xlarge`. This is the main cost saving in the module.
6. **Platform identifier:** **Amazon Linux 2023, Jupyter Lab 4**
   > This is the console's label for `notebook-al2023-v1`, the identifier the
   > official lab names. It will be your **only** choice: AWS retired the
   > older Amazon Linux 2 platforms (JupyterLab 1 and 3) when Amazon Linux 2
   > reached end of support. Select it and move on — nothing is wrong.
7. Under **Additional configuration**, leave **Lifecycle configuration** as
   **None**.
   > The official lab tells you to pick the config containing `ml-pipeline`.
   > It will not be in your dropdown. That is expected, not an error.
8. **Permissions and encryption → IAM role** — the form stops here and asks you
   for a role. This is expected, not an error. Every notebook instance needs
   one so it can reach S3.

   Open the **IAM role** dropdown and select **`SageMakerExecutionRole`** — the
   role you created in the setup guide, section 5, Step 1b.

   > **Do not use the "Create a new role" option in this dropdown.** The
   > official lab tells you to, but on current accounts it leads to **Amazon
   > SageMaker Role Manager**, which reports that it *"is no longer open to new
   > customers"* and cannot create the role. If you have not created the role
   > yet, stop here, open the **IAM** console, and follow section 5, Step 1b of
   > the setup guide — it takes about a minute — then come back to this form.

   **You do this only once.** Reuse the same role for every future instance.

   > If you cannot create a role at all, you are signed in as an IAM user
   > without `iam:CreateRole`. Sign in as the account owner — or use
   > **Track B**, which needs no role at all.

9. Leave everything else at its default and choose **Create notebook
   instance**.

The status goes `Pending` → `InService` in about 2–5 minutes.

> **If creation fails with `ResourceLimitExceeded`**, your `ml.*` quota is 0.
> See section 4 of the setup guide. This needs an approved quota increase, and
> it is not something you can work around in the moment.

**Billing starts the moment the instance reaches `InService`** — not when you
open JupyterLab.

## Task 2 — Open JupyterLab and upload the notebooks

1. When the status is `InService`, choose **Open JupyterLab** at the end of the
   row.
2. In the left file browser, click the **upload** (↑) icon.
3. Upload all eight `.ipynb` files from this pack's `notebooks/` folder.

### Getting oriented in JupyterLab

The official lab walks through the interface using a cheat-sheet notebook you
will not have. Here is the same content, condensed:

> **Your JupyterLab will look slightly different from the official lab's
> screenshots.** Those were taken on JupyterLab 3; every new notebook
> instance now runs **JupyterLab 4**, which rearranges the layout a little
> and changes some icons. Nothing below is affected — the menus, the
> `conda_python3` kernel, the upload arrow and every shortcut work the same.

**Menu bar:** File (save, checkpoint) · Edit · View · **Run** · **Kernel**
(restart, change language) · Git · Tabs · Settings · Help

**Left sidebar tabs:** file browser · running kernels and terminals · git ·
command palette · notebook tools · open tabs · table of contents

**Cell types** — the dropdown in the toolbar:

- **Code** — executable Python. Input is `In [n]`, output `Out [n]`
- **Markdown** — formatted text for documentation
- **Raw** — passed through unprocessed

**Running a cell:** `SHIFT + ENTER`, the ▶ button, or **Run → Run Cells**

**Keyboard shortcuts** (press `ESC` first to enter command mode):

| Key | Action |
|---|---|
| `M` | Change cell to Markdown |
| `Y` | Change cell to Code |
| `A` / `B` | Insert cell above / below |
| `D D` | Delete cell |
| `Z` | Undo delete |
| `SHIFT+ENTER` | Run cell, select next |

**The kernel indicator** (top right): a hollow circle means idle, a filled
circle means running. If a cell hangs, use **Kernel → Interrupt**.

> **The most common beginner error:** cells run in the order *you* run them,
> not top to bottom. If a variable is unexpectedly missing or stale, use
> **Kernel → Restart Kernel and Run All Cells**.

## Task 3 — Open and run the lab notebook

1. Open **`3_1-machinelearning.ipynb`**.
2. If you are prompted for a kernel, choose **`conda_python3`**.
3. Work through it top to bottom with `SHIFT + ENTER`.

### What the notebook does

1. **Installs and imports** `scipy`, `pandas`, `requests`, `zipfile`, `io`
2. **Downloads** the UCI Vertebral Column dataset — streamed into memory and
   extracted, with a second mirror tried automatically if the first fails
3. **Verifies** the four extracted files
4. **Loads** `column_2C_weka.arff` into a pandas DataFrame
5. **Sanity-checks** shape, class balance and missing values
6. **Saves** `vertebral_column.csv` for Labs 3.2 and 3.4–3.7

### Expected output

```
Shape: (310, 7)
Class balance:
Abnormal    210
Normal      100
Missing values: 0 in every column
```

If you see 310 rows split 210/100, everything is correct.

### A gotcha to watch for

ARFF nominal values load as **byte strings** — `b'Abnormal'`, not `'Abnormal'`.
The notebook fixes this with:

```python
df['class'] = df['class'].str.decode('utf-8')
```

Skip that line and every later comparison like `df['class'] == 'Abnormal'`
silently returns `False`. Nothing raises an error; you simply get wrong
answers. It is a good reminder of why you inspect your data before you model
it.

### About the dataset

310 orthopaedic patients, six biomechanical measurements of the pelvis and
lumbar spine, labelled `Normal` (100) or `Abnormal` (210).

| Feature | Meaning |
|---|---|
| `pelvic_incidence` | Angle fixed by pelvic anatomy |
| `pelvic_tilt` | Pelvis rotation |
| `lumbar_lordosis_angle` | Inward curve of the lower spine |
| `sacral_slope` | Slope of the sacrum |
| `pelvic_radius` | Distance, hip axis to sacral plate |
| `degree_spondylolisthesis` | Forward slippage of a vertebra |

Keep this in mind for later: **`pelvic_incidence = sacral_slope + pelvic_tilt`**
exactly. In Lab 3.2 you will rediscover this from the correlation matrix.

## Task 4 — Saving your work

Your files live on the instance's EBS volume:

- **Stop** the instance → files **kept**, hourly billing **stops**
- **Delete** the instance → files **gone**

To keep a notebook permanently, right-click it in the file browser and choose
**Download**.

---

## Before you leave

- [ ] `vertebral_column.csv` exists in the file browser
- [ ] **Stop** the notebook instance if you are pausing here
      (SageMaker → Notebooks → select → **Stop**)

## Troubleshooting

| Symptom | Fix |
|---|---|
| No `ml-pipeline` in the lifecycle dropdown | Expected. Choose **None** |
| "Role Manager is no longer open to new customers" | You used the form's **Create a new role** link. Create the role in the **IAM** console instead — setup guide, section 5, Step 1b |
| The IAM role dropdown is empty | You have not created the execution role yet — setup guide, section 5, Step 1b |
| `ResourceLimitExceeded` | Quota is 0 — see setup guide section 4 |
| Both download mirrors fail | Run the offline fallback cell in the notebook |
| `ModuleNotFoundError: scipy` | Wrong kernel — switch to `conda_python3` |
| Class labels look like `b'Abnormal'` | The `.str.decode('utf-8')` line did not run |

**Next:** [Lab 3.2 — Exploring Data](Lab-3.2-Exploring-Data.md)
