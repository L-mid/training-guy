---
title: "💛 — Loop Drill I: Count 1..N"
sidebar_label: "💛 Loop Drill I: Count 1..N"
sidebar_position: 8
---

## Task

- Create a file named count_to_n.py.
- Read an integer N.
- Print the numbers 1..N (one per line).
- If `N <= 0`, print a message instead of looping.
- (Optional) Also print N..1 (countdown).
- (Optional) Print the sum of 1..N at the end.

## Example run

```text
$ python count_to_n.py
N: 5
1
2
3
4
5
sum = 15
```

## Solution (ATTEMPT FIRST)

<details>
  <summary>Show spoiler code (count_to_n.py)</summary>

Basic loop practice. Also shows how to accumulate a sum.

```python title="count_to_n.py"
"""count_to_n.py

Loop drill: count up to N (and maybe back down).
"""

N = int(input("N: ").strip())

if N <= 0:
    print("N must be positive to count. (Try 1, 2, 5, ...)" )
else:
    total = 0
    for i in range(1, N + 1):
        print(i)
        total += i  # add i into the running total

    print(f"sum = {total}")

    # Optional countdown (commented):
    # for i in range(N, 0, -1):
    #     print(i)
```

</details>

## Docs / Tutorials

- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Built-in Functions](https://docs.python.org/3/library/functions.html)
- [YouTube Playlist: Tech With Tim – Python Programming Tutorials](https://www.youtube.com/playlist?list=PLzMcBGfZo4-mFu00qxl0a67RhjjZj3jXm)
- [YouTube: For Loops (Tech With Tim)](https://www.youtube.com/watch?v=vKeoXxVaga4)
