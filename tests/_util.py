from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def write_json(path: Path, obj: Any) -> None:
    """Write JSON with stable formatting for tests."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def read_text(path: Path) -> str:
    """Read UTF-8 text (convenience)."""
    return path.read_text(encoding="utf-8")


def section_body(md: str, header: str) -> str:
    """
    Extract the body under '## {header}' up to the next '##' header (or EOF).
    Returns '' if missing.
    """
    rgx = re.compile(rf"(?ms)^##\s+{re.escape(header)}\s*\n(.*?)(?=^##\s+|\Z)")
    m = rgx.search(md)
    return m.group(1).strip() if m else ""


def page_path(repo_root: Path, *, tier_folder: str, day_slug: str) -> Path:
    """Path to a day markdown file under docs/curriculum/<tier-folder>/<slug>.md"""
    return repo_root / "docs" / "curriculum" / tier_folder / f"{day_slug}.md"
