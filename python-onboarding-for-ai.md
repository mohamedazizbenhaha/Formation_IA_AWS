# Python Onboarding: From A to Z — Foundations for AI

### A complete, hands-on course to get you from zero to "AI-ready" Python

This course covers everything you need in Python **before** jumping into machine learning libraries (NumPy, pandas, scikit-learn, PyTorch). Every section follows the same pattern:

**Explanation → Mini Exercise → Correction**

Type the code yourself as you go — don't just read it. Muscle memory matters more than you think.

---

## Table of Contents

1. Setting Up & Running Python
2. Variables & Data Types
3. Operators
4. Strings in Depth
5. Control Flow (if/else)
6. Loops (for/while)
7. Lists
8. Tuples & Sets
9. Dictionaries
10. Functions
11. Error Handling (try/except)
12. File I/O
13. Modules, Packages & pip
14. Object-Oriented Programming (OOP)
15. Comprehensions
16. NumPy Basics (your first AI-adjacent library)
17. pandas Basics (working with tabular data)
18. Putting It All Together — Mini Project
19. Where to Go Next

---

## 1. Setting Up & Running Python

### Explanation

You need Python installed (version 3.10 recommended). Check with:

```bash
python3 --version
```

You can run Python three ways:
- **Interactive shell** (type `python3` in a terminal, run one line at a time)
- **Script file** (write code in a `.py` file, run with `python3 file.py`)
- **Notebooks** (Jupyter/Colab — very common in AI work, mix code + text + charts in one document)

For this course, assume you're writing `.py` files and running them from a terminal.

**Virtual environments** matter early: they isolate your project's packages from your system's Python, avoiding version conflicts.

```bash
python3 -m venv myenv
source myenv/bin/activate      # macOS/Linux
myenv\Scripts\activate         # Windows
pip install numpy pandas
```

### Mini Exercise
Open a terminal and print your Python version. Then create a file called `hello.py` that prints `"Hello, AI world!"`.

### Correction
```python
# hello.py
print("Hello, AI world!")
```
Run it with: `python3 hello.py`

---

## 2. Variables & Data Types

### Explanation

A variable is a named box that stores a value. Python figures out the type automatically (this is called **dynamic typing**).

```python
age = 25            # int (whole number)
price = 19.99        # float (decimal number)
name = "Sarah"        # str (text)
is_student = True    # bool (True/False)
nothing = None        # NoneType (absence of a value)
```

Check a variable's type anytime:
```python
print(type(age))     # <class 'int'>
```

Convert between types (**casting**):
```python
str(25)      # "25"
int("25")    # 25
float("3.14") # 3.14
```

**Why this matters for AI:** every dataset you load will be a mix of these basic types — numbers, text labels, booleans (True/False flags), and missing values (`None`/`NaN`). Confusing a string `"5"` with an integer `5` is one of the most common bugs beginners hit.

### Mini Exercise
Create variables for a fictional AI model: `model_name` (string), `accuracy` (float), `num_layers` (int), `is_trained` (bool). Print all four with a descriptive sentence for each.

### Correction
```python
model_name = "ResNet-Lite"
accuracy = 0.943
num_layers = 12
is_trained = True

print(f"Model name: {model_name}")
print(f"Accuracy: {accuracy}")
print(f"Number of layers: {num_layers}")
print(f"Is trained: {is_trained}")
```
> Note the `f"..."` syntax — an **f-string**, the modern way to embed variables inside text.

---

## 3. Operators

### Explanation

**Arithmetic:** `+  -  *  /  //  %  **`
```python
7 / 2    # 3.5   (true division)
7 // 2   # 3     (floor division, drops remainder)
7 % 2    # 1     (modulo — the remainder)
2 ** 3   # 8     (power)
```

**Comparison:** `==  !=  >  <  >=  <=` → always return a `bool`

**Logical:** `and  or  not`
```python
x = 5
print(x > 0 and x < 10)   # True
```

**Assignment shortcuts:** `+=  -=  *=  /=`
```python
score = 10
score += 5   # same as score = score + 5
```

### Mini Exercise
A model was trained for `epochs = 37`. Check whether the number of epochs is even, and print `True`/`False`. Also compute how many full "batches of 10" fit into 37 epochs, and the remainder.

### Correction
```python
epochs = 37
is_even = epochs % 2 == 0
full_batches = epochs // 10
remainder = epochs % 10

print(f"Is even: {is_even}")
print(f"Full batches of 10: {full_batches}, remainder: {remainder}")
```

---

## 4. Strings in Depth

### Explanation

