from __future__ import annotations

from pathlib import Path

from scripts.curriculum_gen.generator import generate

from ._util import page_path, read_text, section_body, write_json


def test_global_defaults_apply_everywhere(tmp_repo: Path, tier_index) -> None:
    """
    Verifies:
    - global defaults apply everywhere
    - docs section exists (either config docs_links or fallback links_for_tier)
    """
    write_json(
        tmp_repo / "curriculum_config" / "global.json",
        {
            "defaults": {
                "task": ["__GLOBAL_TASK_SENTINEL__"],
                "checklist": ["A", "B"],
                "hints_block": {"enabled": False},
            }
        },
    )

    generate(repo_root=tmp_repo)

    for tier_n in range(1, 11):
        slug = tier_index.tier_to_first_day_slug[tier_n]
        folder = tier_index.tier_to_folder[tier_n]
        md = read_text(page_path(tmp_repo, tier_folder=folder, day_slug=slug))

        assert "- __GLOBAL_TASK_SENTINEL__" in section_body(md, "Task")
        assert section_body(md, "Docs / Tutorials"), f"Docs section missing for tier {tier_n}"


def test_fallback_docs_links_vary_by_tier(tmp_repo: Path, tier_index) -> None:
    """
    Spot-check fallback docs link labels (proves links_for_tier wiring works).
    """
    # Ensure global doesn't override docs_links; we want fallbacks.
    write_json(
        tmp_repo / "curriculum_config" / "global.json",
        {"defaults": {"task": ["X"], "hints_block": {"enabled": False}}},
    )

    generate(repo_root=tmp_repo)

    # Tier 1 should include Python Tutorial fallback
    slug1 = tier_index.tier_to_first_day_slug[1]
    folder1 = tier_index.tier_to_folder[1]
    md1 = read_text(page_path(tmp_repo, tier_folder=folder1, day_slug=slug1))
    assert "[Python Tutorial]" in section_body(md1, "Docs / Tutorials")

    # Tier 5 should include Git Reference fallback
    slug5 = tier_index.tier_to_first_day_slug[5]
    folder5 = tier_index.tier_to_folder[5]
    md5 = read_text(page_path(tmp_repo, tier_folder=folder5, day_slug=slug5))
    assert "[Git Reference]" in section_body(md5, "Docs / Tutorials")
