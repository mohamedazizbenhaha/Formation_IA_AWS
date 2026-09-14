# Lab 5 — Setup, Feasibility & Cost
### Amazon Rekognition facial recognition, on a personal AWS account

**Read this before opening the lab.** It is short, because this is the cheapest
and simplest lab in the course.

---

## 1. The short answer: yes, and it is nearly free

**Lab 5 is fully feasible on a personal AWS account, and there is no blocker.**

| Question | Answer |
|---|---|
| Needs an `ml.*` quota increase? | **No** |
| Needs a running instance? | **No** — optional |
| Anything that bills by the hour? | **Only if you choose SageMaker** |
| Realistic cost | **$0.00 – $0.05** |
| Hard blockers | **None** |

Amazon Rekognition is a **fully managed API**. You send it an image, it sends
back an answer, you are billed per call. There is nothing to provision, no
quota to request, and nothing that keeps billing while you are not looking.

### What it costs

| Item | Price |
|---|---|
| Free tier | **1,000 images/month for 12 months** |
| After free tier | ~**$0.001** per image |
| Face metadata storage | ~**$0.00001** per face per month |

**This lab makes about 15 API calls.** Even with no free tier at all, that is
**under two cents**. You could run the whole lab 60 times a month and stay
inside the free allowance.

---

## 2. The one thing that could cost you money

Nothing in Rekognition bills by the hour. **The only hourly meter in this lab is
a SageMaker notebook instance — and you do not need one.**

| Instance left running | 1 day | 1 week | 1 month |
|---|---|---|---|
| `ml.t3.medium` | $1.20 | $8.40 | **$36** |

### You can avoid this entirely

Rekognition is just a web API. The notebook needs only `boto3`, `Pillow` and
AWS credentials — **no machine learning runs on your machine**. So Lab 5 runs
identically on:

| Where | Cost | Setup | Use when |
|---|---|---|---|
| **AWS CloudShell** | **$0** | None — already signed in | ⭐ Running it yourself |
| Your laptop | $0 | `pip install boto3 pillow matplotlib`, `aws configure` | You have Python already |
| Google Colab | $0 | Paste AWS keys — see the warning below | Quick and disposable |
| SageMaker notebook `ml.t3.medium` | ~$0.05/hr | Create instance, wait 5 min | Teaching — students see JupyterLab |

> **If you do use a SageMaker notebook, Stop it when you finish.**
> SageMaker AI → Notebooks → select → **Actions → Stop**.
> *Stopped* keeps your files and ends the hourly charge; *Deleted* also removes
> the files.

> ⚠️ **Never paste long-lived AWS access keys into Google Colab** or any shared
> notebook service. If you must, create a dedicated IAM user limited to
> Rekognition, and delete the keys afterwards.

---

## 3. What the official lab depends on that you will not have

The original lab page assumes the Vocareum-provisioned AWS Academy environment.

| Missing piece | What the lab says | Why it is not there | Fix |
|---|---|---|---|
| **The notebook** | "Open `en_us/05-facedetection.ipynb`" | Placed by a Vocareum lifecycle configuration | **Generated** → `notebooks/05-facedetection.ipynb` |
| **A notebook instance named `MyNotebook`** | "Look for the notebook instance named MyNotebook" | Pre-created by the sandbox | Create one, **or skip SageMaker entirely** (section 2) |
| **Face images** | Assumed present | Never provided | The notebook downloads public-domain portraits automatically |
| **Rekognition permissions** | Pre-granted | Sandbox role | Attach `AmazonRekognitionFullAccess` (section 5) |

**The notebook is the important one.** The official lab page contains no
technical content of its own — it says "open this notebook and follow the
instructions in it". Without the notebook there is nothing to teach.

---

## 4. Pre-flight check (3 minutes)

1. **Region** — top-right of the console. Use **US East (N. Virginia) /
   `us-east-1`**.
   > Resources are region-scoped. A Rekognition collection created in one
   > region is invisible in another. If something "disappears", check here
   > first.
2. **Budget alarm** — Billing and Cost Management → **Budgets** →
   **Create budget** → *Monthly cost budget*, **$5**, alert at **80%**, your
   email. **Confirm the subscription email AWS sends.** Two minutes, and it is
   your safety net.
3. **Rekognition** — search for it in the console; it should open normally.
4. **Decide where to run** — CloudShell (free) or a SageMaker notebook
   (~$0.05/hr).

There is no quota step. That is the advantage of this lab.

---

## 5. Permissions

Whatever identity runs the notebook needs **`AmazonRekognitionFullAccess`**.

### On a SageMaker notebook instance

1. **SageMaker AI → Notebooks** → click `MyNotebook`
2. Under **Permissions and encryption**, click the **IAM role ARN** — it opens
   in the IAM console
3. **Add permissions → Attach policies**
4. Search `AmazonRekognitionFullAccess`, tick it, **Add permissions**

### On CloudShell or your laptop

Your IAM user needs the same policy. If you are the account owner, you already
have it.

> The notebook's Step 2 verifies your credentials with `sts:GetCallerIdentity`
> and prints a clear message if this is wrong — much better than a confusing
> failure five cells later.

---

## 6. Files in this folder

```
Lab5-Facial-Recognition/
├── 00-START-HERE-Setup-and-Cost.md     <- this file
├── Lab-5-Facial-Recognition.md         <- the step-by-step guide
└── notebooks/
    └── 05-facedetection.ipynb          <- replaces the missing lab notebook
```

**This folder is self-contained.** It does not depend on any other lab pack.

### What was verified before shipping

| Item | How |
|---|---|
| Image downloads | All three portraits fetched — valid RGB JPEGs at 960px |
| Bounding-box drawing | Ratio→pixel conversion and PIL rendering executed |
| Notebook syntax | All 16 code cells compile |
| Dataset licensing | US federal government works — public domain |

**Not verified:** the live Rekognition API calls, which need a live account with
the service enabled. Run it once yourself before teaching it.

---

## 7. Before you start: responsible use

This deserves five minutes of class time, not a footnote.

- **Consent.** Faces are biometric data. Under GDPR (EU), BIPA (Illinois) and
  similar laws, collecting or processing them without explicit informed consent
  can be unlawful.
- **Accuracy is not uniform.** NIST's Face Recognition Vendor Test has
  repeatedly found error rates vary substantially by sex and skin tone. A single
  headline accuracy figure conceals this.
- **Errors have consequences.** A false match in policing or access control
  affects a real person.

**This lab uses public-domain official portraits of public figures** — US
federal government works — not photos of students. If a student prefers to use
their own photo, that is their own face and their own consent. **Nobody should
upload photographs of other people without asking them.**

---

## 8. Cleanup checklist

- [ ] Rekognition collection deleted — the notebook's last step does this
- [ ] `list_collections` returns empty
- [ ] **If you used a SageMaker notebook instance: Stopped or Deleted** ← the
      only thing that bills hourly
- [ ] Downloaded face images removed (optional; the notebook offers this)
- [ ] Tomorrow: **Billing → Bills** → confirm the figure is cents, not dollars

---

**Next:** [Lab 5 — Facial Recognition](Lab-5-Facial-Recognition.md)

---

*Adapted from the AWS Academy Machine Learning Foundations lab for use outside
the Vocareum sandbox. Original lab content © Amazon Web Services, Inc.*
