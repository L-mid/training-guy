---
title: "💜⭐ — Boss: Guess-the-Number I"
sidebar_label: "💜⭐ Boss: Guess-the-Number I"
sidebar_position: 10
---

## Task

- Create a file named guess.py.
- Pick a secret number between 1 and 100.
- Loop: ask for a guess until they get it right.
- After each guess, print: too high / too low.
- When correct, print how many guesses it took.
- (Optional) Add an attempt limit (like 10 tries).
- (Optional) Add input validation (no crashing on bad input).

## Hints

- Use: import random and random.randint(1, 100).
- Use a while True loop, break when correct.
- Keep a counter guesses += 1 each loop.

## Example run

```text
$ python guess.py
I'm thinking of a number 1..100.
Guess: 50
Too high!
Guess: 25
Too low!
Guess: 32
Correct! You got it in 3 guesses.
```

## Solution (ATTEMPT FIRST)

<details>
  <summary>Show spoiler code (guess.py)</summary>

Boss mode: includes validation + optional attempt limit + fun flavor text.
Also shows a simpler version in comments.

```python title="guess.py"
"""guess.py

Boss: Guess the Number 🎯

We pick a secret number. The player keeps guessing until they get it.
After each guess we give a hint: too high / too low.
"""

import random

secret = random.randint(1, 100)
guesses = 0
max_attempts = 10  # Optional: change or set to None for unlimited

print("I'm thinking of a number 1..100.")

while True:
    if max_attempts is not None and guesses >= max_attempts:
        print(f"Out of attempts! The secret was {secret}.")
        break

    s = input("Guess: ").strip()

    # Validation: don't crash if they type 'cat' 😼
    try:
        guess = int(s)
    except ValueError:
        print("Please type a whole number like 42.")
        continue

    if guess < 1 or guess > 100:
        print("Stay in range 1..100, wizard.")
        continue

    guesses += 1

    if guess < secret:
        print("Too low!")
    elif guess > secret:
        print("Too high!")
    else:
        print(f"Correct! You got it in {guesses} guesses.")
        break

# --- Simpler version (commented): no validation, no attempt limit ---
# secret = random.randint(1, 100)
# guesses = 0
# while True:
#     guess = int(input('Guess: '))
#     guesses += 1
#     if guess < secret: print('Too low')
#     elif guess > secret: print('Too high')
#     else:
#         print(f'Correct in {guesses}!')
#         break
```

</details>

## Docs / Tutorials

- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Built-in Functions](https://docs.python.org/3/library/functions.html)
- [YouTube Playlist: Tech With Tim – Python Programming Tutorials](https://www.youtube.com/playlist?list=PLzMcBGfZo4-mFu00qxl0a67RhjjZj3jXm)
- [While loops in Python are easy! ♾️](https://www.youtube.com/watch?v=rRTjPnVooxE)
