# Lab 6 — Guided Lab: Amazon Lex chatbot
### Personal AWS account edition

> **Before this lab:** read
> [`00-START-HERE-Setup-and-Cost.md`](00-START-HERE-Setup-and-Cost.md) — it
> covers feasibility, the two resources the official lab assumes exist, the
> security considerations, and cleanup.

**Duration:** ~90 minutes (the official lab says 60; allow more for the two
resources you must create yourself)
**Cost:** ~**$0.04** total
**Quota needed:** **none**

---

## Objectives

- Create and configure a bot with Amazon Lex V2
- Create a Lambda function and wire it to the bot
- Host a chat webpage on Amazon S3
- Interact with the bot from that webpage

## What changes from the official lab

| Official lab | This version | Why |
|---|---|---|
| "Under Existing role select **LexRole**" | **Task 2a creates it** | The role does not exist on your account |
| "Choose **MyIdentityPool**" | **Task 5 creates it** | The pool does not exist on your account |
| "Download the following two webpage files" | **Provided** → `lab6-assets/` | The download link is Vocareum-hosted |
| Lambda code pasted from the lab page | **Rewritten and tested** → `lab6-assets/lambda_function.py` | Verified against 13 synthetic Lex V2 events |
| Availability via `random.randint()` | **Deterministic by date** | Random availability makes a class demo unreproducible |
| Bucket policy includes a `lexv2.amazonaws.com` statement | **Removed** | Lex never reads your bucket; it was never needed |
| — | Adds a config-validation guard to `index.html` | Tells you exactly which value you forgot |

> **The two missing resources are the real trap.** The official lab reads as
> though `LexRole` and `MyIdentityPool` already exist. On your account they do
> not, and the lab never explains how to create them. Tasks 2a and 5 below do.

---

## Architecture

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
cannot safely hold any. Cognito issues short-lived, tightly-scoped
*unauthenticated* credentials to anonymous visitors so the page can call Lex
without you ever embedding a secret.

---

## Task 1 — Create the bot

1. Console → search **Amazon Lex** → open it.
   **Confirm you are in the V2 console** — the left nav should show **Bots**.
2. **Create bot**
3. **Creation method:** *Traditional* → select **Start with an example**
4. **Example bots:** `MakeAppointment`
5. **Bot name:** `ScheduleAppointment`
6. **IAM permissions:** *Create a role with basic Amazon Lex permissions*
   *(this one Lex does create for you — unlike `LexRole` in Task 2)*
7. **COPPA:** **No**
8. **Next**
9. **Language:** *English (US)* → **Done**

You land on the `MakeAppointment` intent page.

10. Scroll to **Code hooks - optional**
11. Tick **Use a Lambda function for initialization and validation**
12. **Save intent**

> Without step 11 the bot works but never calls your Lambda — no validation,
> no availability checking. This is the easiest step to miss.

**Record your Bot ID now.** Left nav → **Bots** → `ScheduleAppointment`. The
**Bot ID** is a 10-character string like `ABCDEFGHIJ`. You need it in Task 7.

---

## Task 2a — Create `LexRole` ← not in the official lab

The official lab says to select an existing role called `LexRole`. It does not
exist on your account. Create it:

1. Console → **IAM → Roles → Create role**
2. **Trusted entity type:** *AWS service*
3. **Use case:** **Lambda** → **Next**
4. **Permissions:** search and tick **`AWSLambdaBasicExecutionRole`**
   *(this grants CloudWatch Logs access — essential for debugging)*
5. **Next**
6. **Role name:** `LexRole`
7. **Create role**

That is all it needs. The Lambda only validates data and returns JSON — it
calls no other AWS service. Logging permission is the only requirement.

> Trust policy for reference: [`lab6-assets/lexrole-trust-policy.json`](lab6-assets/lexrole-trust-policy.json)
> (the console builds this for you when you pick *Lambda* as the use case).

---

## Task 2b — Create the Lambda function

