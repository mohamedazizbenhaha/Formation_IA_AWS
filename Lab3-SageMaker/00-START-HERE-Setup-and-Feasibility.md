# Module 3 on your own AWS account — Start here

**Read this before you run any lab.** It tells you what the official AWS Academy
labs rely on that your own account will not have, and it gets your environment
ready.

---

## 1. Can you run these labs outside the AWS Academy sandbox? Yes

**Labs 3.1–3.7 run on an ordinary personal AWS account.** You need three
things, and none of them is unusual:

| You need | Where it comes from |
|---|---|
| A normal AWS account with console access | Sign up at aws.amazon.com |
| Amazon SageMaker AI available in your region | Available by default |
| Quota for `ml.*` instance types | May need one free request — see section 4 |

An AWS account on the **Free account plan** normally comes with **$100 in
credits, valid for 12 months.** That is far more than this module needs.

> **The ~$1 charge on your card when you sign up** is a card-verification
> authorisation hold, not a spending cap. It is normally reversed within a few
> days.

### Free plan vs Paid plan

| | Free account plan | Paid account plan |
|---|---|---|
| Service access | A selected subset of services | All services |
| Charges beyond your credits | Cannot occur | Billed to your card |
| **When credits run out or the term ends** | **The account closes automatically** | The account stays open |

SageMaker works on the Free plan — you do not need to upgrade to run this
module. AWS excludes services "that could possibly deplete your credits" from
the Free plan, naming Savings Plans, Reserved Instances and certain Marketplace
offers. SageMaker is not among them.

> **The one reason to upgrade later:** on the Free plan your account *closes*
> when credits are exhausted or the plan term ends (AWS keeps your data for 90
> days before deleting it). If you want to keep the account long-term,
> upgrading protects it. That is a decision for after the module — it is not
> needed here.

### The one thing that genuinely blocks people: `ml.*` quota

New AWS accounts often have a **quota of 0** for `ml.*` instance types, and
approval is **not instant**. This is the only realistic blocker you will meet.
See section 4, and **check it at least a day before you need to run a lab** —
not in the hour you sit down to work.

### The IAM prompt is normal

The create-notebook form asks you for an **IAM role**. That is expected, not an
obstacle — every notebook instance needs one so it can reach S3.

**Create it in the IAM console before you start the form.** The "Create a new
role" shortcut inside the form now leads to the retired Amazon SageMaker Role
Manager on many accounts, which cannot create it. Section 5, Step 1b gives the
exact click-path. It takes about a minute.

### Budget

With $100 in credits, budget is not a constraint here:

- Following the official lab instructions literally: **~$1.06**
- Following this guide's settings, Track A: **~$0.22**
- Track B: **~$0.15**

Follow the efficiency guidance anyway, because:

- Credits expire after 12 months; after that everything bills to your card
- A single forgotten endpoint costs ~$0.28/hr **indefinitely** — about
  **$200/month**

See **`01-Cost-Control-Playbook.md`** for the full set of habits.

---

## 2. The 10-minute pre-flight check

Do this once, ideally a day or more before your first lab session.

**Step 1 — Confirm your region.**
Look at the top-right of the console. Use **US East (N. Virginia) /
`us-east-1`** — it has the widest instance availability and the lowest prices.
*Resources are region-specific: create a notebook in one region and it is
invisible in another.* This catches almost everyone at least once.

**Step 2 — Confirm your credits.**
**Billing and Cost Management → Credits.** You should see your remaining
balance and an expiry date. **Put that date in your calendar.**

**Step 3 — Set a budget alarm. Do not skip this.**
**Billing and Cost Management → Budgets → Create budget**:

- Template: **Monthly cost budget**
- Amount: **$5**
- Alert at **80%** of the budgeted amount
- Enter your email address, then confirm the subscription email AWS sends you

Two minutes now. This is what catches the mistake you did not anticipate.

**Step 4 — Open SageMaker.**
Search for **SageMaker AI** in the console search bar. It should open normally.

**Step 5 — Check your quota. This is the make-or-break step.**
Go to **Notebooks → Create notebook instance**, then open the **Notebook
instance type** dropdown.

