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

## Docs / Tutorials

- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Built-in Functions](https://docs.python.org/3/library/functions.html)
- [YouTube Playlist: Tech With Tim – Python Programming Tutorials](https://www.youtube.com/playlist?list=PLzMcBGfZo4-mFu00qxl0a67RhjjZj3jXm)
- [YouTube: Variables & Data Types (Tech With Tim)](https://www.youtube.com/watch?v=OFrLs22MDAw)

## Example run

```text
$ python variables.py
My name is Alex and I am 12 years old.
Now my name is Alex and I am 13 years old.
```

## Solution (spoiler)

<details>
  <summary>Show example code</summary>

This is one simple example using f-strings.

```python title="variables.py"
name = 'Alex'
age = 12

print(f'My name is {name} and I am {age} years old.')

age = age + 1
print(f'Now my name is {name} and I am {age} years old.')

# Optional:
# favorite_game = 'Minecraft'
# print(f'My favorite game is {favorite_game}.')
```

</details>