1. Console → **Lambda → Create function**
2. Select **Author from scratch**
   *(the official lab uses the "Make an appointment with Lex" blueprint; that
   blueprint targets **Lex V1** and its response format will not work with a
   V2 bot. Authoring from scratch with the provided code avoids that mismatch.)*
3. **Function name:** `MakeAppointmentCodeHook`
4. **Runtime:** **Python 3.12**
5. **Change default execution role → Use an existing role → `LexRole`**
6. **Create function**

### Paste the code

1. In the **Code source** editor, open `lambda_function.py`
2. Select all existing code and delete it
3. Paste the entire contents of
   [`lab6-assets/lambda_function.py`](lab6-assets/lambda_function.py)
4. **Deploy**

Wait for *"Changes deployed"*.

### Give Lex permission to invoke it

Lex must be allowed to call your function:

1. In the Lambda console, **Configuration → Permissions**
2. Scroll to **Resource-based policy statements → Add permissions**
3. **AWS service** → **Other**
4. **Statement ID:** `lex-invoke`
5. **Principal:** `lexv2.amazonaws.com`
6. **Action:** `lambda:InvokeFunction`
7. **Save**

> In many cases attaching the Lambda via the Lex console (Task 3) adds this
> automatically. Adding it explicitly is harmless and avoids a confusing
> `AccessDeniedException` in the Lex test window.

### Quick sanity test

**Test** tab → create an event named `dialog` with:

```json
{
  "invocationSource": "DialogCodeHook",
  "inputTranscript": "test",
  "sessionState": {
    "sessionAttributes": {},
    "intent": {
      "name": "MakeAppointment",
      "state": "InProgress",
      "confirmationState": "None",
      "slots": {
        "AppointmentType": {"value": {"interpretedValue": "facelift"}},
        "Date": null,
        "Time": null
      }
    }
  }
}
```

**Test**. You should get back an `ElicitSlot` action for `AppointmentType`
with the message *"I can book a cleaning, a root canal, or a whitening…"*.

If that works, your Lambda is correct and any later problem is wiring.

---

## Task 3 — Attach the Lambda to the bot alias

1. **Lex → Bots → `ScheduleAppointment`**
2. Left nav → **Aliases** → **`TestBotAlias`**
3. Under **Languages**, choose **English (US)**
4. Expand **Lambda function - optional**
   - **Source:** `MakeAppointmentCodeHook`
   - **Lambda function version or alias:** `$LATEST`
5. **Save**

> This is per-alias. Attaching it to `TestBotAlias` does not affect any other
> alias you create later.

**Record the Alias ID.** On the Aliases list, `TestBotAlias` shows an
**Alias ID** — usually `TSTALIASID`. You need it in Task 7.

---

## Task 4 — Build and test in the console

1. Left nav → **Intents** → **Build** (takes 1–2 minutes)
2. When it completes → **Test**

Try this conversation:

| You | Expected |
|---|---|
| `I would like to make an appointment` | *What type of appointment…* |
| `A root canal` | *What day…* |
| `tomorrow` | *We have 10:00 a.m., 11:30 a.m. or 1:00 p.m. available…* |
| `10:00` | *…confirm?* |
| `yes` | *Booked. Your root canal is on …* |

**Proof the Lambda is running:** the bot offers **specific times**. Those come
from your code, not from Lex. If it never mentions times, the Lambda is not
wired up — recheck Task 1 step 11 and Task 3.

### Things worth demonstrating

| Say | Shows |
|---|---|
| `a facelift` | Rejects unknown appointment types |
| `yesterday` | Rejects dates in the past |
| a Sunday | Closed-day rule |
| `7:00` | Opening-hours rule |
| `10:17` | Half-hour-increment rule |
| `a root canal` then a half-hour-only slot | Duration logic — 60-min bookings need two consecutive slots |

That last one is the nicest: a root canal needs a 60-minute window, so it is
offered **fewer** times than a cleaning on the same day.

---

## Task 5 — Create the Cognito identity pool ← not in the official lab

