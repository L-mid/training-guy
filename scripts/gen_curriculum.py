from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import copy
import json
import re
import unicodedata
from typing import Any


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


# Backstop links if you don't want to put them in config.
# (If you set docs_links in config, those take precedence.)

def links_for_tier(tier_n: int) -> list[dict[str, str]]:
    if tier_n <= 4:
        return [
            {"label": "Python Tutorial", "url": "https://docs.python.org/3/tutorial/"},
            {
                "label": "Built-in Functions",
                "url": "https://docs.python.org/3/library/functions.html",
            },
        ]
    if tier_n == 5:
        return [
            {"label": "Git Reference", "url": "https://git-scm.com/docs"},
            {"label": "Pro Git (free book)", "url": "https://git-scm.com/book/en/v2"},
        ]
    if tier_n == 6:
        return [
            {"label": "pathlib", "url": "https://docs.python.org/3/library/pathlib.html"},
            {"label": "csv", "url": "https://docs.python.org/3/library/csv.html"},
            {"label": "json", "url": "https://docs.python.org/3/library/json.html"},
        ]
    if tier_n == 7:
        return [
            {"label": "pytest docs", "url": "https://docs.pytest.org/en/stable/"},
        ]
    if tier_n == 8:
        return [
            {"label": "Python turtle", "url": "https://docs.python.org/3/library/turtle.html"},
        ]
    if tier_n == 9:
        return [
            {"label": "Luau docs", "url": "https://create.roblox.com/docs/luau"},
            {
                "label": "Luau control structures",
                "url": "https://create.roblox.com/docs/luau/control-structures",
            },
            {"label": "Luau functions", "url": "https://create.roblox.com/docs/luau/functions"},
        ]
    if tier_n == 10:
        return [
            {"label": "Roblox scripting docs", "url": "https://create.roblox.com/docs/scripting"},
            {
                "label": "Intro to scripting (tutorial)",
                "url": "https://create.roblox.com/docs/tutorials/use-case-tutorials/scripting/basic-scripting/intro-to-scripting",
            },
            {"label": "Luau docs", "url": "https://create.roblox.com/docs/luau"},
        ]
    return []


# -------------------------
# Config loading + merging
# -------------------------

_ALLOWED_TIER_ROOT_KEYS = {"tier_defaults", "files"}
_ALLOWED_GLOBAL_ROOT_KEYS = {"defaults"}

_ALLOWED_SECTION_KEYS = {
    "task",
    "checklist",
    "hints",
    "docs_links",
    "hints_block",
    # Append semantics (optional)
    "task_append",
    "checklist_append",
    "hints_append",
    "docs_links_append",
}


def _normalize_newlines(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n")


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"Bad JSON in {path}") from e


def _validate_section_obj(obj: dict[str, Any], ctx: str) -> None:
    extra = set(obj.keys()) - _ALLOWED_SECTION_KEYS
    if extra:
        raise ValueError(f"Unknown keys in {ctx}: {sorted(extra)}")

    for k in ("task", "task_append", "checklist", "checklist_append", "hints", "hints_append"):
        if k in obj and obj[k] is not None:
            if not isinstance(obj[k], list) or not all(isinstance(x, str) for x in obj[k]):
                raise ValueError(f"{ctx}.{k} must be a list[str]")

    for k in ("docs_links", "docs_links_append"):
        if k in obj and obj[k] is not None:
            if not isinstance(obj[k], list):
                raise ValueError(f"{ctx}.{k} must be a list")
            for i, it in enumerate(obj[k]):
                if isinstance(it, dict):
                    if not isinstance(it.get("label"), str) or not isinstance(it.get("url"), str):
                        raise ValueError(f"{ctx}.{k}[{i}] must have str label/url")
                elif isinstance(it, list) or isinstance(it, tuple):
                    if len(it) != 2 or not isinstance(it[0], str) or not isinstance(it[1], str):
                        raise ValueError(f"{ctx}.{k}[{i}] must be [label, url]")
                else:
                    raise ValueError(f"{ctx}.{k}[{i}] must be an object with label/url")

    if "hints_block" in obj and obj["hints_block"] is not None:
        hb = obj["hints_block"]
        if not isinstance(hb, dict):
            raise ValueError(f"{ctx}.hints_block must be an object")
        if "enabled" in hb and not isinstance(hb["enabled"], bool):
            raise ValueError(f"{ctx}.hints_block.enabled must be a bool")


