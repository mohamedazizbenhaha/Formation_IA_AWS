# Lab 5 — Guided Lab: Facial Recognition
### Personal AWS account edition

> **Before this lab:** read
> [`00-START-HERE-Setup-and-Cost.md`](00-START-HERE-Setup-and-Cost.md) — it
> covers feasibility, permissions, where to run this, and cleanup.

**Duration:** ~60 minutes
**Cost:** **$0.00** on CloudShell · ~$0.05 if you use a SageMaker notebook
**Quota needed:** **none**

---

## Objectives

- Create a custom collection for Amazon Rekognition
- Add an image to a custom collection
- Detect known faces in an image
- View bounding boxes
- Delete the collection

## What changes from the official lab

| Official lab | This version | Why |
|---|---|---|
| "Open `en_us/05-facedetection.ipynb`" | **Provided** → `notebooks/05-facedetection.ipynb` | Vocareum lifecycle config does not exist on your account |
| Requires a `MyNotebook` SageMaker instance | **Optional** — CloudShell works and is free | Rekognition is a plain API; no ML runs locally |
| Face images assumed present | Notebook downloads public-domain portraits | Nothing was provided to download |
| Index and search only | Adds a **negative test** (different person) | Proves the system discriminates — the original never checks |
| Fixed threshold | Adds a **threshold sweep table** | Makes the false-positive/false-negative trade-off concrete |
| No ethics discussion | Adds responsible-use section + questions | Facial recognition is not a neutral technology |

---

## Before you start: responsible use

This deserves five minutes of class time, not a footnote.

- **Consent.** Faces are biometric data. Under GDPR (EU), BIPA (Illinois) and
  similar laws, collecting or processing them without explicit informed
  consent can be unlawful.
- **Accuracy is not uniform.** NIST's Face Recognition Vendor Test has
  repeatedly found error rates vary substantially by sex and skin tone. A
  single headline accuracy figure conceals this.
- **Errors have consequences.** A false match in policing or access control
  affects a real person.

**This lab uses public-domain official portraits of public figures** — US
federal government works — not photos of students. If a student prefers to use
their own photo, that is their own face and their own consent. **Nobody should
upload photographs of other people without asking them.**

---

## Task 1 — Choose where to run it

| Option | Cost | Best for |
|---|---|---|
| **AWS CloudShell** | **$0** | Running it yourself; no setup |
| Your laptop | $0 | If you already have Python + AWS CLI |
| **SageMaker notebook** `ml.t3.medium` | ~$0.05/hr | Teaching — students see JupyterLab |

### Option A — CloudShell (recommended for a solo run)

1. Console → set region to **US East (N. Virginia)**
2. Click the **CloudShell** icon (`>_`) in the top nav bar
3. Wait ~20 seconds for the shell
4. Install dependencies:

```bash
pip install --quiet boto3 pillow matplotlib requests pandas
```

5. **Actions → Upload file** → upload `05-facedetection.ipynb`
6. CloudShell has no notebook UI, so either convert it:

```bash
pip install --quiet nbconvert jupyter && jupyter nbconvert --to script 05-facedetection.ipynb && python 05-facedetection.py
```

   or open the `.ipynb` and paste cells into `python3` one at a time.

> CloudShell storage (1 GB in your home directory) persists between sessions,
> but the environment resets after ~20 minutes idle. Re-run the `pip install`
> if that happens.

### Option B — SageMaker notebook instance (for teaching)

Follow section 5 of the setup guide, then:

1. **SageMaker AI → Notebooks → Create notebook instance**
2. Name `MyNotebook`, type **`ml.t3.medium`**, lifecycle config **None**
3. IAM role: reuse your existing SageMaker execution role, or create one
4. Wait for `InService`, choose **Open JupyterLab**
5. Upload `05-facedetection.ipynb` with the **↑** button
6. **Attach Rekognition permissions to the execution role** — see Task 2

> ⏰ **Billing starts at `InService`.** Stop the instance when you finish.

---

## Task 2 — Grant Rekognition permissions

Whatever identity runs the notebook needs `AmazonRekognitionFullAccess`.

**On a SageMaker notebook:**

1. SageMaker AI → Notebooks → click `MyNotebook`
2. Under **Permissions and encryption**, click the **IAM role ARN** — it opens
   in the IAM console
3. **Add permissions → Attach policies**
4. Search `AmazonRekognitionFullAccess`, tick it, **Add permissions**

**On CloudShell or a laptop:** your IAM user needs the same policy. If you are
the account owner, you already have it.

> The notebook's Step 2 verifies credentials with `sts:GetCallerIdentity` and
> prints a clear message if this is wrong — far better than a confusing
> failure five cells later.

---