The official lab says to choose `MyIdentityPool`. It does not exist. Create it:

1. Console → **Cognito**
2. Left nav → **Identity pools** → **Create identity pool**
3. **User access:** **Guest access** *(unauthenticated — the webpage has no
   sign-in)*
4. **Next**
5. **IAM role:** *Create a new IAM role*, name it `Cognito_LexLabUnauthRole`
6. **Next**
7. **Identity pool name:** `MyIdentityPool`
8. **Next → Create identity pool**

**Record the Identity pool ID** — format `us-east-1:xxxxxxxx-xxxx-…`. You need
it in Task 7.

### Grant the unauthenticated role permission to call Lex

Cognito creates the role with almost no permissions. Without this step the
webpage fails with `AccessDeniedException`.

1. **IAM → Roles →** `Cognito_LexLabUnauthRole`
2. **Add permissions → Create inline policy**
3. Choose the **JSON** tab and paste the contents of
   [`lab6-assets/cognito-unauth-policy.json`](lab6-assets/cognito-unauth-policy.json):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowLexChat",
      "Effect": "Allow",
      "Action": ["lex:RecognizeText", "lex:RecognizeUtterance"],
      "Resource": "*"
    }
  ]
}
```

4. **Next**, name it `LexChatAccess`, **Create policy**

> ⚠️ **Keep this policy minimal.** Anyone who loads your webpage can assume
> this role. Two Lex actions is all it needs. Never attach
> `AmazonLexFullAccess` — that would let any visitor delete your bot.

---

## Task 6 — Create the S3 bucket and enable website hosting

> ⚠️ This makes a bucket **publicly readable**. That is required for S3 static
> website hosting. Put **only** the two HTML files in it, and delete the bucket
> when you finish.

1. Console → **S3 → Create bucket**
2. **Bucket name:** `lexlab6-` plus six random letters (must be globally unique)
3. **Uncheck** *Block all public access*
4. Tick the acknowledgement warning
5. **Create bucket**

### Upload the files

1. Open the bucket → **Upload → Add files**
2. Add `lab6-assets/index.html` and `lab6-assets/error.html`
3. **Upload** → **Close**

### Enable static website hosting

1. **Properties** tab → scroll to **Static website hosting** → **Edit**
2. **Enable**
3. **Index document:** `index.html`
4. **Error document:** `error.html`
5. **Save changes**

Scroll back down and **copy the bucket website endpoint URL** — you will use it
in Task 7.

### Attach the public-read bucket policy

1. **Permissions** tab → **Bucket policy → Edit**
2. Paste [`lab6-assets/bucket-policy.json`](lab6-assets/bucket-policy.json):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::REPLACE-WITH-YOUR-BUCKET-NAME/*"
    }
  ]
}
```

3. **Replace `REPLACE-WITH-YOUR-BUCKET-NAME` with your actual bucket name.**
   Keep the `/*` on the end — it applies the policy to the objects, not the
   bucket itself.
4. **Save changes**, accept the public-access warning

> **Deviation from the official lab:** its policy has a second statement
> granting `lexv2.amazonaws.com` read/write to your bucket. Lex never touches
> your bucket in this architecture, so that statement grants a service
> permissions it does not need. It has been removed.

---

## Task 7 — Configure and test the webpage

1. Open `lab6-assets/index.html` in a text editor
2. Find the **CONFIG** block near the bottom and fill in all four values:

```javascript
var CONFIG = {
  identityPoolId: 'us-east-1:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',  // Task 5
  botId:          'ABCDEFGHIJ',                                       // Task 1
  botAliasId:     'TSTALIASID',                                       // Task 3
  region:         'us-east-1',
  localeId:       'en_US'
};
```

| Value | Where to find it |
|---|---|
| `identityPoolId` | Cognito → Identity pools → `MyIdentityPool` |
| `botId` | Lex → Bots → `ScheduleAppointment` → Bot ID |
| `botAliasId` | Lex → your bot → Aliases → `TestBotAlias` → Alias ID |
| `region` | Must match where you built everything |

