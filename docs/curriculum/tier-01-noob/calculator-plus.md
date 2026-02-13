---
title: "💛 — Calculator: + − × ÷"
sidebar_label: "💛 Calculator: + − × ÷"
sidebar_position: 5
---

## Task

- Create a file named calculator.py.
- Read two numbers (use float) from input.
- Print the results of: +, -, *, /.
- If the second number is 0, don’t crash on division (print a message).
- (Optional) Ask for the operator (+ - * /) and only do that one.
- (Optional) Round results to 2 decimals.

## Example run

```text
$ python calculator.py
a: 10
b: 4
a + b = 14.0
a - b = 6.0
a * b = 40.0
a / b = 2.5
```

## Solution (ATTEMPT FIRST)

<details>
  <summary>Show spoiler code (calculator.py)</summary>

This prints all four operations, with a safe divide-by-zero check.
An optional single-op mode is included in comments.

```python title="calculator.py"
"""calculator.py

A tiny calculator. We'll be polite about division by zero.
"""

def read_number(prompt: str) -> float:
    """Read a float from input, retrying until valid."""
    while True:
        s = input(prompt).strip()
        try:
            return float(s)
        except ValueError:
            print("Please enter a number like 3 or 2.5")

a = read_number("a: ")
b = read_number("b: ")

print(f"a + b = {a + b}")
print(f"a - b = {a - b}")
print(f"a * b = {a * b}")

if b == 0:
    print("a / b = (nope) division by zero is illegal in this kingdom")
else:
    print(f"a / b = {a / b}")

# --- Optional single-operator mode (commented) ---
# op = input("Choose op (+ - * /): ").strip()
# if op == "+": print(a + b)
# elif op == "-": print(a - b)
# elif op == "*": print(a * b)
# elif op == "/":
#     print("nope" if b == 0 else a / b)
# else:
#     print("Unknown operator")
```

</details>

## Docs / Tutorials

- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Built-in Functions](https://docs.python.org/3/library/functions.html)
- [YouTube Playlist: Tech With Tim – Python Programming Tutorials](https://www.youtube.com/playlist?list=PLzMcBGfZo4-mFu00qxl0a67RhjjZj3jXm)
- [Python Program #30 - Make a Simple Calculator in Python](https://www.youtube.com/watch?v=BM_MlI6MySY)