def _merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Deep-merge dicts. Lists are replaced. Supports *_append keys for list appends."""

    out = copy.deepcopy(base)

    # First: handle *_append keys (so you can do additive edits cleanly)
    for k, v in override.items():
        if not k.endswith("_append"):
            continue
        target = k[: -len("_append")]
        if v is None:
            continue
        prev = out.get(target)
        if prev is None:
            prev = []
        if not isinstance(prev, list) or not isinstance(v, list):
            raise ValueError(f"Cannot append non-lists via {k}")
        out[target] = prev + v

    # Second: normal override/deep-merge
    for k, v in override.items():
        if k.endswith("_append"):
            continue
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)  # type: ignore[arg-type]
        else:
            out[k] = copy.deepcopy(v)

    return out


def load_global_defaults(config_root: Path) -> dict[str, Any]:
    cfg = _read_json(config_root / "global.json")
    if not cfg:
        return {}
    extra = set(cfg.keys()) - _ALLOWED_GLOBAL_ROOT_KEYS
    if extra:
        raise ValueError(f"Unknown keys in global.json: {sorted(extra)}")

    defaults = cfg.get("defaults", {})
    if not isinstance(defaults, dict):
        raise ValueError("global.json.defaults must be an object")
    _validate_section_obj(defaults, "global.json.defaults")
    return defaults


def load_tier_config(config_root: Path, tier_n: int) -> dict[str, Any]:
    path = config_root / f"tier-{tier_n:02d}.json"
    cfg = _read_json(path)
    if not cfg:
        return {"tier_defaults": {}, "files": {}}

    extra = set(cfg.keys()) - _ALLOWED_TIER_ROOT_KEYS
    if extra:
        raise ValueError(f"Unknown keys in {path.name}: {sorted(extra)}")

    tier_defaults = cfg.get("tier_defaults", {})
    files = cfg.get("files", {})

    if not isinstance(tier_defaults, dict):
        raise ValueError(f"{path.name}.tier_defaults must be an object")
    if not isinstance(files, dict):
        raise ValueError(f"{path.name}.files must be an object")

    _validate_section_obj(tier_defaults, f"{path.name}.tier_defaults")

    for slug, overrides in files.items():
        if not isinstance(slug, str):
            raise ValueError(f"{path.name}.files keys must be strings")
        if not isinstance(overrides, dict):
            raise ValueError(f"{path.name}.files[{slug}] must be an object")
        _validate_section_obj(overrides, f"{path.name}.files[{slug}]")

    return {"tier_defaults": tier_defaults, "files": files}


# -------------------------
# Markdown frontmatter + section edits
# -------------------------

_MANAGED_SECTIONS = [
    "Task",
    "Checklist",
    "Hints",
    "Docs / Tutorials",
]


def _find_frontmatter_block(md: str) -> tuple[str | None, str]:
    md = _normalize_newlines(md)
    if not md.startswith("---\n"):
        return None, md

    end = md.find("\n---\n", 4)
    if end == -1:
        return None, md

    fm = md[: end + len("\n---\n")]
    body = md[end + len("\n---\n") :]
    return fm, body


def _upsert_frontmatter(
    existing: str,
    *,
    title: str,
    sidebar_label: str,
    sidebar_position: int,
) -> str:
    """Preserve any extra frontmatter keys, but set title/label/position deterministically."""

    fm, body = _find_frontmatter_block(existing)

    keep_lines: list[str] = []
    if fm is not None:
        lines = fm.splitlines()
        # lines[0] == '---', lines[-1] == '---'
        for ln in lines[1:-1]:
            if re.match(r"^(title|sidebar_label|sidebar_position):", ln.strip()):
                continue
            keep_lines.append(ln)

    # YAML accepts JSON-quoted strings
    title_q = json.dumps(title, ensure_ascii=False)
    label_q = json.dumps(sidebar_label, ensure_ascii=False)

    new_fm_lines = [
        "---",
        f"title: {title_q}",
        f"sidebar_label: {label_q}",
        f"sidebar_position: {sidebar_position}",
    ]
    new_fm_lines.extend(keep_lines)
    new_fm_lines.append("---")

    body = body.lstrip("\n")
    return "\n".join(new_fm_lines) + "\n\n" + body


def _section_regex(header: str) -> re.Pattern[str]:
    # Matches: ## Header
    # Captures header line, then content until next ## ... or EOF.
    escaped = re.escape(header)
    return re.compile(rf"(?ms)(^##\s+{escaped}\s*\n)(.*?)(?=^##\s+|\Z)")


def _remove_section(md: str, header: str) -> str:
    rgx = _section_regex(header)
    if not rgx.search(md):
        return md
    md = rgx.sub("", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip("\n") + "\n"


def _replace_or_append_section(md: str, header: str, new_section_body: str) -> str:
    """Replace a managed section's content, or append it if missing."""

    rgx = _section_regex(header)
    if rgx.search(md):
        md = rgx.sub(rf"\1{new_section_body}", md)
        return md

    # Append at end with decent spacing
    md = md.rstrip() + "\n\n" + f"## {header}\n" + new_section_body
    return md


