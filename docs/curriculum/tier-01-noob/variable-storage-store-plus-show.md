---
title: "💚 — Variable Storage: Store + Show"
sidebar_label: "💚 Variable Storage: Store + Show"
sidebar_position: 2
---

## Task

- Create a file named variables.py.
- Make 2 variables (for example: name and age).
- Print both values in one sentence.
- Change one variable and print again.
- (Optional) Add a third variable (favorite_food, favorite_game, etc.).
- (Optional) Try BOTH string building styles: f-strings and + concatenation.

## Example run

```text
$ python variables.py
My name is Alex and I am 12 years old.
Now my name is Alex and I am 13 years old.
Bonus: My favorite game is Minecraft.
```

## Solution (ATTEMPT FIRST)

<details>
  <summary>Show spoiler code (variables.py)</summary>

This example uses f-strings (the nicest beginner way).
It also shows a second approach in comments.

```python title="variables.py"
"""variables.py

Variables = labeled boxes you can put values inside.
You can change what's in the box later.
"""

# A string (text)
name = "Alex"

# An integer (whole number)
age = 12

# f-strings let you drop variables right into text with {like_this}.
print(f"My name is {name} and I am {age} years old.")

# Let's change the value in the age box.
age = age + 1  # you can also write: age += 1
print(f"Now my name is {name} and I am {age} years old.")

# Optional: third variable (pick anything fun)
favorite_game = "Minecraft"
print(f"Bonus: My favorite game is {favorite_game}.")

# --- Alt approach (commented): concatenation with + ---
# print("My name is " + name + " and I am " + str(age) + " years old.")
# ^ Notice we needed str(age) because age is a number, not text.
```

</details>

## Docs / Tutorials

- [Built-in Python Functions](https://docs.python.org/3/library/functions.html)
- [Python variables for beginners ❎](https://www.youtube.com/watch?v=LKFrQXaoSMQ)
