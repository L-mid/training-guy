---
title: "💚 — If Gate I: Even / Odd"
sidebar_label: "💚 If Gate I: Even / Odd"
sidebar_position: 6
---

## Task

- Create a file named even_odd.py.
- Read an integer n.
- If n is even, print: even. Otherwise print: odd.
- Test with: 0, 1, 2, -3.
- (Optional) Also print whether n is positive/negative/zero.
- (Optional) Put the even/odd logic in a function.

## Example run

```text
$ python even_odd.py
n: -3
odd
negative
```

## Solution (ATTEMPT FIRST)

<details>
  <summary>Show spoiler code (even_odd.py)</summary>

Use n % 2 to check even/odd. Then a second if for sign.

```python title="even_odd.py"
"""even_odd.py

If-gate challenge: decide which message to print.
"""

def even_or_odd(n: int) -> str:
    """Return 'even' or 'odd' based on parity."""
    # % is 'mod' (remainder). Even numbers have remainder 0 when divided by 2.
    return "even" if (n % 2 == 0) else "odd"

s = input("n: ").strip()
n = int(s)  # assume valid int for now (you can add try/except as an upgrade)

print(even_or_odd(n))

# Optional: sign check
if n > 0:
    print("positive")
elif n < 0:
    print("negative")
else:
    print("zero")

# Alt parity approach (commented):
# if n % 2 == 0: print("even")
# else: print("odd")
```

</details>

## Docs / Tutorials

- [Built-in Python Functions](https://docs.python.org/3/library/functions.html)
- [If statements in Python are easy (if, elif, else) 🤔](https://www.youtube.com/watch?v=FvMPfrgGeKs)