- `ml.t3.medium` is listed → **you are clear**
- The dropdown is empty, or creation later fails with `ResourceLimitExceeded` →
  **go to section 4 and request quota now**

**Step 6 — Create the role and the instance** (section 5).

> **If your quota request is refused or delayed**, use **Track B** (section 5,
> Step 3). Every notebook also runs on SageMaker Studio Lab (free, no AWS
> account), Google Colab, or your own laptop. You lose the managed-SageMaker
> part of the story but keep 100% of the machine-learning content. **Nothing in
> this pack becomes unusable.**

---

## 3. What the official labs rely on that you will not have

The official `.mhtml` lab pages assume the Vocareum-provisioned AWS Academy
environment. Four things are missing outside it:

| Missing piece | What the official lab says | Why it is not there | What to do instead |
|---|---|---|---|
| **The notebooks themselves** | "Open `en_us/3_2-machinelearning.ipynb`" | Placed on the instance by a Vocareum lifecycle configuration | **Provided in this pack** — see `notebooks/` |
| **Lifecycle configuration `ml-pipeline`** | "Choose the lifecycle configuration that contains `ml-pipeline`" | Vocareum-specific | Skip it. Upload the notebooks yourself (section 5) |
| **A ready-made IAM execution role** | Assumed silently | Created by the sandbox | Create one yourself in IAM (section 5, Step 1b) |
| **Pre-granted service quotas** | Assumed silently | Sandbox accounts are pre-provisioned | Request them (section 4) |

**The biggest gotcha:** Labs 3.2 through 3.7 consist almost entirely of "open
this notebook and follow the instructions inside it." The lab pages contain no
machine-learning content of their own. Without the notebooks there is nothing
to work through. That is why this pack includes them.

---

## 4. Service quotas — check this early

New AWS accounts frequently have a **quota of 0** for `ml.*` instance types.
You will not find out until instance creation fails with
`ResourceLimitExceeded`.

**Approval is not instant** — anywhere from minutes to a couple of business
days, and a brand-new account with no billing history is more likely to wait.
Check at least a day before you need it.

Go to **Service Quotas → AWS services → Amazon SageMaker** and confirm:

| Quota | Needed for | Minimum |
|---|---|---|
| `ml.t3.medium for notebook instance usage` | All labs | 1 |
| `ml.m5.large for training job usage` | Labs 3.4 and 3.7, Track A | 1 (2 for tuning) |
| `ml.t2.medium for endpoint usage` | Lab 3.5, Track A | 1 |

**Track B needs only the first row.** If a quota request is slow or refused,
Track B keeps you moving.

---

## 5. Setting up

### Step 1 — Create the notebook instance

Console → **SageMaker AI → Notebooks → Create notebook instance**:

| Field | Official lab | **Use this** | Why |
|---|---|---|---|
| Name | `MyNotebook` | `MyNotebook` | Keep it — the lab text refers to it |
| **Instance type** | `ml.m5.xlarge` | **`ml.t3.medium`** | ~$0.05/hr vs ~$0.23/hr. Ample for 310 rows |
| Platform identifier | `notebook-al2023-v1` | **Amazon Linux 2023, Jupyter Lab 4** (this *is* `notebook-al2023-v1`) | The only option now — older platforms are retired |
| **Lifecycle configuration** | `...ml-pipeline` | **None** | Does not exist in your account |
| Volume size | default (5 GB) | 5 GB (**25 GB** for the challenge lab) | Module 3 data is tiny |
| IAM role | (ready-made) | **Create one in IAM first** — see Step 1b | Needed for Track A |

Creation takes 2–5 minutes.

> If you have credits to spare, `ml.m5.xlarge` is affordable if you prefer to
> match the official lab exactly. `ml.t3.medium` is still the better default —
> it is 4.5× cheaper and the dataset is 310 rows.

### Step 1b — The IAM role, click by click

The form stops and asks for an **IAM role**. This is normal. An IAM role is
simply the set of permissions the notebook itself uses when it talks to other
AWS services — mainly to read and write S3. The notebook cannot be created
without one.

