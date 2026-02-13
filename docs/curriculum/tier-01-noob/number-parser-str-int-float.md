---
title: "💛 — Number Parser: str → int/float"
sidebar_label: "💛 Number Parser: str → int/float"
sidebar_position: 4
---

## Task

- Create a file named parse_numbers.py.
- Read one whole number (int) from input and print it + 1.
- Read one decimal number (float) and print it * 2.
- Print the type(...) of both parsed values.
- (Optional) Handle bad input by printing a friendly message.
- (Optional) Accept blanks by using defaults (like 0 or 1.0).

## Example run

```text
$ python parse_numbers.py
Enter a whole number:  41
n + 1 = 42
type(n) = <class 'int'>
Enter a decimal number:  2.5
x * 2 = 5.0
type(x) = <class 'float'>
```

## Solution (ATTEMPT FIRST)

<details>
  <summary>Show spoiler code (parse_numbers.py)</summary>

Key idea: input() gives you a string. int(...) and float(...) convert it.
Try/except lets you handle bad input without crashing.

```python title="parse_numbers.py"
"""parse_numbers.py

Parsing numbers from input (strings -> int/float).
If parsing fails, we print a friendly message instead of exploding.
"""

s_int = input("Enter a whole number: ").strip()

try:
    n = int(s_int)  # convert string -> int
except ValueError:
    print("That wasn't a whole number. Example: 41")
else:
    print(f"n + 1 = {n + 1}")
    print(f"type(n) = {type(n)}")

print()  # blank line for readability

s_float = input("Enter a decimal number: ").strip()

try:
    x = float(s_float)  # convert string -> float
except ValueError:
    print("That wasn't a decimal number. Example: 2.5")
else:
    print(f"x * 2 = {x * 2}")
    print(f"type(x) = {type(x)}")

# Alt idea (commented): defaults for empty input
# s = input("Enter a whole number (default 0): ").strip()
# n = int(s) if s else 0
```

</details>

## Docs / Tutorials

- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Built-in Functions](https://docs.python.org/3/library/functions.html)
- [YouTube Playlist: Tech With Tim – Python Programming Tutorials](https://www.youtube.com/playlist?list=PLzMcBGfZo4-mFu00qxl0a67RhjjZj3jXm)
- [Floats and Integers | How To Python](https://www.youtube.com/watch?v=77TsTM3XxmA)
