---
title: "💛 — FizzBuzz I"
sidebar_label: "💛 FizzBuzz I"
sidebar_position: 9
---

## Task

- Create a file named fizzbuzz.py.
- For numbers 1..N:
- - Print Fizz if divisible by 3
- - Print Buzz if divisible by 5
- - Print FizzBuzz if divisible by both
- - Otherwise print the number
- (Optional) Let the user choose N; default to 100.
- (Optional) Add a 'mode' where the words are different (like Zap/Zoop).

## Example run

```text
$ python fizzbuzz.py
N (default 100): 16
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
16
```

## Solution (ATTEMPT FIRST)

<details>
  <summary>Show spoiler code (fizzbuzz.py)</summary>

This version is extra-commented and includes an alt approach in comments.

```python title="fizzbuzz.py"
"""fizzbuzz.py

FizzBuzz: a classic loop + if logic puzzle.

Rules:
- divisible by 3 -> Fizz
- divisible by 5 -> Buzz
- divisible by 15 -> FizzBuzz
"""

s = input("N (default 100): ").strip()
n = int(s) if s else 100

for i in range(1, n + 1):
    # Check 'both' first so 15 doesn't get caught by 3 or 5 early.
    if i % 15 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)

# --- Alt approach (commented): build a word, then print word or number ---
# for i in range(1, n + 1):
#     word = ""
#     if i % 3 == 0: word += "Fizz"
#     if i % 5 == 0: word += "Buzz"
#     print(word if word else i)
```

</details>

## Docs / Tutorials

- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Built-in Functions](https://docs.python.org/3/library/functions.html)
- [YouTube Playlist: Tech With Tim – Python Programming Tutorials](https://www.youtube.com/playlist?list=PLzMcBGfZo4-mFu00qxl0a67RhjjZj3jXm)
- [YouTube: FizzBuzz (Programming with Mosh)](https://www.youtube.com/watch?v=z3-XFI_nXNM)
