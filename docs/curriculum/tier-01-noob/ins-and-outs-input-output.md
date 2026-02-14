---
title: "💚 — Ins and Outs: Input → Output"
sidebar_label: "💚 Ins and Outs: Input → Output"
sidebar_position: 3
---

## Task

- Create a file named echo.py.
- Ask the user for their name using input(...).
- Print a greeting using the user's input.
- Ask for a second value (favorite color / game / animal) and echo it back.
- (Optional) Format the output nicely (newlines, punctuation).
- (Optional) Use .strip() to clean extra spaces.

## Example run

```text
$ python echo.py
What is your name?  alex
Hello, Alex!
Pick a favorite creature:  dragon
Nice. If I see a dragon, I'll tell it you said hi.
```

## Solution (ATTEMPT FIRST)

<details>
  <summary>Show spoiler code (echo.py)</summary>

Use input(...) to read a string. Use .strip() to remove weird spaces.
This one also makes the name look nicer.

```python title="echo.py"
"""echo.py

Input -> output (a.k.a. 'I say something, you say something')
"""

# input(prompt) prints the prompt and returns what the user typed (as a STRING).
raw_name = input("What is your name? ")

# Clean up: remove leading/trailing spaces, and make it look nice.
name = raw_name.strip().title()  # title() capitalizes words

print(f"Hello, {name}!")

creature = input("Pick a favorite creature: ").strip().lower()

# A little fun line. This is still just printing text.
print(f"Nice. If I see a {creature}, I'll tell it you said hi.")

# Alt idea (commented): multi-line output in one print
# print(f"Hello, {name}!
Your creature is: {creature}
Legendary choice.")
```

</details>

## Docs / Tutorials

- [Built-in Python Functions](https://docs.python.org/3/library/functions.html)
- [Python user input ⌨️](https://www.youtube.com/watch?v=DB9Cq6TSTuQ)