def _section_body_from_lines(lines: list[str]) -> str:
    # Always keep a blank line after header, and a blank line after the content.
    return "\n" + "\n".join(lines).rstrip() + "\n\n"


def _render_bullets(items: list[str]) -> list[str]:
    return [f"- {x}" for x in items]


def _render_checklist(items: list[str]) -> list[str]:
    return [f"- [ ] {x}" for x in items]


def _render_docs_links(links: list[Any]) -> list[str]:
    out: list[str] = []
    for it in links:
        if isinstance(it, dict):
            label = it.get("label")
            url = it.get("url")
        else:
            label, url = it  # [label, url]
        out.append(f"- [{label}]({url})")
    return out


def write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def generate(*, repo_root: Path) -> Path:
    """
    Generate/refresh curriculum docs under {repo_root}/docs/curriculum.

    Returns:
        docs_root Path
    """
    docs_root = repo_root / "docs" / "curriculum"
    config_root = repo_root / "curriculum_config"

    tiers = parse(RAW)
    global_defaults = load_global_defaults(config_root)

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

    landing = ["# Curriculum\n", "\n## Tiers\n"]
    for t in tiers:
        tier_folder = f"tier-{t.n:02d}-{slugify(t.name)}"
        landing.append(f"- **TIER {t.n} — {t.name}** → ./{tier_folder}/\n")
    write_file(docs_root / "index.mdx", "".join(landing) + "\n")

    # Tiers + days
    for t in tiers:
        tier_cfg = load_tier_config(config_root, t.n)
        tier_defaults = tier_cfg["tier_defaults"]
        file_overrides = tier_cfg["files"]

        tier_folder = docs_root / f"tier-{t.n:02d}-{slugify(t.name)}"

        expected_slugs = {slugify(d.title) for d in t.days}
        extra = set(file_overrides.keys()) - expected_slugs
        if extra:
            raise ValueError(
                f"{config_root / f'tier-{t.n:02d}.json'} contains unknown slugs: {sorted(extra)}"
            )

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

        for i, d in enumerate(t.days, start=1):
            filename = f"{slugify(d.title)}.md"
            slug = slugify(d.title)

            sidebar_label = f"{d.emoji} {d.title}"
            title = f"{d.emoji} — {d.title}"

            effective = _merge(global_defaults, tier_defaults)
            effective = _merge(effective, file_overrides.get(slug, {}))

            task = effective.get("task", ["TODO"])
            checklist = effective.get(
                "checklist", ["Works", "Cleaned up", "(Optional) 1 upgrade / stretch"]
            )

            hints_block = effective.get("hints_block", {})
            hints_enabled = bool(hints_block.get("enabled", False))
            hints = effective.get("hints", []) if hints_enabled else []

            if "docs_links" in effective:
                docs_links = effective["docs_links"]
            else:
                docs_links = links_for_tier(t.n)

            path = tier_folder / filename
            existing = path.read_text(encoding="utf-8") if path.exists() else ""
            existing = _normalize_newlines(existing)

            md = _upsert_frontmatter(
                existing,
                title=title,
                sidebar_label=sidebar_label,
                sidebar_position=i,
            )

            md = _replace_or_append_section(md, "Task", _section_body_from_lines(_render_bullets(task)))
            md = _replace_or_append_section(
                md, "Checklist", _section_body_from_lines(_render_checklist(checklist))
            )

            if hints_enabled:
                md = _replace_or_append_section(
                    md, "Hints", _section_body_from_lines(_render_bullets(hints))
                )
            else:
                md = _remove_section(md, "Hints")

            if docs_links:
                md = _replace_or_append_section(
                    md,
                    "Docs / Tutorials",
                    _section_body_from_lines(_render_docs_links(docs_links)),
                )
            else:
                md = _remove_section(md, "Docs / Tutorials")

            write_file(path, md.rstrip() + "\n")

    print(f"Generated curriculum at: {docs_root}")
    return docs_root


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    generate(repo_root=repo_root)


if __name__ == "__main__":
    main()
