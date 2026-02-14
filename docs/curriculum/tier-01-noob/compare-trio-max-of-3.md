---
title: "💚 — Compare Trio: Max of 3"
sidebar_label: "💚 Compare Trio: Max of 3"
sidebar_position: 7
---

## Task

- Create a file named max3.py.
- Read three integers a, b, c.
- Print the largest value.
- Test with a tie case (like 5, 5, 1).
- (Optional) Print the smallest value too.
- (Optional) Print BOTH using built-ins: max(...) and min(...).

## Example run

```text
$ python max3.py
a: 5
b: 5
c: 1
largest = 5
smallest = 1
```

## Solution (ATTEMPT FIRST)

<details>
  <summary>Show spoiler code (max3.py)</summary>

Two ways are shown: built-ins (easy) and manual comparisons (commented).

```python title="max3.py"
"""max3.py

Find the largest of three numbers (and optionally the smallest).
"""

a = int(input("a: ").strip())
b = int(input("b: ").strip())
c = int(input("c: ").strip())

# Easiest: use built-in max/min
largest = max(a, b, c)
smallest = min(a, b, c)

print(f"largest = {largest}")
print(f"smallest = {smallest}")

# --- Alt approach (commented): manual comparisons ---
# largest = a
# if b > largest: largest = b
# if c > largest: largest = c
# print(largest)
```

</details>

## Docs / Tutorials

- [Built-in Python Functions](https://docs.python.org/3/library/functions.html)
- [Control Flow in Python - If Elif Else Statements](https://www.youtube.com/watch?v=Zp5MuPOtsSY)
