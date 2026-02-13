from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Day:
    """A single curriculum day inside a tier."""
    n: int
    emoji: str
    title: str


@dataclass(frozen=True)
class Tier:
    """A curriculum tier: header + ordered list of days."""
    n: int
    name: str
    days: list[Day]
