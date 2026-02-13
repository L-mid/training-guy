from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
from scripts import gen_curriculum


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section(md: str, header: str) -> str:
    """
    Extract the body under '## {header}' up to the next '##' header (or EOF).
    Returns '' if missing.
    """
    rgx = re.compile(rf"(?ms)^##\s+{re.escape(header)}\s*\n(.*?)(?=^##\s+|\Z)")
    m = rgx.search(md)
    return m.group(1).strip() if m else ""


def _pick_first_day_slug_by_tier(tier_n: int) -> str:
    tiers = gen_curriculum.parse(gen_curriculum.RAW)
    t = next(x for x in tiers if x.n == tier_n)
    return gen_curriculum.slugify(t.days[0].title)


def _tier_folder_name(tier_n: int) -> str:
    tiers = gen_curriculum.parse(gen_curriculum.RAW)
    t = next(x for x in tiers if x.n == tier_n)
    return f"tier-{t.n:02d}-{gen_curriculum.slugify(t.name)}"


def _page_path(repo_root: Path, *, tier_n: int, day_slug: str) -> Path:
    return repo_root / "docs" / "curriculum" / _tier_folder_name(tier_n) / f"{day_slug}.md"


def _copy_config_to(tmp_root: Path) -> None:
    shutil.copytree(REPO_ROOT / "curriculum_config", tmp_root / "curriculum_config")


def test_global_defaults_apply_across_all_tiers(tmp_path: Path) -> None:
    """
    Verifies: global defaults apply everywhere AND tier configs are being applied (docs section exists).
    """
    tmp = tmp_path
    _copy_config_to(tmp)

    _write_json(
        tmp / "curriculum_config" / "global.json",
        {
            "defaults": {
                "task": ["__GLOBAL_TASK_SENTINEL__"],
                "checklist": ["A", "B"],
                "hints_block": {"enabled": False},
            }
        },
    )

    gen_curriculum.generate(repo_root=tmp)

    # Global task should appear on first page of every tier.
    for tier_n in range(1, 11):
        slug = _pick_first_day_slug_by_tier(tier_n)
        md = _read(_page_path(tmp, tier_n=tier_n, day_slug=slug))

        assert "- __GLOBAL_TASK_SENTINEL__" in _section(md, "Task")
        assert _section(md, "Docs / Tutorials"), f"Docs section missing for tier {tier_n}"

    # Spot-check some tier-specific docs link labels (proves tier configs are used)
    slug = _pick_first_day_slug_by_tier(1)
    md = _read(_page_path(tmp, tier_n=1, day_slug=slug))
    assert "[Python Tutorial]" in _section(md, "Docs / Tutorials")

    slug = _pick_first_day_slug_by_tier(5)
    md = _read(_page_path(tmp, tier_n=5, day_slug=slug))
    assert "[Git Reference]" in _section(md, "Docs / Tutorials")


def test_tier_defaults_override_global_defaults(tmp_path: Path) -> None:
    """
    Verifies: global -> tier precedence (tier overrides win).
    """
    tmp = tmp_path
    _copy_config_to(tmp)

    _write_json(
        tmp / "curriculum_config" / "global.json",
        {
            "defaults": {
                "task": ["GLOBAL"],
                "checklist": ["C"],
                "hints_block": {"enabled": False},
            }
        },
    )

    # Make tier-02 override the task
    tier2_path = tmp / "curriculum_config" / "tier-02.json"
    tier2 = json.loads(_read(tier2_path))
    tier2.setdefault("tier_defaults", {})["task"] = ["TIER2"]
    _write_json(tier2_path, tier2)

    gen_curriculum.generate(repo_root=tmp)

    slug = _pick_first_day_slug_by_tier(2)
    md = _read(_page_path(tmp, tier_n=2, day_slug=slug))

    task = _section(md, "Task")
    assert "- TIER2" in task
    assert "- GLOBAL" not in task


def test_file_overrides_are_sticky_and_manual_content_is_preserved(tmp_path: Path) -> None:
    """
    Verifies:
      - file overrides win (over global/tier),
      - overrides remain after regeneration,
      - extra frontmatter keys and non-managed sections remain.
    """
    tmp = tmp_path
    _copy_config_to(tmp)

    # Set a global task we can change later.
    _write_json(
        tmp / "curriculum_config" / "global.json",
        {
            "defaults": {
                "task": ["GLOBAL_V1"],
                "checklist": ["Works"],
                "hints_block": {"enabled": False},
            }
        },
    )

    # Add a file override in tier-03 for a real slug.
    slug = _pick_first_day_slug_by_tier(3)
    tier3_path = tmp / "curriculum_config" / "tier-03.json"
    tier3 = json.loads(_read(tier3_path))
    tier3.setdefault("files", {})[slug] = {
        "task": ["FILE_TASK"],
        "checklist_append": ["EXTRA"],
        "hints_block": {"enabled": True},
        "hints": ["H1"],
    }
    _write_json(tier3_path, tier3)

    # First generate.
    gen_curriculum.generate(repo_root=tmp)

    target = _page_path(tmp, tier_n=3, day_slug=slug)
    md1 = _read(target)

    assert "- FILE_TASK" in _section(md1, "Task")
    assert "- [ ] EXTRA" in _section(md1, "Checklist")
    assert "- H1" in _section(md1, "Hints")

    # Add custom frontmatter key + a non-managed section.
    lines = md1.splitlines()
    assert lines and lines[0].strip() == "---"

    end_idx = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    lines.insert(end_idx, "custom: true")
    md1_custom = "\n".join(lines).rstrip() + "\n\n## Notes\nThis should stay.\n"
    target.write_text(md1_custom, encoding="utf-8")

    # Change global defaults; file override should still win after regen.
    _write_json(
        tmp / "curriculum_config" / "global.json",
        {
            "defaults": {
                "task": ["GLOBAL_V2"],
                "checklist": ["Works"],
                "hints_block": {"enabled": False},
            }
        },
    )

    gen_curriculum.generate(repo_root=tmp)
    md2 = _read(target)

    assert "custom: true" in md2
    assert "## Notes" in md2
    assert "This should stay." in md2

    assert "- FILE_TASK" in _section(md2, "Task")
    assert "- GLOBAL_V2" not in _section(md2, "Task")

    # Another Tier 3 page (no file override) should pick up the new global.
    tiers = gen_curriculum.parse(gen_curriculum.RAW)
    t3 = next(t for t in tiers if t.n == 3)
    other_day = next(d for d in t3.days if gen_curriculum.slugify(d.title) != slug)
    other_slug = gen_curriculum.slugify(other_day.title)

    other_md = _read(_page_path(tmp, tier_n=3, day_slug=other_slug))
    assert "- GLOBAL_V2" in _section(other_md, "Task")
