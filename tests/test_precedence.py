from __future__ import annotations

import json
from pathlib import Path

from scripts.curriculum_gen.generator import generate

from ._util import page_path, read_text, section_body, write_json


def test_tier_defaults_override_global(tmp_repo: Path, tier_index) -> None:
    """
    Verifies precedence: global < tier_defaults < file_overrides
    Here: tier_defaults should override global.
    """
    write_json(
        tmp_repo / "curriculum_config" / "global.json",
        {"defaults": {"task": ["GLOBAL"], "checklist": ["C"], "hints_block": {"enabled": False}}},
    )

    # Make tier-02 override task
    tier2_path = tmp_repo / "curriculum_config" / "tier-02.json"
    tier2 = json.loads(read_text(tier2_path))
    tier2.setdefault("tier_defaults", {})["task"] = ["TIER2"]
    write_json(tier2_path, tier2)

    generate(repo_root=tmp_repo)

    slug = tier_index.tier_to_first_day_slug[2]
    folder = tier_index.tier_to_folder[2]
    md = read_text(page_path(tmp_repo, tier_folder=folder, day_slug=slug))

    task = section_body(md, "Task")
    assert "- TIER2" in task
    assert "- GLOBAL" not in task
