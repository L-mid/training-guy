from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re
import unicodedata


RAW = r"""
TIER 1 — NOOB
Day 001 💚 — Print Spell: Hello, World
 Day 002 💚 — Variable Storage: Store + Show
 Day 003 💚 — Echo Mage: Input → Output
 Day 004 💛 — Number Parser: str → int/float
 Day 005 💛 — Calculator: + − × ÷
 Day 006 💚 — If Gate I: Even / Odd
 Day 007 💚 — Compare Trio: Max of 3
 Day 008 💛 — Loop Drill I: Count 1..N
 Day 009 💛 — FizzBuzz I
 Day 010 💜🎰 — Boss: Guess-the-Number I

TIER 2 — BEGINNER
Day 011 💚 — Variable Chest Reload: Types + Reassign
 Day 012 💛 — If Gate II: Grade Ladder (A/B/C)
 Day 013 💛 — Loop Drill II: Sum 1..N
 Day 014 💛 — Loop Drill III: Factorial
 Day 015 💛 — String Forge I: Reverse
 Day 016 💛 — String Forge II: Palindrome
 Day 017 💛 — Counter Spell: Vowels
 Day 018 💛 — FizzBuzz II (with function)
 Day 019 💛 — Prime Check I
 Day 020 💜🧠 — Boss: Two Sum (Brute Force + Trace)

TIER 3 — BEGINNER +
Day 021 💚 — List 101: Append/Pop/Index
 Day 022 💛 — Loop + List: Running Sum
 Day 023 💛 — Min/Max Scan
 Day 024 💛 — Dedup (Set)
 Day 025 💛 — Dict 101: Frequency Counter I
 Day 026 💛 — Frequency Counter II (Top 1)
 Day 027 💛 — Prime Check II (optimize a bit)
 Day 028 💛 — Guess-the-Number II (attempt limit)
 Day 029 💛 — Rock Paper Scissors (best-of-3)
 Day 030 💜🛡️ — Boss: Text Health Bar (HP + Damage + Heal)

TIER 4 — NOVICE
Day 031 💛 — Function Forge I: Make 3 helper funcs
 Day 032 💛 — Function Forge II: Return Values
 Day 033 💛 — Refactor Rumble: Remove Copy/Paste
 Day 034 💛 — Menu Loop: Start/Play/Quit
 Day 035 ❤️‍🔥 — State Machine: menu → game → win/lose
 Day 036 💛 — Debug Prints: Track State + Variables
 Day 037 💛 — String Split Parser
 Day 038 💛 — Cleaner: strip + casefold + replace
 Day 039 ❤️‍🔥 — Hangman I: Core Loop
 Day 040 💜📜 — Boss: Hangman II (win/lose + replay + polish)

TIER 5 — PRO
Day 041 💛 — Git Init Quest
 Day 042 💛 — Git Add/Commit (3 commits)
 Day 043 💛 — Git Log Time Travel
 Day 044 💛 — Git Diff Detective
 Day 045 💛 — .gitignore Shield
 Day 046 ❤️‍🔥 — Branching Basics: feature branch
 Day 047 ❤️‍🔥 — Merge Conflict Mini-Boss
 Day 048 💛 — Revert the Mistake
 Day 049 💛 — Tag the Win
 Day 050 💜🧪 — Boss: “Clean Repo” Checkpoint (README + commits + tag)

TIER 6 — PRO +
Day 051 💛 — File I/O I: Write Text
 Day 052 💛 — File I/O II: Read Text
 Day 053 💛 — CSV Saver
 Day 054 💛 — CSV Loader
 Day 055 💛 — JSON Roundtrip I
 Day 056 💛 — JSON Roundtrip II (sorted keys + indent)
 Day 057 💛 — JSONL Append
 Day 058 💛 — JSONL Stream
 Day 059 ❤️‍🔥 — Error Handling Arena (try/except)
 Day 060 💜🗺️ — Boss: Tiny Data Quest (load → clean → save JSONL)

TIER 7 — PRO ++
Day 061 💛 — Tests I: 3 asserts for one function
 Day 062 💛 — Pytest First Run
 Day 063 💛 — Tests II: Edge Cases Pack (3 edges)
 Day 064 💛 — Tests III: “Bad Input” Raises
 Day 065 💛 — Debug Drill: Fix 3 failing tests
 Day 066 💛 — Refactor: Split into 2 modules
 Day 067 💛 — CLI Menu: Use functions per option
 Day 068 ❤️‍🔥 — Data Cleaner: Validate email/age
 Day 069 ❤️‍🔥 — Scoreboard Save/Load (JSON)
 Day 070 💜🐉 — Boss: CLI Mini-App (menu + validate + save + tests)

TIER 8 — TURTLE GAMES
Day 071 💛 — Turtle Move Set I (WASD)
 Day 072 💛 — Turtle Move Set II (speed variable)
 Day 073 💛 — Turtle Coin (random spawn)
 Day 074 ❤️‍🔥 — Turtle Lava (lose on touch)
 Day 075 💛 — Turtle Timer (countdown)
 Day 076 💛 — Turtle Levels (next stage)
 Day 077 ❤️‍🔥 — Turtle Enemy (chase)
 Day 078 💛 — Turtle HUD (score + time)
 Day 079 ❤️‍🔥 — Turtle Polish (restart + win screen)
 Day 080 💜🌙 — Boss: Turtle Game Ship (playable loop + 2 levels)

TIER 9 —  LUA
Day 081 💚 — Lua Hello, Print
 Day 082 💚 — Lua Variables Reload: number/string/boolean
 Day 083 💛 — Lua If Gate
 Day 084 💛 — Lua Loops I (for)
 Day 085 💛 — Lua Loops II (while)
 Day 086 💛 — Lua Functions (params + return)
 Day 087 💛 — Lua Tables I (array mode)
 Day 088 ❤️‍🔥 — Lua Tables II (dict mode)
 Day 089 💛 — Python Flashback I: FizzBuzz III (fast)
 Day 090 💜🏗️ — Boss: Lua Mini-Game (guess number + score + replay)

TIER 10 — ROBLOX
Day 091 💚 — Roblox Studio Boot
 Day 092 💚 — Spawn a Part (size/color/position)
 Day 093 💛 — Script Placement (Server Script)
 Day 094 💚 — Print to Output (Luau)
 Day 095 💛 — Variables Reload (speed/jump settings)
 Day 096 ❤️‍🔥 — Touch Event: Coin Pickup
 Day 097 💛 — Score State: IntValue counter
 Day 098 💛 — Score UI: BillboardGui label
 Day 099 💛 — Python Flashback II: Frequency Counter III
 Day 100 💜🚀 — Final Boss: Ship Roblox Obby (coin + hazard + checkpoint + score UI)
""".strip("\n")


