# Cost Control Playbook
### How to run Module 3 for pennies, and never get a surprise bill

**Read this once before your first lab.** It takes ten minutes, and it is the
difference between spending $0.22 and spending $200.

---

## The one thing to understand

**AWS bills for resources that *exist*, not for resources you *use*.**

This is the single idea beginners get wrong, and every expensive mistake traces
back to it. A notebook instance you are not typing in costs exactly the same as
one you are. An endpoint receiving zero requests costs exactly the same as one
serving thousands.

> **The mental model:** you are renting a machine by the hour, not buying
> compute by the calculation. The meter runs until you switch the machine off.

Everything below follows from that.

---

## 1. The cost ladder — what actually costs what

Approximate `us-east-1` on-demand rates. Verify current prices at
[SageMaker pricing](https://aws.amazon.com/sagemaker-ai/pricing/).

| Resource | Rate | Stops by itself? | Risk |
|---|---|---|---|
| **Real-time endpoint** | $0.056–$0.28/hr | ❌ **Never** | 🔴 **Highest** |
| **Notebook instance** | $0.05–$0.23/hr | ❌ **Never** | 🟠 High |
| Tuning job (N × training) | N × rate | ✅ Yes | 🟡 Medium |
| Training job | $0.115–$0.23/hr | ✅ Yes | 🟢 Low |
| Batch transform | $0.115–$0.23/hr | ✅ Yes | 🟢 Low |
| EBS volume (storage) | ~$0.10/GB/month | — | 🟢 Negligible |
| S3 storage | ~$0.023/GB/month | — | 🟢 Negligible |

**Read the "stops by itself" column.** The two that never stop on their own are
the two that will hurt you. Everything else terminates automatically when its
work is done.

### What "forever" actually costs

| Resource left running | 1 day | 1 week | 1 month |
|---|---|---|---|
| `ml.t3.medium` notebook | $1.20 | $8.40 | **$36** |
| `ml.m5.xlarge` notebook (official lab type) | $5.52 | $38.64 | **$166** |
| `ml.t2.medium` endpoint | $1.34 | $9.41 | **$40** |
| `ml.m4.xlarge` endpoint (official lab type) | $6.72 | $47.04 | **$202** |

That last row is **twice a typical $100 credit balance**, from forgetting one
checkbox. It is the most common way people lose their credits.

---

## 2. The five habits

### Habit 1 — Stop the notebook instance every single time

**This is the highest-value habit in the whole module.** The notebook instance
is your dominant cost, because it is the thing that stays alive longest.

**SageMaker AI → Notebooks → select `MyNotebook` → Actions → Stop.**

| | Stopped | Deleted |
|---|---|---|
| Hourly compute charge | **$0** | $0 |
| Your files (`.ipynb`, `.csv`, models) | ✅ **Kept** | ❌ **Gone** |
| EBS storage charge | ~$0.0007/hr (5 GB) | $0 |
| Restart time | ~2 min | Recreate from scratch |

**Stop between lab sessions. Delete only when the whole module is finished.**

> Stopping takes 2–3 minutes to complete. You do not have to wait — it will
> finish on its own. But do check next session that it actually says `Stopped`.

### Habit 2 — Delete the endpoint in the same sitting you create it

Endpoints are the fastest way to burn a balance. Labs 3.5 and 3.7 delete them
for you and then verify — **do not skip those cells.**

**The rule: never create an endpoint you are not going to delete within the
hour.** If you are interrupted mid-lab, delete it before you walk away. You can
always recreate it in five minutes.

Verify by hand too: **SageMaker AI → Inference → Endpoints** should be empty.

> Deleting the *notebook instance* does **not** delete endpoints. They are
> separate resources. Neither does shutting your laptop, closing the browser,
> or logging out. **Only an explicit delete stops an endpoint.**

### Habit 3 — Prefer batch transform to endpoints

| | Real-time endpoint | Batch transform |
|---|---|---|
| Billing | Hourly, continuously, until deleted | Only while the job runs |
| Terminates itself | ❌ No | ✅ Yes |
| Latency | Milliseconds | Minutes of startup |

**Decision rule:** if no human is waiting for the answer *right now*, you do not
need an endpoint. Coursework, analytics, reporting and scoring a file are all
batch problems.

Lab 3.5 has you build both, deliberately — endpoint first, then batch — so you
feel the difference for yourself.

### Habit 4 — Right-size, and never default to bigger

The official labs specify `ml.m5.xlarge`. **The dataset is 310 rows and 6
columns.** An `ml.t3.medium` runs it indistinguishably fast for a fifth of the
price.

| Purpose | Official | **Use** | Saving |
|---|---|---|---|
| Notebook | `ml.m5.xlarge` ~$0.23/hr | **`ml.t3.medium`** ~$0.05/hr | **78%** |
| Training | `ml.m4/m5.xlarge` ~$0.23/hr | **`ml.m5.large`** ~$0.115/hr | **50%** |
| Endpoint | `ml.m4.xlarge` ~$0.28/hr | **`ml.t2.medium`** ~$0.056/hr | **80%** |

> **"Bigger is faster" is false here.** With 310 rows the job is dominated by
> instance *startup*, not computation. A larger instance finishes at the same
> wall-clock time and costs more. Size up only when you have measured a
> bottleneck.

### Habit 5 — Multiply before you raise `max_jobs`

Lab 3.7's tuning job runs `max_jobs` **separate billed instances**.

```
cost ≈ max_jobs × duration × hourly_rate

 4 jobs × 5 min × $0.115/hr ≈ $0.04   ← this pack's default
20 jobs × 5 min × $0.115/hr ≈ $0.19
20 jobs × 5 min × $0.23/hr  ≈ $0.38
```

In Lab 3.7 you will see that the best and tenth-best hyperparameter
combinations differ by 0.007 AUC — **less than the noise in the data.** More
jobs buy you almost nothing on a dataset this size. Spend the effort on better
features instead.

---

## 3. Free ways to cut your cost to near zero

### Use Track B

Every notebook has `USE_MANAGED_SAGEMAKER = False` at the top. Track B runs
training, inference and tuning **inside the notebook**:

- **Extra AWS cost: $0** — only the notebook instance bills
- No S3, no IAM role, no `ml.*` training or endpoint quota
- Identical model, identical metrics
- Faster (seconds, not minutes of provisioning)

**Track B is not a lesser version of the machine-learning content.** It is the
same content without the managed-infrastructure part.

### Run the pure-analysis labs anywhere, free

**Labs 3.2, 3.3 and 3.6 make no AWS API calls at all.** They are pandas,
Matplotlib and scikit-learn. You can run them on:

| Platform | Cost | Notes |
|---|---|---|
| **SageMaker Studio Lab** | Free | No AWS account needed; closest to the real thing |
| **Google Colab** | Free | Ubiquitous, no setup |
| **Your own laptop** | Free | Needs `pandas scipy scikit-learn xgboost matplotlib seaborn` |

A good plan: do 3.2, 3.3 and 3.6 for free off AWS, and save your paid AWS time
for 3.1, 3.4, 3.5 and 3.7, where SageMaker itself is the point.

### Batch your AWS session

Instance time is billed by the hour of *existence*. Doing four labs in one
3-hour sitting costs far less than four separate 1-hour sessions on different
days — you pay the startup and idle overhead once.

**Plan a single block:** open the console, create the instance, run 3.1 → 3.7,
stop the instance. One session, ~$0.22.

---

## 4. Guardrails to set up now

### A budget alarm (2 minutes — do this today)

**Billing and Cost Management → Budgets → Create budget**

- Template: **Monthly cost budget**
- Budgeted amount: **$5**
- Alert threshold: **80%** of the budgeted amount
- Email: yours — **and confirm the subscription email AWS sends you**

This will not stop spending; it tells you it is happening. That is enough,
because every runaway cost here is fixed by deleting one resource.

> **Important caveat:** budget alerts are based on data that updates roughly
> every 24 hours. They are a safety net, not a real-time tripwire. The habits
> above are your actual protection.

### Check the billing dashboard

**Billing → Bills** shows charges by service. Check it the day after any lab
session. If SageMaker shows more than a few cents, something is still running.

### Put your credit expiry in your calendar

Find the date under **Billing and Cost Management → Credits**. After it,
everything bills to your card at standard rates. Before then, delete every
resource you no longer need — especially anything with an hourly charge.

---

## 5. The end-of-session ritual

Run this every time, in this order. It takes 90 seconds.

1. **Endpoints** — SageMaker AI → **Inference → Endpoints** → the list must be
   **empty**
2. **Training jobs** — Training → **Training jobs** → nothing `InProgress`
3. **Tuning jobs** — Training → **Hyperparameter tuning jobs** → nothing
   `InProgress`
4. **Notebook instance** — Notebooks → **Stop** (or **Delete** if you are
   finished)
5. **Tomorrow** — Billing → **Bills** → confirm the number is what you expect

Labs 3.5 and 3.7 include a cell that automates checks 1–3:

```python
sm = boto3.client('sagemaker')
print('Endpoints running:', len(sm.list_endpoints()['Endpoints']))
```

Run it at the end of *every* session, not just those two labs.

---

## 6. If you are sharing an AWS account with others

Most of the time you will be working in your own account, and the habits above
are all you need. If you are working in an account shared with other people,
two extra rules apply:

- **Name your resources with something identifying you** (for example
  `MyNotebook-<yourname>`), so nobody stops or deletes each other's work by
  mistake.
- **Be twice as strict about endpoints.** In a shared account, one forgotten
  endpoint drains everyone's balance, not just yours. Check the Endpoints list
  before you close the browser, every single time.

If you have a free-tier account of your own available, prefer it: you get your
own credits, and nothing you do can cost anyone else money.

---

## 7. Quick reference

**The three sentences that matter:**

1. **Stop the notebook instance when you finish.**
2. **Delete the endpoint in the same sitting you create it.**
3. **Check the Endpoints list is empty before you close the browser.**

**Costs at a glance:**

| | Cost |
|---|---|
| This pack, Track B | ~$0.15 |
| This pack, Track A | ~$0.22 |
| Official instructions, literally | ~$1.06 |
| One forgotten `ml.m4.xlarge` endpoint, one month | **~$202** |

---

**Next:** [`02-Beginner-Primer.md`](02-Beginner-Primer.md) if AWS or Jupyter are
new to you · otherwise
[Lab 3.1](Lab-3.1-Creating-and-Importing-Data.md)
