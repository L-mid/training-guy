from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

import pytest

from scripts.curriculum_gen.parsing import parse_curriculum, slugify
from scripts.curriculum_gen.raw_curriculum import RAW


@dataclass(frozen=True)
class TierIndex:
    """
    Precomputed tier lookup to keep tests fast + readable.

    Integration contract:
    - uses RAW curriculum text
    - generates deterministic tier folder names like:
        tier-03-beginner-plus
    """
    tier_to_first_day_slug: dict[int, str]
    tier_to_folder: dict[int, str]


@pytest.fixture(scope="session")
def tier_index() -> TierIndex:
    tiers = parse_curriculum(RAW)
    tier_to_first_day_slug: dict[int, str] = {}
    tier_to_folder: dict[int, str] = {}

    for t in tiers:
        tier_to_first_day_slug[t.n] = slugify(t.days[0].title)
        tier_to_folder[t.n] = f"tier-{t.n:02d}-{slugify(t.name)}"

    return TierIndex(
        tier_to_first_day_slug=tier_to_first_day_slug,
        tier_to_folder=tier_to_folder,
    )


@pytest.fixture
def tmp_repo(tmp_path: Path) -> Path:
    """
    Create a temporary "repo root" layout for generator integration tests.

    Copies:
      real_repo/curriculum_config -> tmp_repo/curriculum_config

    Writes:
      tmp_repo/docs/curriculum/... during generation
    """
    real_repo_root = Path(__file__).resolve().parents[1]
    src = real_repo_root / "curriculum_config"
    dst = tmp_path / "curriculum_config"
    shutil.copytree(src, dst)
    return tmp_path