**What is IAM?** *Identity and Access Management* — AWS's permissions system.
A **role** is a bundle of permissions that a *service* (not a person) assumes.
Your notebook instance "wears" this role whenever it calls AWS.

> ### ⚠ Do not use "Create a new role" in the notebook form
>
> Older guides — including the official lab — tell you to open the **IAM role**
> dropdown and choose **Create a new role**. On current accounts that can send
> you to **Amazon SageMaker Role Manager**, which greets you with:
>
> > *Amazon SageMaker Role Manager is no longer open to new customers.*
>
> That is a dead end. Role Manager has been retired and cannot create the role
> for you. **Create the role in the IAM console first, then come back and
> select it.** The steps below do exactly that, and they work regardless of
> which version of the console you get.

**Part 1 — create the role in IAM** (about one minute)

1. Open the **IAM** console — search for "IAM" in the console search bar. IAM
   is a global service, so the region selector does not matter here.
2. In the left navigation, choose **Roles**, then **Create role**.
3. **Trusted entity type:** **AWS service**.
4. Under **Use case**, select **SageMaker**, then choose the
   **SageMaker - Execution** use case.
   > On some console versions SageMaker is not shown as a tile. Open the
   > *"Use case for other AWS services"* dropdown, pick `SageMaker`, then
   > select `SageMaker - Execution`.
5. Choose **Next**. The `AmazonSageMakerFullAccess` policy is already attached
   for you — add nothing else. Choose **Next** again.
6. **Role name:** `SageMakerExecutionRole`
7. Choose **Create role**.

**Part 2 — select it in the notebook form**

8. Return to **SageMaker AI → Notebooks → Create notebook instance**.
9. Scroll to the **Permissions and encryption** section.
10. Open the **IAM role** dropdown and choose **`SageMakerExecutionRole`** from
    the list of existing roles.

**You only do this once** — reuse the same role for every later notebook
instance and every training job.

**What about S3 access?** `AmazonSageMakerFullAccess` already grants read and
write on any bucket whose name contains `sagemaker`, `SageMaker`, `Sagemaker`
or `aws-glue`. Track A uploads training data to, and reads model artifacts
from, the automatically created `sagemaker-us-east-1-<account-id>` bucket — so
it is covered and you need nothing extra. (This is what the old "Any S3 bucket"
checkbox was for; you no longer need it.) If you later point the notebooks at a
bucket you named yourself, attach `AmazonS3FullAccess` to this role as well, or
add a policy scoped to that bucket.

> **If you cannot create a role at all** — **Create role** is greyed out, or
> you get an access-denied error — you are signed in as an IAM user that lacks
> `iam:CreateRole`. Sign in as the account owner, or ask whoever administers
> the account to create the role for you or to attach `IAMFullAccess`. If
> neither is possible, **Track B needs no role at all** and every lab still
> runs.

### Step 2 — Upload the notebooks

Because there is no lifecycle configuration, you upload them yourself:

1. Choose **Open JupyterLab** on your instance.
2. Click the **upload** arrow (↑) in the left file browser.
3. Upload all eight `.ipynb` files from this pack's `notebooks/` folder.
4. When a notebook asks you for a kernel, choose **`conda_python3`**.

If the files are in a Git repository instead, you can run one cell —

```bash
!git clone https://github.com/<owner>/<repo>.git && mv <repo>/*.ipynb .
```

— or attach the repository when you create the instance, under **Additional
configuration → Git repositories**.

### Step 3 — Pick your track

Every notebook from 3.4 onward starts with:

```python
USE_MANAGED_SAGEMAKER = False
```

| | **Track A** (`True`) | **Track B** (`False`) |
|---|---|---|
| Where training runs | Managed SageMaker jobs | Inside the notebook |
| Extra cost | ~$0.07 for the module | **$0** |
| Needs S3 + IAM role | Yes | No |
| Needs `ml.*` training/endpoint quota | **Yes** | No |
| You learn | ML concepts **+ the SageMaker workflow** | ML concepts |

