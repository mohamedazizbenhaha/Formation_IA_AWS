# Lab 6 — Setup, Feasibility & Cost
### Amazon Lex chatbot, on a personal AWS account

**Read this before opening the lab.** Lab 6 is cheap but has more moving parts
than any other lab in the course, and two resources the official instructions
assume already exist.

---

## 1. The short answer: yes, and nothing bills by the hour

**Lab 6 is fully feasible on a personal AWS account.**

| Question | Answer |
|---|---|
| Needs an `ml.*` quota increase? | **No** |
| Needs a running instance? | **No** |
| Anything that bills by the hour? | **Nothing at all** |
| Realistic cost | **~$0.04** |
| Hard blockers | **None** |

Every service in this lab is **serverless and per-request**. Lex, Lambda,
Cognito and S3 all charge for what you use. **An idle bot costs $0. An idle
Lambda costs $0.** There is no meter to forget about.

### What it costs

| Service | Free tier | Beyond it | This lab uses |
|---|---|---|---|
| **Lex** (text) | Credits apply | ~$0.00075/request | ~50 requests ≈ **$0.04** |
| **Lambda** | 1M requests/month, **permanently** | — | ~50 invocations = **$0** |
| **Cognito** identity pools | Free | — | 1 pool = **$0** |
| **S3** | 5 GB for 12 months | ~$0.023/GB/month | 2 files ≈ 10 KB ≈ **$0** |

**Total: about four cents.** Speech requests cost ~5× text ($0.004 vs
$0.00075), but this lab is text-only by design.

---

## 2. The real risk here is security, not cost

Lab 6 has no runaway-cost trap. It has something else worth taking seriously.

### 🟠 The lab makes an S3 bucket publicly readable

Task 6 has you turn **off** Block Public Access and attach a public-read bucket
policy. That is genuinely required for S3 static website hosting — but it leaves
a bucket that anyone on the internet can read.

**Rules while it exists:**

- Put **only** `index.html` and `error.html` in that bucket. Nothing else, ever.
- Do not reuse this bucket for anything afterwards.
- **Delete it when the lab is finished** (section 7).

The danger is not the lab itself. It is a forgotten public bucket that someone
later uploads something sensitive into.

### 🟠 The Cognito unauthenticated role is assumable by anyone

Your webpage hands out temporary AWS credentials to anonymous visitors. That is
the whole point of a Cognito identity pool — but it means **anyone who loads
your page can assume that role**.

Give it exactly one thing:

```json
{ "Effect": "Allow", "Action": ["lex:RecognizeText"], "Resource": "*" }
```

**Never attach `AmazonLexFullAccess`** — that would let any visitor delete your
bot.

> **On the IDs in your page source:** `index.html` contains a Cognito identity
> pool ID and a bot ID. Those are **not secrets** — identity pool IDs are
> designed to be public. The security comes entirely from how tightly the
> unauthenticated role is scoped, which is why the point above matters.

---

## 3. What the official lab depends on that you will not have

This lab has the largest gap of any in the course — **four** missing pieces, and
two of them are genuinely misleading.

| Missing piece | What the lab says | Why it is not there | Fix |
|---|---|---|---|
| **`LexRole` IAM role** | "Under Existing role select **LexRole**" | Pre-created by Vocareum | **Does not exist.** Lab guide, Task 2a |
| **`MyIdentityPool` Cognito pool** | "Choose **MyIdentityPool**" | Pre-created by Vocareum | **Does not exist.** Lab guide, Task 5 |
| **`index.html` / `error.html`** | "Download the following two webpage files" | Vocareum-hosted download link | **Generated** → `lab6-assets/` |
| **Lambda code** | Pasted inline in the lab page | Targets Lex **V1**, and the page mangles it | **Rewritten and tested** → `lab6-assets/lambda_function.py` |

> ### The trap worth knowing about in advance
> The official lab reads as though `LexRole` and `MyIdentityPool` already
> exist — "select this", "choose that". On your account they do not, and the
> lab never explains how to create them. You will hit a dropdown with nothing
> in it and no guidance.
>
> **Tasks 2a and 5 of the lab guide create both.** That is the main reason this
> lab takes ~90 minutes rather than the official 60.

---

