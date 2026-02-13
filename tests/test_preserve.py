from __future__ import annotations

import json
from pathlib import Path

from scripts.curriculum_gen.generator import generate
from scripts.curriculum_gen.parsing import parse_curriculum, slugify
from scripts.curriculum_gen.raw_curriculum import RAW

from ._util import page_path, read_text, section_body, write_json


def test_file_overrides_sticky_and_manual_content_preserved(tmp_repo: Path, tier_index) -> None:
    """
    Verifies:
    - file overrides win (over global/tier)
    - overrides remain after regeneration
    - extra frontmatter keys and non-managed sections remain
    """
    # Global baseline
    write_json(
        tmp_repo / "curriculum_config" / "global.json",
        {"defaults": {"task": ["GLOBAL_V1"], "checklist": ["Works"], "hints_block": {"enabled": False}}},
    )

    # File override on Tier 3, first day
    slug = tier_index.tier_to_first_day_slug[3]
    folder = tier_index.tier_to_folder[3]
    tier3_path = tmp_repo / "curriculum_config" / "tier-03.json"
    tier3 = json.loads(read_text(tier3_path))
    tier3.setdefault("files", {})[slug] = {
        "task": ["FILE_TASK"],
        "checklist_append": ["EXTRA"],
        "hints_block": {"enabled": True},
        "hints": ["H1"],
    }
    write_json(tier3_path, tier3)

    # Generate v1
    generate(repo_root=tmp_repo)

    target = page_path(tmp_repo, tier_folder=folder, day_slug=slug)
    md1 = read_text(target)

    assert "- FILE_TASK" in section_body(md1, "Task")
    assert "- [ ] EXTRA" in section_body(md1, "Checklist")
    assert "- H1" in section_body(md1, "Hints")

    # Inject custom frontmatter key + non-managed section
    lines = md1.splitlines()
    assert lines and lines[0].strip() == "---"
    end_idx = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    lines.insert(end_idx, "custom: true")

    md1_custom = "\n".join(lines).rstrip() + "\n\n## Notes\nThis should stay.\n"
    target.write_text(md1_custom, encoding="utf-8")

    # Change global to v2 (file override should still win)
    write_json(
        tmp_repo / "curriculum_config" / "global.json",
        {"defaults": {"task": ["GLOBAL_V2"], "checklist": ["Works"], "hints_block": {"enabled": False}}},
    )

    generate(repo_root=tmp_repo)
    md2 = read_text(target)

    assert "custom: true" in md2
    assert "## Notes" in md2
    assert "This should stay." in md2

    assert "- FILE_TASK" in section_body(md2, "Task")
    assert "- GLOBAL_V2" not in section_body(md2, "Task")

    # Another Tier 3 day (no file override) should pick up global v2
    tiers = parse_curriculum(RAW)
    t3 = next(t for t in tiers if t.n == 3)
    other_day = next(d for d in t3.days if slugify(d.title) != slug)
    other_slug = slugify(other_day.title)

    other_md = read_text(page_path(tmp_repo, tier_folder=folder, day_slug=other_slug))
    assert "- GLOBAL_V2" in section_body(other_md, "Task")