> ### 👉 If you have credits, run **Track A**.
>
> Set `USE_MANAGED_SAGEMAKER = True` in notebooks 3.4–3.7. The whole module
> costs about **$0.22**, and Track A is the one that actually exercises
> SageMaker: real training jobs, a real endpoint, batch transform, and a real
> tuning job. Since SageMaker is the point of Module 3, this is the version to
> aim for.
>
> **Keep Track B as your safety net.** If a quota request is denied, or
> something breaks, flip the flag to `False` and everything still runs, with
> identical results and no AWS dependencies at all.

Both tracks produce the same model and the same metrics. Every cell checks the
flag and skips itself when it does not apply, so you can safely run all cells
top to bottom either way.

---

## 6. What it actually costs

Prices are **us-east-1 on-demand, approximate**; confirm current rates on the
[SageMaker pricing page](https://aws.amazon.com/sagemaker-ai/pricing/).

### Following the official instructions literally

| Item | Rate | Time | Cost |
|---|---|---|---|
| `ml.m5.xlarge` notebook | ~$0.23/hr | 3 hr session | $0.69 |
| Training `ml.m5.xlarge` (Lab 3.4) | ~$0.23/hr | ~5 min billed | $0.02 |
| Endpoint `ml.m4.xlarge` (Lab 3.5) | ~$0.28/hr | 30 min | $0.14 |
| Batch transform | ~$0.23/hr | ~5 min | $0.02 |
| Tuning, 10 jobs (Lab 3.7) | ~$0.23/hr | ~5 min each | $0.19 |
| **Total** | | | **≈ $1.06** |

Affordable on $100 of credits — about 1% of the balance. This is a perfectly
reasonable way to run the module if you want to match the official lab exactly.

### Using this guide's settings — Track A (recommended)

| Item | Rate | Time | Cost |
|---|---|---|---|
| `ml.t3.medium` notebook | ~$0.05/hr | 3 hr | $0.15 |
| Training `ml.m5.large` | ~$0.115/hr | ~5 min | $0.01 |
| Endpoint `ml.t2.medium`, **deleted promptly** | ~$0.056/hr | 15 min | $0.01 |
| Batch transform `ml.m5.large` | ~$0.115/hr | ~5 min | $0.01 |
| Tuning, **4 jobs** `ml.m5.large` | ~$0.115/hr | ~5 min each | $0.04 |
| **Total** | | | **≈ $0.22** |

### Track B

| Item | Rate | Time | Cost |
|---|---|---|---|
| `ml.t3.medium` notebook | ~$0.05/hr | 3 hr | **$0.15** |
| Everything else | — | — | **$0.00** |

### The one number to remember

| Scenario | Cost |
|---|---|
| Whole module, Track A, this guide's settings | ~$0.22 |
| Whole module, official instance types | ~$1.06 |
| **One endpoint forgotten for a month** | **~$200** ⚠ |

That last row is why the cleanup steps matter far more than the choice of
instance size.

### The rules that protect your balance

1. **Stop the notebook instance** whenever you are not using it. This is your
   dominant cost — it bills by the hour whether or not you are typing.
   *Stopped* keeps your files; *deleted* loses them.
2. **Delete every endpoint the moment you are done with it.** Endpoints bill
   continuously and are the number-one cause of surprise bills. Labs 3.5 and
   3.7 delete them for you and then verify — do not skip those cells.
3. **Keep the budget alarm** from section 2. It catches the mistake you did not
   think of.
4. **Never raise `max_jobs`** in Lab 3.7 without doing the multiplication
   first. Each job is a separately billed instance.
5. **Put your credit expiry date in your calendar.** After it, everything bills
   to your card at standard rates. Delete leftover resources before then.

---

## 7. Files in this pack

```
Module3-Educate-Edition/
├── 00-START-HERE-Setup-and-Feasibility.md   <- this file
├── 01-Cost-Control-Playbook.md              <- read before your first lab
├── 02-Beginner-Primer.md                    <- if AWS or Jupyter are new to you
├── Lab-3.1-Creating-and-Importing-Data.md
├── Lab-3.2-Exploring-Data.md
├── Lab-3.3-Encoding-Categorical-Data.md
├── Lab-3.4-Training-a-Model.md
├── Lab-3.5-Deploying-a-Model.md
├── Lab-3.6-Model-Performance-Metrics.md
├── Lab-3.7-Hyperparameter-Tuning.md
├── Challenge-Lab-3-Flight-Delays.md
└── notebooks/
    ├── 3_1-machinelearning.ipynb  ...  3_7-machinelearning.ipynb
    └── Flight_Delay-Student.ipynb
```

Each `Lab-3.x` guide mirrors the structure of the official lab page and states
exactly where it differs and why.

**About the results quoted in these guides.** Every "expected output" block was
produced by running the notebooks end to end on the real data: 310 rows loaded,
an 80/10/10 stratified split holding 67.7% Abnormal in every partition, and a
model scoring **83.9% accuracy / 0.919 AUC** against a 67.7% majority-class
baseline. The challenge lab was run against real BTS data: 1.2M rows processed,
final **AUC 0.762**. Those figures came from Track B; on Track A the numbers are
the same, because both tracks train the same model with the same
hyperparameters.

---

## 8. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| The form asks for an **IAM role** | Normal — every instance needs one | Section 5, Step 1b. Takes about a minute |
| `AccessDenied` creating the IAM role | Signed in as a non-admin IAM user | Sign in as the account owner, or use Track B (needs no role) |
| "Role Manager is no longer open to new customers" | The in-form "Create a new role" link routes to the retired Role Manager | Create the role in the **IAM** console instead — section 5, Step 1b |
| SageMaker missing from search | **Wrong region** | Set the region selector to **US East (N. Virginia)** |
| A notebook instance has "disappeared" | You are looking in a different region | Switch back to the region you created it in |
| "Upgrade your account plan to use this service" | You are on the **Free** plan, for a genuinely restricted service | Does not apply to SageMaker. If you see it elsewhere, see section 1 |
| No `ml-pipeline` lifecycle config | Vocareum-only | Expected. Choose **None** and upload the notebooks yourself |
| `ResourceLimitExceeded` on create | Your quota is 0 | Request an increase (section 4) |
| Instance type dropdown is empty | No `ml.*` quota | Request an increase |
| `AccessDenied` on `get_execution_role()` | Role misconfigured | Recreate the role with S3 access, or use Track B |
| `ClientError` on S3 upload | Role lacks S3 permissions | Attach `AmazonS3FullAccess`, or use Track B |
| `ModuleNotFoundError: xgboost` | Wrong kernel | Switch to `conda_python3`; otherwise `!pip install xgboost` |
| Dataset download fails | No outbound internet | Lab 3.1 has an offline fallback cell |
| `FileNotFoundError: vertebral_column.csv` | Labs run out of order | Run Lab 3.1 first |
| Files vanished between sessions | The instance was **deleted**, not stopped | Re-run Lab 3.1; next time *stop* it instead |
| Unexpected charges appearing | Something is still running | Check Endpoints, Notebooks and Training jobs |

---

## 9. Before you finish — cleanup checklist

- [ ] All endpoints deleted (Labs 3.5 and 3.7 verify this; check the console too)
- [ ] No training or tuning jobs still `InProgress`
- [ ] Notebook instance **Stopped** (or **Deleted** if you are finished for good)
- [ ] Optional: empty the `sagemaker-<region>-<account-id>` S3 bucket
- [ ] Check **Billing → Bills** the next day to confirm your actual spend
- [ ] Confirm your **credit expiry date** is in your calendar

---

**Next:** [`01-Cost-Control-Playbook.md`](01-Cost-Control-Playbook.md)

*Adapted from the AWS Academy Machine Learning Foundations labs for use outside
the Vocareum sandbox. The original lab content is © Amazon Web Services, Inc.
These are study aids for that course, not a replacement for it.*

**Sources for the account-plan details:**
[AWS Free Tier announcement](https://aws.amazon.com/about-aws/whats-new/2025/07/aws-free-tier-credits-month-free-plan/) ·
[AWS Billing docs — Free Tier](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier.html) ·
[AWS Free Tier FAQs](https://aws.amazon.com/free/free-tier-faqs/) ·
[SageMaker pricing](https://aws.amazon.com/sagemaker-ai/pricing/)