## 4. Pre-flight check (5 minutes)

1. **Region** — top-right of the console. Use **US East (N. Virginia) /
   `us-east-1`**.
   > ⚠️ **This matters more in Lab 6 than anywhere else.** Lex bots, Lambda
   > functions, Cognito pools and S3 buckets are *all* region-scoped. Mixing
   > regions is the single most common way this lab fails, and the error
   > messages do not tell you that is the problem.
2. **Budget alarm** — Billing and Cost Management → **Budgets** →
   *Monthly cost budget*, **$5**, alert at **80%**, your email. Confirm the
   subscription email.
3. **Lex** — search for **Amazon Lex**. Make sure you land on the **Lex V2**
   console: the left navigation should say **Bots**. *This lab is V2 only.*
4. **Lambda, Cognito, S3** — confirm each opens. No setup needed yet.

There is no quota step, and nothing to provision in advance.

---

## 5. What you will build

```
   Browser (index.html on S3)
        │  1. get temporary credentials
        ▼
   Amazon Cognito  ──── identity pool, unauthenticated role
        │  2. RecognizeText (signed with those credentials)
        ▼
   Amazon Lex V2  ──── ScheduleAppointment bot, MakeAppointment intent
        │  3. code hook on every turn
        ▼
   AWS Lambda  ──── MakeAppointmentCodeHook (validation + booking)
```

**Why Cognito is in the picture:** a static webpage has no AWS credentials and
cannot safely hold any — anyone can read the page source. Cognito issues
short-lived, tightly-scoped *unauthenticated* credentials to anonymous visitors
so the page can call Lex without you ever embedding a secret.

---

## 6. Files in this folder

```
Lab6-Lex-Chatbot/
├── 00-START-HERE-Setup-and-Cost.md      <- this file
├── Lab-6-Lex-Chatbot.md                 <- the step-by-step guide
└── lab6-assets/
    ├── lambda_function.py               <- tested Lex V2 code hook
    ├── index.html                       <- the chatbot webpage
    ├── error.html
    ├── bucket-policy.json               <- S3 public-read template
    ├── lexrole-trust-policy.json        <- LexRole trust policy
    └── cognito-unauth-policy.json       <- lex:RecognizeText for the webpage
```

**This folder is self-contained.** It does not depend on any other lab pack.

### What was verified before shipping

| Item | How |
|---|---|
| **Lambda function** | **Executed against 13 synthetic Lex V2 events — all pass** |
| Validation rules | Bad appointment type, past date, Sunday, out-of-hours, wrong increment, unavailable slot |
| Duration logic | Root canal (60 min) correctly offered fewer slots than a cleaning (30 min) |
| Determinism | Same date returns identical availability across runs |
| `index.html` | Rendered in a browser; config guard fires; chat bubbles verified |
| **AWS SDK dependency** | **`AWS.LexRuntimeV2` constructs, `recognizeText` present** |
| Policy JSON | All three parse |

**Not verified:** a live Lex bot, a real Lambda invocation from Lex, and the
deployed webpage end to end. That needs a live account. **Rehearse once before
teaching.**

---

## 7. Cleanup — in priority order

1. **Empty and delete the S3 bucket** ← most important; it is public
   *(S3 → bucket → **Empty**, then **Delete**)*
2. **Delete the Cognito identity pool** — it exposes a public-facing role
3. Delete the Lex bot *(optional — an idle bot costs nothing)*
4. Delete the Lambda function *(optional — idle Lambda costs nothing)*
5. Delete the `LexRole` and `Cognito_LexLabUnauthRole` IAM roles if finished

If you want to keep the demo working for later, the minimum safe step is
**re-enable Block Public Access** on the bucket between demonstrations.

- [ ] S3 bucket emptied and deleted (or made private again)
- [ ] Cognito identity pool deleted
- [ ] Lex requests used: ~50 ≈ $0.04
- [ ] **Nothing in this lab bills hourly — there is no instance to stop**

---

**Next:** [Lab 6 — Amazon Lex chatbot](Lab-6-Lex-Chatbot.md)

---

*Adapted from the AWS Academy Machine Learning Foundations lab for use outside
the Vocareum sandbox. Original lab content © Amazon Web Services, Inc.*