Strings are sequences of characters — you'll manipulate them constantly (cleaning text data, labels, file names).

```python
s = "Machine Learning"
s.lower()          # "machine learning"
s.upper()          # "MACHINE LEARNING"
s.split(" ")       # ["Machine", "Learning"]
s.replace("Machine", "Deep")  # "Deep Learning"
len(s)             # 17
s[0]               # "M"   (indexing — starts at 0)
s[0:7]             # "Machine" (slicing)
s.strip()          # removes leading/trailing whitespace
"  ".join(["a","b","c"])  # "a  b  c"
```

f-strings for formatting:
```python
name = "Sarah"
acc = 0.9432
print(f"{name} scored {acc:.2%}")   # Sarah scored 94.32%
```

### Mini Exercise
Given the sentence `"the quick brown fox"`, capitalize each word and count how many words it contains.

### Correction
```python
sentence = "the quick brown fox"
words = sentence.split(" ")
capitalized = " ".join(word.capitalize() for word in words)
print(capitalized)          # The Quick Brown Fox
print(len(words))           # 4
```

---

## 5. Control Flow (if / else)

### Explanation

Control flow lets your program make decisions.

```python
accuracy = 0.85

if accuracy >= 0.9:
    print("Excellent model")
elif accuracy >= 0.7:
    print("Decent model, needs tuning")
else:
    print("Model needs rework")
```

Python uses **indentation** (spaces) instead of curly braces to define blocks — this is not optional, it's part of the syntax.

### Mini Exercise
Write a function-free script that checks a variable `temperature` (in Celsius): print `"Freezing"` if ≤ 0, `"Cold"` if between 1 and 15, `"Mild"` if between 16 and 25, `"Hot"` if above 25.

### Correction
```python
temperature = 18

if temperature <= 0:
    print("Freezing")
elif temperature <= 15:
    print("Cold")
elif temperature <= 25:
    print("Mild")
else:
    print("Hot")
```

---

## 6. Loops (for / while)

### Explanation

**`for` loop** — iterate over a known sequence:
```python
for i in range(5):        # 0,1,2,3,4
    print(i)

fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
```

**`while` loop** — repeat until a condition becomes false:
```python
count = 0
while count < 3:
    print(count)
    count += 1
```

**`break`** exits a loop early. **`continue`** skips to the next iteration.

**Why this matters for AI:** training a model is literally a loop — repeat "predict, measure error, adjust" thousands of times. Understanding loops deeply is non-negotiable.

### Mini Exercise
Simulate a tiny "training loop": for 5 epochs, print the epoch number and a fake loss value that decreases each time (e.g., start at 1.0, subtract 0.15 each epoch).

### Correction
```python
loss = 1.0
for epoch in range(1, 6):
    print(f"Epoch {epoch}: loss = {loss:.2f}")
    loss -= 0.15
```

---

## 7. Lists

### Explanation

A list is an ordered, changeable collection — the workhorse data structure in Python.

```python
scores = [0.91, 0.85, 0.76, 0.99]

scores.append(0.60)       # add to the end
scores[0]                 # 0.91 (access by index)
scores[-1]                # last element
scores[1:3]               # slice: [0.85, 0.76]
len(scores)                # 5
sorted(scores)             # new sorted list (ascending)
scores.sort(reverse=True)  # sorts in place, descending
sum(scores) / len(scores)  # average
max(scores), min(scores)
```

Lists can hold mixed types, and even other lists (nested lists — used for matrices/grids).

```python
matrix = [[1, 2], [3, 4]]
matrix[0][1]   # 2
```

### Mini Exercise
Given `scores = [88, 92, 79, 65, 90, 100]`, compute the average, the highest, the lowest, and a new list containing only scores ≥ 85.

### Correction
```python
scores = [88, 92, 79, 65, 90, 100]

average = sum(scores) / len(scores)
highest = max(scores)
lowest = min(scores)
passing = [s for s in scores if s >= 85]

print(f"Average: {average:.2f}")
print(f"Highest: {highest}")
print(f"Lowest: {lowest}")
print(f"Scores >= 85: {passing}")
```
> `[s for s in scores if s >= 85]` is a **list comprehension** — we'll cover it properly in section 15, but it's worth seeing early.

---

## 8. Tuples & Sets

### Explanation

