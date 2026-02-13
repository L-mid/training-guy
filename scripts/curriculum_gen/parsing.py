from __future__ import annotations

import re
import unicodedata

from .models import Day, Tier


def slugify(s: str) -> str:
    """
    Convert a human title into a filesystem-safe slug.

    Rules (same as your original):
    - NFKD normalize + strip accents
    - casefold
    - & -> " and "
    - + -> " plus "
    - non-alnum -> hyphen
    - collapse hyphens
    """
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.casefold()
    s = s.replace("&", " and ")
    s = re.sub(r"[+]+", " plus ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "x"


def parse_curriculum(raw: str) -> list[Tier]:
    """
    Parse the RAW curriculum text into a list of Tier objects.

    Contract:
    - Input must contain "TIER N — Name" headers
    - Day lines must be "Day DDD <emoji> — <title>"
    - Raises ValueError for any unrecognized non-empty line
    """
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
            cur.days.append(
                Day(
                    n=int(m.group(1)),
                    emoji=m.group(2).strip(),
                    title=m.group(3).strip(),
                )
            )
            continue

        raise ValueError(f"Unparsed line: {line!r}")

    if cur:
        tiers.append(cur)

    return tiers
