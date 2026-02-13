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

## Docs / Tutorials

- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Built-in Functions](https://docs.python.org/3/library/functions.html)
- [YouTube Playlist: Tech With Tim – Python Programming Tutorials](https://www.youtube.com/playlist?list=PLzMcBGfZo4-mFu00qxl0a67RhjjZj3jXm)
- [YouTube: FizzBuzz (Programming with Mosh)](https://www.youtube.com/watch?v=z3-XFI_nXNM)

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

## Solution (spoiler)

<details>
  <summary>Show one possible solution</summary>

Keep it simple. This is one valid way; many others are fine.

```python title="fizzbuzz.py"
s = input('N (default 100): ').strip()
n = int(s) if s else 100

for i in range(1, n + 1):
    if i % 15 == 0:
        print('FizzBuzz')
    elif i % 3 == 0:
        print('Fizz')
    elif i % 5 == 0:
        print('Buzz')
    else:
        print(i)
```

</details>