@dataclass
class Day:
    n: int
    emoji: str
    title: str


@dataclass
class Tier:
    n: int
    name: str
    days: list[Day]


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.casefold()
    s = s.replace("&", " and ")
    s = re.sub(r"[+]+", " plus ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "x"


def parse(raw: str) -> list[Tier]:
    tiers: list[Tier] = []
    cur: Tier | None = None

    tier_re = re.compile(r"^TIER\s+(\d+)\s+—\s+(.*)$")
    day_re = re.compile(r"^Day\s+(\d{3})\s+(.*?)\s+—\s+(.*)$")

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        m = tier_re.match(line)
        if m:
            if cur:
                tiers.append(cur)
            cur = Tier(n=int(m.group(1)), name=m.group(2).strip(), days=[])
            continue

        m = day_re.match(line)
        if m:
            if cur is None:
                raise ValueError("Found a Day before any TIER header.")
            n = int(m.group(1))
            emoji = m.group(2).strip()
            title = m.group(3).strip()
            cur.days.append(Day(n=n, emoji=emoji, title=title))
            continue

        raise ValueError(f"Unparsed line: {line!r}")

    if cur:
        tiers.append(cur)
    return tiers


def links_for_tier(tier_n: int) -> list[tuple[str, str]]:
    # Put URLs here because these files will live inside your docs.
    if tier_n <= 4:
        return [
            ("Python Tutorial", "https://docs.python.org/3/tutorial/"),
            ("Built-in Functions", "https://docs.python.org/3/library/functions.html"),
        ]
    if tier_n == 5:
        return [
            ("Git Reference", "https://git-scm.com/docs"),
            ("Pro Git (free book)", "https://git-scm.com/book/en/v2"),
        ]
    if tier_n == 6:
        return [
            ("pathlib", "https://docs.python.org/3/library/pathlib.html"),
            ("csv", "https://docs.python.org/3/library/csv.html"),
            ("json", "https://docs.python.org/3/library/json.html"),
        ]
    if tier_n == 7:
        return [
            ("pytest docs", "https://docs.pytest.org/en/stable/"),
        ]
    if tier_n == 8:
        return [
            ("Python turtle", "https://docs.python.org/3/library/turtle.html"),
        ]
    if tier_n == 9:
        return [
            ("Luau docs", "https://create.roblox.com/docs/luau"),
            ("Luau control structures", "https://create.roblox.com/docs/luau/control-structures"),
            ("Luau functions", "https://create.roblox.com/docs/luau/functions"),
        ]
    if tier_n == 10:
        return [
            ("Roblox scripting docs", "https://create.roblox.com/docs/scripting"),
            ("Intro to scripting (tutorial)", "https://create.roblox.com/docs/tutorials/use-case-tutorials/scripting/basic-scripting/intro-to-scripting"),
            ("Luau docs", "https://create.roblox.com/docs/luau"),
        ]
    return []


def write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    docs_root = repo_root / "docs" / "curriculum"

    tiers = parse(RAW)

    # Root category + landing page
    write_file(
        docs_root / "_category_.json",
        json.dumps(
            {
                "label": "Curriculum",
                "position": 1,
                "link": {
                    "type": "generated-index",
                    "title": "Curriculum",
                    "description": "Click a tier to start. Each tier page lists the days.",
                },
            },
            indent=2,
        )
        + "\n",
    )

    landing = ["# Curriculum\n", "## Tiers\n"]
    for t in tiers:
        tier_folder = f"tier-{t.n:02d}-{slugify(t.name)}"
        landing.append(f"- **TIER {t.n} — {t.name}** → ./{tier_folder}/\n")
    write_file(docs_root / "index.mdx", "".join(landing) + "\n")

    # Tiers + days
    for t in tiers:
        tier_folder = docs_root / f"tier-{t.n:02d}-{slugify(t.name)}"
        write_file(
            tier_folder / "_category_.json",
            json.dumps(
                {
                    "label": f"TIER {t.n} — {t.name}",
                    "position": t.n,
                    "link": {
                        "type": "generated-index",
                        "title": f"TIER {t.n} — {t.name}",
                        "description": f"Days {t.days[0].n:03d}–{t.days[-1].n:03d}",
                    },
                },
                indent=2,
            )
            + "\n",
        )

        tier_links = links_for_tier(t.n)

        for i, d in enumerate(t.days, start=1):
            # NEW (no Day/number in names)
            filename = f"{slugify(d.title)}.md"
            sidebar_label = f"{d.emoji} {d.title}"
            title = f"{d.emoji} — {d.title}"
 
            docs_lines = []
            if tier_links:
                docs_lines.append("\n## Docs / Tutorials\n")
                for (label, url) in tier_links:
                    docs_lines.append(f"- [{label}]({url})\n")

            body = f"""---
title: "{title}"
sidebar_label: "{sidebar_label}"
sidebar_position: {i}
---

## Task

- TODO

## Checklist

- [ ] Works
- [ ] Cleaned up
- [ ] (Optional) 1 upgrade / stretch

{''.join(docs_lines)}
"""
            write_file(tier_folder / filename, body)

    print(f"Generated curriculum at: {docs_root}")


if __name__ == "__main__":
    main()