## Task 3 — Open and run the notebook

Open **`05-facedetection.ipynb`**, kernel **`conda_python3`**, and work top to
bottom with `SHIFT + ENTER`.

### What each step does

| Step | What happens | Watch for |
|---|---|---|
| 1 | Install/import `boto3`, `Pillow`, `matplotlib` | — |
| 2 | Connect to Rekognition; **verify credentials** | Prints your account ID |
| 3 | Download three public-domain portraits | Two of person A, one of person B |
| 4 | `detect_faces` + draw bounding box | Ratio → pixel conversion |
| 5 | `create_collection` | Server-side store of face **vectors** |
| 6 | `index_faces` with `ExternalImageId` | The label you get back on a match |
| 7 | `list_faces` | Confirms what is stored |
| 8 | `search_faces_by_image` — **should match** | Different photo, same person |
| 9 | Negative test — **should not match** | Different person |
| 9b | Threshold sweep table | The core trade-off |
| 10 | `delete_collection` | Data hygiene |

---

## The three ideas worth teaching

### 1. Bounding boxes are ratios, not pixels

This trips up everyone the first time. Rekognition returns:

```python
{'Left': 0.31, 'Top': 0.14, 'Width': 0.38, 'Height': 0.42}
```

Those are **fractions of the image dimensions (0–1)**, so the same numbers stay
valid at any resolution. To draw the box:

```python
left   = box['Left']   * image_width
top    = box['Top']    * image_height
width  = box['Width']  * image_width
height = box['Height'] * image_height
```

Forget the multiplication and your rectangle collapses into the top-left
corner — a very common first bug.

### 2. A collection stores vectors, not images

`index_faces` does **not** store your photograph. It stores a mathematical
feature vector. You cannot retrieve the original image from a collection.

**But that does not make it exempt from data-protection law.** A face vector
still identifies a person, so it is still biometric data. "We don't store the
photo" is not a compliance argument.

### 3. `FaceMatchThreshold` is the same trade-off as Lab 3.6

| Threshold | Effect |
|---|---|
| **Low** (70) | More matches — more **false positives** (wrong person accepted) |
| **High** (95) | Fewer matches — more **false negatives** (right person rejected) |

Exactly the precision/recall tension from the classification threshold in
Module 3, in a different costume. The notebook's sweep table shows the window
where the same person still matches and the different person does not.

**There is no universally correct value.** It depends entirely on the cost of
each error — a business and ethical decision, not a technical one.

---

## Discussion questions

1. Your two-person test worked perfectly. Why is that **not** evidence the
   system is accurate? *(Sample of two; no demographic breakdown; ideal
   lighting; posed studio portraits; one pose each.)*
2. You are building door access for an office. Threshold 70 or 99? What goes
   wrong with each? *(70: strangers get in. 99: staff get locked out in poor
   lighting or with a new haircut.)*
3. NIST has found error rates differ across demographic groups. What would you
   measure before deploying, and what would you do if accuracy differed by
   group?
4. The collection stores vectors, not images. Does that exempt it from
   data-protection law? *(No.)*
5. Rekognition reports estimated emotions. How much should you trust "this
   person is happy"? *(It reports resemblance to training-data patterns
   labelled 'happy'. Mapping expression to felt emotion is scientifically
   contested.)*

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `UnrecognizedClientException` / `InvalidSignature` | No or bad credentials | CloudShell: already set. Laptop: `aws configure`. SageMaker: check the role |
| `AccessDeniedException` on any call | Missing Rekognition policy | Attach `AmazonRekognitionFullAccess` (Task 2) |
| `ResourceAlreadyExistsException` | Collection left from a previous run | The notebook deletes it first — re-run that cell |
| `InvalidParameterException: no faces in image` | Face too small, blurred, or turned away | Use a clear, front-facing portrait |
| `ExternalImageId` rejected | Contains a space or symbol | Letters, digits, `_ . : -` only |
| Image downloads fail | No internet, or Wikimedia blocked | Upload your own photos — see the notebook's alternative cell |
| Bounding box in the corner | Forgot to multiply by width/height | See idea #1 above |
| `ValidationException` on `search_faces_by_image` | Image has no detectable face | Check the file actually contains a face |

---

## Before you leave

- [ ] Collection deleted (the notebook's last step does this)
- [ ] `list_collections` returns empty
- [ ] **If you used a SageMaker notebook instance: STOP IT**
      (SageMaker AI → Notebooks → select → Actions → Stop)
- [ ] Rekognition calls used: ~15 of your 1,000/month free allowance

---

*This lab is self-contained. Setup, permissions, cost and cleanup are in
[`00-START-HERE-Setup-and-Cost.md`](00-START-HERE-Setup-and-Cost.md).*
