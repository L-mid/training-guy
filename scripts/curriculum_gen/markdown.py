from __future__ import annotations

import json
import re
from typing import Any


def normalize_newlines(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n")


def find_frontmatter_block(md: str) -> tuple[str | None, str]:
    """
    If md begins with a YAML frontmatter block, return (frontmatter, body).
    Otherwise return (None, md).
    """
    md = normalize_newlines(md)
    if not md.startswith("---\n"):
        return None, md

    end = md.find("\n---\n", 4)
    if end == -1:
        return None, md

    fm = md[: end + len("\n---\n")]
    body = md[end + len("\n---\n") :]
    return fm, body


def upsert_frontmatter(
    existing: str,
    *,
    title: str,
    sidebar_label: str,
    sidebar_position: int,
) -> str:
    """
    Ensure title/sidebar_label/sidebar_position exist and are deterministic.

    Integration notes:
    - Preserves any other frontmatter keys already present.
    - Leaves body content intact.
    """
    fm, body = find_frontmatter_block(existing)

    keep_lines: list[str] = []
    if fm is not None:
        lines = fm.splitlines()
        for ln in lines[1:-1]:
            if re.match(r"^(title|sidebar_label|sidebar_position):", ln.strip()):
                continue
            keep_lines.append(ln)

    title_q = json.dumps(title, ensure_ascii=False)
    label_q = json.dumps(sidebar_label, ensure_ascii=False)

    new_fm_lines = [
        "---",
        f"title: {title_q}",
        f"sidebar_label: {label_q}",
        f"sidebar_position: {sidebar_position}",
        *keep_lines,
        "---",
    ]

    body = body.lstrip("\n")
    return "\n".join(new_fm_lines) + "\n\n" + body


def section_regex(header: str) -> re.Pattern[str]:
    escaped = re.escape(header)
    return re.compile(rf"(?ms)(^##\s+{escaped}\s*\n)(.*?)(?=^##\s+|\Z)")


def remove_section(md: str, header: str) -> str:
    rgx = section_regex(header)
    if not rgx.search(md):
        return md
    md = rgx.sub("", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip("\n") + "\n"


def replace_or_append_section(md: str, header: str, new_section_body: str) -> str:
    """
    Replace the content of a "## Header" section, or append it if missing.

    new_section_body should include leading/trailing newlines (use section_body_from_lines).
    """
    rgx = section_regex(header)
    if rgx.search(md):
        return rgx.sub(rf"\1{new_section_body}", md)

    return md.rstrip() + "\n\n" + f"## {header}\n" + new_section_body


def section_body_from_lines(lines: list[str]) -> str:
    """
    Render a section body with consistent spacing:
    - blank line after header
    - content
    - blank line after content
    """
    return "\n" + "\n".join(lines).rstrip() + "\n\n"


def render_bullets(items: list[str]) -> list[str]:
    return [f"- {x}" for x in items]


def render_checklist(items: list[str]) -> list[str]:
    return [f"- [ ] {x}" for x in items]


def render_docs_links(links: list[Any]) -> list[str]:
    """
    Accepts:
      - {"label": str, "url": str}
      - [label, url] / (label, url)
    Returns markdown list lines.
    """
    out: list[str] = []
    for it in links:
        if isinstance(it, dict):
            label = it.get("label")
            url = it.get("url")
        else:
            label, url = it
        out.append(f"- [{label}]({url})")
    return out