3. Save, then **re-upload `index.html`** to the bucket (S3 → Objects →
   Upload → it overwrites)
4. Open the **bucket website endpoint** from Task 6
5. Chat with your bot

> **If you forget a value**, the page tells you which one — it validates the
> config on load and displays a message instead of failing silently.

### Use the website endpoint, not the object URL

There are two different URLs and only one works properly:

| URL | Works? |
|---|---|
| `http://<bucket>.s3-website-us-east-1.amazonaws.com` | ✅ **Use this** — website endpoint |
| `https://<bucket>.s3.amazonaws.com/index.html` | ⚠️ Renders, but no index/error document routing |

The website endpoint is **HTTP only**. That is fine for this lab. A production
site would put CloudFront in front of it for HTTPS.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Page shows "Configuration incomplete" | CONFIG not filled in | Edit CONFIG, re-upload |
| `AccessDeniedException` / `NotAuthorizedException` | Unauth role lacks `lex:RecognizeText` | Task 5's inline policy |
| `ResourceNotFoundException` | Wrong `botId`/`botAliasId`/region, or bot not built | Recheck IDs; **Build** the bot |
| Bot replies but never offers times | Lambda not attached | Task 1 step 11 **and** Task 3 |
| `AccessDeniedException` in the Lex **test window** | Lex cannot invoke Lambda | Add the resource-based policy (Task 2b) |
| Lambda errors in CloudWatch | Code paste truncated | Re-paste the whole file, **Deploy** |
| 403 Forbidden on the website URL | Bucket policy missing or wrong ARN | Check `/*` and the bucket name |
| 404 on the website URL | Static website hosting not enabled | Properties → Static website hosting |
| Page loads, sending does nothing | Browser console will say | F12 → Console |
| Bot understands nothing | Bot not built after changes | **Build** again — required after every edit |

**Your first debugging stop is always CloudWatch:** Lambda → Monitor → **View
CloudWatch logs**. The function logs every event it receives.

---

## Discussion questions

1. Why does the webpage use Cognito rather than an AWS access key?
   *(A static page cannot hold a secret — anyone can read the source. Cognito
   issues short-lived, narrowly-scoped credentials instead.)*
2. The identity pool ID is visible in the page source. Is that a security
   problem? *(No — it is designed to be public. The security comes from the
   unauthenticated role's permissions, which is why scoping it matters.)*
3. What does the Lambda do that Lex cannot? *(Business rules: opening hours,
   appointment durations, availability. Lex handles language; Lambda handles
   logic.)*
4. Why does a root canal get offered fewer slots than a cleaning?
   *(60 minutes needs two consecutive free half-hour slots.)*
5. The original code invented availability with `random`. Why is deterministic
   availability better here? *(Reproducibility — you can rehearse a demo and
   debug a specific case.)*

---

## Cleanup — do this when you finish

**In priority order:**

1. **Empty and delete the S3 bucket** ← most important; it is public
   *(S3 → bucket → **Empty**, then **Delete**)*
2. **Delete the Cognito identity pool** — it exposes a public-facing role
3. Delete the Lex bot *(optional — an idle bot costs nothing)*
4. Delete the Lambda function *(optional — idle Lambda costs nothing)*
5. Delete the `LexRole` and `Cognito_LexLabUnauthRole` IAM roles if finished

If you want to keep the demo working, the minimum safe step is **re-enable
Block Public Access** on the bucket when you are not demonstrating.

- [ ] S3 bucket emptied and deleted (or made private again)
- [ ] Cognito identity pool deleted
- [ ] Lex requests used: ~50 ≈ $0.04
- [ ] Nothing in this lab bills hourly — there is no instance to stop

---

## Conclusion

You have:
- Created and configured an Amazon Lex V2 bot
- Written and deployed a Lambda code hook that enforces real business rules
- Created the two resources the official lab assumed existed
- Hosted a chat client on S3 and connected it through Cognito
- Talked to your bot from a public webpage