**Tuple** — like a list, but **immutable** (can't be changed after creation). Useful for fixed data like coordinates or (input, label) pairs.

```python
point = (3, 4)
x, y = point   # unpacking
```

**Set** — an unordered collection of **unique** values. Great for removing duplicates or checking membership fast.

```python
labels = ["cat", "dog", "cat", "bird", "dog"]
unique_labels = set(labels)     # {"cat", "dog", "bird"}
"cat" in unique_labels          # True (fast lookup)
```

### Mini Exercise
You have a list of predicted labels with duplicates: `["spam","ham","spam","spam","ham"]`. Find the unique labels and count how many unique classes there are.

### Correction
```python
predicted = ["spam", "ham", "spam", "spam", "ham"]
unique_classes = set(predicted)
print(unique_classes)          # {'spam', 'ham'}
print(len(unique_classes))     # 2
```

---

## 9. Dictionaries

### Explanation

A dictionary stores **key → value** pairs. Extremely common in AI for configs, labeled data, and JSON-like structures.

```python
model_config = {
    "name": "MiniNet",
    "layers": 8,
    "learning_rate": 0.001,
    "trained": False
}

model_config["layers"]          # 8
model_config["trained"] = True   # update a value
model_config["dropout"] = 0.2   # add a new key
model_config.keys()             # all keys
model_config.values()           # all values
model_config.items()            # key-value pairs

for key, value in model_config.items():
    print(key, "->", value)
```

Check safely if a key exists:
```python
model_config.get("batch_size", "not set")   # returns "not set" if missing
```

### Mini Exercise
Build a dictionary representing a dataset sample: `{"text": "I love this movie", "label": "positive", "confidence": 0.97}`. Print a formatted sentence using all three values, then add a new key `"length"` equal to the number of words in `"text"`.

### Correction
```python
sample = {"text": "I love this movie", "label": "positive", "confidence": 0.97}

print(f"Text: '{sample['text']}' -> {sample['label']} ({sample['confidence']:.0%})")

sample["length"] = len(sample["text"].split())
print(sample)
```

---

## 10. Functions

### Explanation

Functions package reusable logic. Almost everything in AI code (data loading, preprocessing, training, evaluation) is organized into functions.

```python
def greet(name):
    return f"Hello, {name}!"

print(greet("Sarah"))
```

**Default arguments:**
```python
def train_model(epochs=10, learning_rate=0.01):
    print(f"Training for {epochs} epochs at rate {learning_rate}")

train_model()                     # uses defaults
train_model(epochs=20)            # override one
```

**Multiple return values:**
```python
def stats(numbers):
    return min(numbers), max(numbers), sum(numbers)/len(numbers)

low, high, avg = stats([1,2,3,4,5])
```

**`*args` and `**kwargs`** (variable numbers of arguments — you'll see this constantly in AI library code):
```python
def log_metrics(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

log_metrics(accuracy=0.9, loss=0.2)
```

**Lambda (anonymous one-line functions):**
```python
square = lambda x: x ** 2
square(5)   # 25
```

### Mini Exercise
Write a function `normalize(value, min_val, max_val)` that scales `value` into a 0–1 range using the formula `(value - min_val) / (max_val - min_val)`. Test it with `normalize(50, 0, 100)`.

### Correction
```python
def normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val)

print(normalize(50, 0, 100))   # 0.5
print(normalize(75, 0, 100))   # 0.75
```
> This exact formula (**min-max scaling**) is one of the first things you'll do to real datasets before feeding them to a model.

---

## 11. Error Handling (try / except)

### Explanation

Real-world data is messy — files go missing, values are the wrong type, division by zero happens. `try/except` prevents your program from crashing.

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Can't divide by zero!")

try:
    value = int("not a number")
except ValueError as e:
    print(f"Conversion failed: {e}")
finally:
    print("This always runs, error or not")
```

You can catch multiple specific error types, or a generic `Exception` as a catch-all (use sparingly — specific is better than generic).

### Mini Exercise
Write a function `safe_divide(a, b)` that returns the division result, but returns `None` and prints a friendly message if dividing by zero.

### Correction
```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Division by zero avoided.")
        return None

print(safe_divide(10, 2))   # 5.0
print(safe_divide(10, 0))   # None + message
```

---

## 12. File I/O

### Explanation

AI work constantly involves reading datasets from files and saving results.

```python
# Writing
with open("data.txt", "w") as f:
    f.write("line one\n")
    f.write("line two\n")

# Reading
with open("data.txt", "r") as f:
    content = f.read()          # whole file as one string
    
with open("data.txt", "r") as f:
    for line in f:               # read line by line
        print(line.strip())
```

The `with` statement automatically closes the file for you, even if an error occurs — always prefer it over manually calling `open()`/`close()`.

For structured data, **JSON** is everywhere in AI (configs, API responses, labeled datasets):
```python
import json

data = {"name": "model1", "accuracy": 0.92}

with open("result.json", "w") as f:
    json.dump(data, f)

with open("result.json", "r") as f:
    loaded = json.load(f)
```

### Mini Exercise
Write a dictionary of 3 fake experiment results to a JSON file, then read it back and print the experiment with the highest accuracy.

### Correction
```python
import json

experiments = {
    "exp1": {"accuracy": 0.85},
    "exp2": {"accuracy": 0.93},
    "exp3": {"accuracy": 0.78}
}

with open("experiments.json", "w") as f:
    json.dump(experiments, f)

with open("experiments.json", "r") as f:
    loaded = json.load(f)

best = max(loaded, key=lambda k: loaded[k]["accuracy"])
print(f"Best experiment: {best} with accuracy {loaded[best]['accuracy']}")
```

---

## 13. Modules, Packages & pip

### Explanation

Python's power comes from its ecosystem. A **module** is a `.py` file with reusable code; a **package** is a folder of modules; `pip` installs packages from PyPI.

```bash
pip install numpy pandas scikit-learn matplotlib
```

```python
import math
math.sqrt(16)          # 4.0

import numpy as np      # common alias convention
from math import pi     # import just one name
from collections import Counter
```

`Counter` is a handy tool worth knowing early:
```python
from collections import Counter
labels = ["cat","dog","cat","cat","bird"]
Counter(labels)   # Counter({'cat': 3, 'dog': 1, 'bird': 1})
```

### Mini Exercise
Use `Counter` to find the most common word in the sentence `"the cat sat on the mat the cat ran"`.

### Correction
```python
from collections import Counter

sentence = "the cat sat on the mat the cat ran"
words = sentence.split()
counts = Counter(words)
print(counts.most_common(1))    # [('the', 3)]
```

---

## 14. Object-Oriented Programming (OOP)

### Explanation

Classes bundle data (**attributes**) and behavior (**methods**) together. Almost every AI library (models, layers, datasets) is built as classes — you don't need to master OOP deeply, but you must read it comfortably.

```python
class Model:
    def __init__(self, name, accuracy):
        self.name = name              # attribute
        self.accuracy = accuracy

    def summary(self):                 # method
        return f"{self.name}: {self.accuracy:.0%} accuracy"

    def is_good(self):
        return self.accuracy >= 0.9

m = Model("ResNet-Lite", 0.94)
print(m.summary())
print(m.is_good())
```

**Inheritance** — a class can build on another:
```python
class VisionModel(Model):
    def __init__(self, name, accuracy, image_size):
        super().__init__(name, accuracy)   # reuse parent's init
        self.image_size = image_size

v = VisionModel("ImageNet-Small", 0.88, 224)
print(v.summary())        # inherited method works
print(v.image_size)
```

This pattern (`class X(nn.Module)` in PyTorch, for example) is exactly how you'll define custom neural networks later.

### Mini Exercise
Create a class `Dataset` with attributes `name` and `size` (number of samples), and a method `describe()` that returns a formatted sentence. Create two instances and print their descriptions.

### Correction
```python
class Dataset:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def describe(self):
        return f"Dataset '{self.name}' contains {self.size} samples."

train = Dataset("Training Set", 10000)
test = Dataset("Test Set", 2000)

print(train.describe())
print(test.describe())
```

---

## 15. Comprehensions

### Explanation

A compact, Pythonic way to build lists, dicts, or sets from existing sequences — you'll see this style constantly in real AI codebases.

```python
# List comprehension
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]

# Dict comprehension
lengths = {word: len(word) for word in ["cat", "elephant", "dog"]}

# Set comprehension
unique_lengths = {len(word) for word in ["cat", "dog", "bird"]}
```

Rule of thumb: if you can say it in one clear sentence ("give me x squared for every x in range"), a comprehension probably fits. If the logic needs multiple steps or is hard to read on one line, use a regular loop instead — readability wins.

### Mini Exercise
Given `words = ["AI", "machine", "learning", "GPU", "data"]`, build a list of only the words with more than 3 letters, converted to uppercase.

### Correction
```python
words = ["AI", "machine", "learning", "GPU", "data"]
result = [w.upper() for w in words if len(w) > 3]
print(result)    # ['MACHINE', 'LEARNING', 'DATA']
```

---

## 16. NumPy Basics (your first AI-adjacent library)

### Explanation

NumPy provides **arrays** — like lists, but much faster and built for math operations on entire collections at once (this is what every AI framework is built on top of).

```python
import numpy as np

a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

a + b            # array([11, 22, 33, 44])  — element-wise, no loop needed!
a * 2            # array([2, 4, 6, 8])
a.mean()         # 2.5
a.sum()          # 10
a.max()          # 4

# 2D arrays (matrices) — the core structure behind neural networks
matrix = np.array([[1, 2], [3, 4]])
matrix.shape     # (2, 2)
matrix.T         # transpose

np.zeros((3,3))  # 3x3 matrix of zeros
np.random.rand(3) # 3 random numbers between 0 and 1
```

**Why this matters:** in traditional Python, adding two lists element-by-element requires a loop. NumPy does it instantly across millions of numbers — this speed is why it underlies nearly all of AI computing.

### Mini Exercise
Create a NumPy array of the numbers 1 to 10. Compute its mean, its standard deviation, and a new array where every value is squared.

### Correction
```python
import numpy as np

arr = np.array(range(1, 11))
print(arr.mean())     # 5.5
print(arr.std())      # ~2.87
print(arr ** 2)        # [1, 4, 9, ..., 100]
```

---

## 17. pandas Basics (working with tabular data)

### Explanation

pandas is built on NumPy and gives you **DataFrames** — spreadsheet-like tables, the standard way to load and explore real datasets.

```python
import pandas as pd

data = {
    "name": ["Alice", "Bob", "Carla"],
    "score": [88, 92, 79],
    "passed": [True, True, False]
}

df = pd.DataFrame(data)

df.head()              # first rows
df["score"]             # a single column
df[df["score"] > 80]   # filter rows
df["score"].mean()      # 86.33
df.describe()            # quick statistical summary
df.sort_values("score", ascending=False)

# Reading real files
df = pd.read_csv("dataset.csv")
```

### Mini Exercise
Create a DataFrame with columns `city` and `temperature` for 4 cities of your choice. Filter to show only cities with temperature above 20, and compute the average temperature.

### Correction
```python
import pandas as pd

data = {
    "city": ["Tunis", "Paris", "Cairo", "Oslo"],
    "temperature": [28, 15, 33, 8]
}
df = pd.DataFrame(data)

warm_cities = df[df["temperature"] > 20]
print(warm_cities)

print(df["temperature"].mean())   # 21.0
```

---

## 18. Putting It All Together — Mini Project

### Explanation

Let's combine everything: functions, dictionaries, error handling, NumPy, and pandas, in one small realistic script that mimics an early step of an AI workflow — loading, cleaning, and summarizing a dataset.

### Exercise
Given this raw data (some values are messy/missing), write a script that:
1. Builds a DataFrame from it
2. Removes rows with missing scores
3. Adds a `passed` column (`True` if score ≥ 60)
4. Prints the pass rate and average score

```python
raw_data = {
    "student": ["Ali", "Sara", "Omar", "Lina", "Yassine"],
    "score": [72, None, 55, 91, 60]
}
```

### Correction
```python
import pandas as pd

raw_data = {
    "student": ["Ali", "Sara", "Omar", "Lina", "Yassine"],
    "score": [72, None, 55, 91, 60]
}

df = pd.DataFrame(raw_data)
df = df.dropna(subset=["score"])          # remove missing scores
df["passed"] = df["score"] >= 60

pass_rate = df["passed"].mean()           # mean of booleans = proportion True
average_score = df["score"].mean()

print(df)
print(f"\nPass rate: {pass_rate:.0%}")
print(f"Average score: {average_score:.1f}")
```

This exact pattern — **load → clean → transform → summarize** — is the backbone of nearly every real-world AI project's first step, before any model gets trained.

---

## 19. Where to Go Next

You now have the Python foundation needed to start real AI/ML work. Suggested path:

1. **scikit-learn** — train your first real machine learning models (classification, regression) with just a few lines of code.
2. **matplotlib / seaborn** — visualize your data (essential before modeling anything).
3. **Basic statistics & linear algebra refresher** — means, distributions, vectors, matrix multiplication (you already touched the practical side with NumPy).
4. **PyTorch or TensorFlow** — once comfortable with the above, move into building actual neural networks.
5. **Practice on real datasets** — sites like Kaggle offer beginner-friendly datasets and mini-competitions to apply everything above.

### Quick self-check before moving on
You should be able to, without looking anything up:
- Write a function with default arguments and a return value
- Loop through a list and a dictionary
- Handle a potential error with try/except
- Load a CSV into a pandas DataFrame and filter it
- Explain the difference between a list, a tuple, a set, and a dictionary

If any of these feel shaky, revisit that section and redo the exercise from scratch (without peeking at the correction first).
