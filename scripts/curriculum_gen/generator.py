from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .config import load_global_defaults, load_site_config, load_tier_config, merge_section
from .links import links_for_tier
from .markdown import (
    normalize_newlines,
    remove_section,
    render_bullets,
    render_checklist,
    render_docs_links,
    replace_or_append_section,
    section_body_from_lines,
    upsert_frontmatter,
)
from .parsing import parse_curriculum, slugify
from .raw_curriculum import RAW


def write_file(path: Path, text: str) -> None:
    """Atomic-enough for docs generation: ensure parent exists then write UTF-8."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def generate(*, repo_root: Path) -> Path:
    """
    Generate/refresh curriculum docs under {repo_root}/docs/curriculum.

    Integration contract (filesystem):
      - reads RAW (baked-in)
      - reads config from {repo_root}/curriculum_config/
          - global.json (optional)
          - tier-XX.json (optional)
      - writes docs to {repo_root}/docs/curriculum/

    Returns:
        Path to the docs_root folder.
    """
    docs_root = repo_root / "docs" / "curriculum"
    config_root = repo_root / "curriculum_config"

    tiers = parse_curriculum(RAW)
    global_defaults = load_global_defaults(config_root)
    site_cfg = load_site_config(config_root)
    max_public_tier = site_cfg.get("max_tier")

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

    landing = [
        "# Curriculum\n",
        "\n",
        "Difficulty:\n",
        "- ! 💚 Easy !\n",
        "- ! 💛 Medium !\n",
        "- ! ❤️‍🔥 Hard !\n",
        "- ! 💜 Boss !\n",
        "\n",
        "Unlock the next tier by completing all the units!\n",
        "\n",
        "## Tiers\n",
    ]

    available = 0
    locked = 0

    for t in tiers:
        tier_folder = f"tier-{t.n:02d}-{slugify(t.name)}"

        is_public = not isinstance(max_public_tier, int) or t.n <= max_public_tier
        if is_public:
            available += 1
            landing.append(f"- ✅ [TIER {t.n} — {t.name}](/curriculum/{tier_folder})\n")

    landing.insert(
        landing.index("## Tiers\n"),
        f"\n**Available now:** {available} tier(s)"
        + (f" • **Locked:** {locked}" if locked else "")
        + "\n",
    )

    write_file(docs_root / "index.mdx", "".join(landing) + "\n")
        
    # Tiers + days
    for t in tiers:
        tier_cfg = load_tier_config(config_root, t.n)
        tier_defaults: dict[str, Any] = tier_cfg["tier_defaults"]
        file_overrides: dict[str, Any] = tier_cfg["files"]

        expected_slugs = {slugify(d.title) for d in t.days}
        extra = set(file_overrides.keys()) - expected_slugs
        if extra:
            raise ValueError(
                f"{config_root / f'tier-{t.n:02d}.json'} contains unknown slugs: {sorted(extra)}"
            )

        tier_folder = docs_root / f"tier-{t.n:02d}-{slugify(t.name)}"
        tier_index_slug = f"/curriculum/{tier_folder.name}"

        write_file(
            tier_folder / "_category_.json",
            json.dumps(
                {
                    "label": f"TIER {t.n} — {t.name}",
                    "position": t.n,
                    "link": {
                        "type": "generated-index",
                        "slug": tier_index_slug,
                        "title": f"TIER {t.n} — {t.name}",
                        "description": "Do tasks → do boss.",
                    },
                },
                indent=2,
            )
            + "\n",
        )

        for i, d in enumerate(t.days, start=1):
            slug = slugify(d.title)
            filename = f"{slug}.md"

            sidebar_label = f"{d.emoji} {d.title}"
            title = f"{d.emoji} — {d.title}"

            effective = merge_section(global_defaults, tier_defaults)
            effective = merge_section(effective, file_overrides.get(slug, {}))

            # If a block is None or an empty list, we treat it as "do not render".
            task = effective.get("task")
            checklist = effective.get(
                "checklist",
                ["Works", "Cleaned up", "(Optional) 1 upgrade / stretch"],
            )

            example_run = effective.get("example_run")
            solution_block = effective.get("solution_block")

            hints_block = effective.get("hints_block", {})
            hints_enabled = bool(hints_block.get("enabled", False))
            hints = effective.get("hints", []) if hints_enabled else []

            if "docs_links" in effective:
                docs_links = effective["docs_links"]
            else:
                docs_links = links_for_tier(t.n)

            path = tier_folder / filename
            existing = path.read_text(encoding="utf-8") if path.exists() else ""
            existing = normalize_newlines(existing)

            md = upsert_frontmatter(
                existing,
                title=title,
                sidebar_label=sidebar_label,
                sidebar_position=i,
            )

            # Task / Checklist are optional: if they resolve to empty/None, remove the section entirely.
            if isinstance(task, list) and any(x.strip() for x in task):
                md = replace_or_append_section(md, "Task", section_body_from_lines(render_bullets(task)))
            else:
                md = remove_section(md, "Task")

            if isinstance(checklist, list) and any(x.strip() for x in checklist):
                md = replace_or_append_section(
                    md, "Checklist", section_body_from_lines(render_checklist(checklist))
                )
            else:
                md = remove_section(md, "Checklist")

            if hints_enabled:
                md = replace_or_append_section(md, "Hints", section_body_from_lines(render_bullets(hints)))
            else:
                md = remove_section(md, "Hints")

            # Example run (raw markdown lines; not forced into bullets)
            if isinstance(example_run, list) and any(x.strip() for x in example_run):
                md = replace_or_append_section(md, "Example run", section_body_from_lines(example_run))
            else:
                md = remove_section(md, "Example run")

            # Solution (spoiler)
            if isinstance(solution_block, dict) and solution_block.get("enabled", True):
                summary = solution_block.get("summary") or "Show solution"
                language = solution_block.get("language") or "python"
                filename = solution_block.get("filename")
                text_lines = solution_block.get("text") or []
                code_lines = solution_block.get("code") or []

                body_lines: list[str] = []
                body_lines.append("<details>")
                body_lines.append(f"  <summary>{summary}</summary>")
                body_lines.append("")

                # Optional text block inside the spoiler
                if isinstance(text_lines, list) and any(x.strip() for x in text_lines):
                    body_lines.extend(text_lines)
                    body_lines.append("")

                if isinstance(code_lines, list) and any(x.strip() for x in code_lines):
                    if isinstance(filename, str) and filename.strip():
                        body_lines.append(f"```{language} title=\"{filename.strip()}\"")
                    else:
                        body_lines.append(f"```{language}")
                    body_lines.extend(code_lines)
                    body_lines.append("```")

                body_lines.append("")
                body_lines.append("</details>")

                # Only render if there's *something* inside.
                if len(body_lines) > 5:
                    md = replace_or_append_section(md, "Solution (ATTEMPT FIRST)", section_body_from_lines(body_lines))
                else:
                    md = remove_section(md, "Solution (ATTEMPT FIRST)")
            else:
                md = remove_section(md, "Solution (ATTEMPT FIRST)")

            if docs_links:
                md = replace_or_append_section(
                    md, "Docs / Tutorials", section_body_from_lines(render_docs_links(docs_links))
                )
            else:
                md = remove_section(md, "Docs / Tutorials")

            # Final formatting pass: prevent runaway blank lines from accumulating
            # after multiple generations.
            md = re.sub(r"\n{3,}", "\n\n", md).strip("\n") + "\n"
            write_file(path, md)

    return docs_root