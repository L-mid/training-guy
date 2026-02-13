from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


"""
Config schema (JSON)

curriculum_config/global.json
{
  "defaults": {
    "task": ["..."],
    "checklist": ["..."],
    "hints": ["..."],
    "docs_links": [{"label": "...", "url": "..."}],
    "hints_block": {"enabled": true},

    // optional additive list semantics:
    "task_append": ["..."],
    "checklist_append": ["..."],
    "hints_append": ["..."],
    "docs_links_append": [{"label": "...", "url": "..."}]
  }
}

curriculum_config/tier-XX.json
{
  "tier_defaults": { ...same shape as defaults... },
  "files": {
    "<day-slug>": { ...same shape as defaults... }
  }
}

Merge semantics:
- dicts deep-merge
- lists replace
- *_append keys append onto the base list (after deep-copy)
"""


_ALLOWED_TIER_ROOT_KEYS = {"tier_defaults", "files"}
_ALLOWED_GLOBAL_ROOT_KEYS = {"defaults", "site"}

_ALLOWED_SITE_KEYS = {"max_tier"}

_ALLOWED_SECTION_KEYS = {
    "task",
    "checklist",
    "hints",
    "docs_links",
    "hints_block",
    "task_append",
    "checklist_append",
    "hints_append",
    "docs_links_append",
}


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"Bad JSON in {path}") from e


def _validate_section_obj(obj: dict[str, Any], ctx: str) -> None:
    extra = set(obj.keys()) - _ALLOWED_SECTION_KEYS
    if extra:
        raise ValueError(f"Unknown keys in {ctx}: {sorted(extra)}")

    for k in ("task", "task_append", "checklist", "checklist_append", "hints", "hints_append"):
        if k in obj and obj[k] is not None:
            if not isinstance(obj[k], list) or not all(isinstance(x, str) for x in obj[k]):
                raise ValueError(f"{ctx}.{k} must be a list[str]")

    for k in ("docs_links", "docs_links_append"):
        if k in obj and obj[k] is not None:
            if not isinstance(obj[k], list):
                raise ValueError(f"{ctx}.{k} must be a list")
            for i, it in enumerate(obj[k]):
                if isinstance(it, dict):
                    if not isinstance(it.get("label"), str) or not isinstance(it.get("url"), str):
                        raise ValueError(f"{ctx}.{k}[{i}] must have str label/url")
                elif isinstance(it, (list, tuple)):
                    if len(it) != 2 or not isinstance(it[0], str) or not isinstance(it[1], str):
                        raise ValueError(f"{ctx}.{k}[{i}] must be [label, url]")
                else:
                    raise ValueError(f"{ctx}.{k}[{i}] must be an object with label/url")

    if "hints_block" in obj and obj["hints_block"] is not None:
        hb = obj["hints_block"]
        if not isinstance(hb, dict):
            raise ValueError(f"{ctx}.hints_block must be an object")
        if "enabled" in hb and not isinstance(hb["enabled"], bool):
            raise ValueError(f"{ctx}.hints_block.enabled must be a bool")


def _validate_site_obj(obj: dict[str, Any], ctx: str) -> None:
    extra = set(obj.keys()) - _ALLOWED_SITE_KEYS
    if extra:
        raise ValueError(f"Unknown keys in {ctx}: {sorted(extra)}")

    if "max_tier" in obj and obj["max_tier"] is not None:
        mt = obj["max_tier"]
        if not isinstance(mt, int) or mt < 1:
            raise ValueError(f"{ctx}.max_tier must be an int >= 1")


def merge_section(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """
    Deep-merge dicts.
    - dict + dict merges recursively
    - lists replace
    - supports *_append keys to append list items
    """
    out = copy.deepcopy(base)

    # handle *_append first
    for k, v in override.items():
        if not k.endswith("_append"):
            continue
        target = k[: -len("_append")]
        if v is None:
            continue
        prev = out.get(target)
        if prev is None:
            prev = []
        if not isinstance(prev, list) or not isinstance(v, list):
            raise ValueError(f"Cannot append non-lists via {k}")
        out[target] = prev + v

    # normal override/deep merge
    for k, v in override.items():
        if k.endswith("_append"):
            continue
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = merge_section(out[k], v)  # type: ignore[arg-type]
        else:
            out[k] = copy.deepcopy(v)

    return out


def load_global_defaults(config_root: Path) -> dict[str, Any]:
    """
    Load curriculum_config/global.json defaults.

    Returns the inner "defaults" object (validated), or {} if missing.
    """
    cfg = _read_json(config_root / "global.json")
    if not cfg:
        return {}

    extra = set(cfg.keys()) - _ALLOWED_GLOBAL_ROOT_KEYS
    if extra:
        raise ValueError(f"Unknown keys in global.json: {sorted(extra)}")

    defaults = cfg.get("defaults", {})
    if not isinstance(defaults, dict):
        raise ValueError("global.json.defaults must be an object")

    _validate_section_obj(defaults, "global.json.defaults")
    return defaults


def load_site_config(config_root: Path) -> dict[str, Any]:
    """Load curriculum_config/global.json site settings.

    Returns the inner "site" object (validated), or {} if missing.

    Supported keys:
      - max_tier: int >= 1
    """
    cfg = _read_json(config_root / "global.json")
    if not cfg:
        return {}

    extra = set(cfg.keys()) - _ALLOWED_GLOBAL_ROOT_KEYS
    if extra:
        raise ValueError(f"Unknown keys in global.json: {sorted(extra)}")

    site = cfg.get("site", {})
    if site is None:
        return {}
    if not isinstance(site, dict):
        raise ValueError("global.json.site must be an object")

    _validate_site_obj(site, "global.json.site")
    return site


def load_tier_config(config_root: Path, tier_n: int) -> dict[str, Any]:
    """
    Load curriculum_config/tier-XX.json for the given tier.

    Returns:
      {"tier_defaults": dict, "files": dict}
    """
    path = config_root / f"tier-{tier_n:02d}.json"
    cfg = _read_json(path)
    if not cfg:
        return {"tier_defaults": {}, "files": {}}

    extra = set(cfg.keys()) - _ALLOWED_TIER_ROOT_KEYS
    if extra:
        raise ValueError(f"Unknown keys in {path.name}: {sorted(extra)}")

    tier_defaults = cfg.get("tier_defaults", {})
    files = cfg.get("files", {})

    if not isinstance(tier_defaults, dict):
        raise ValueError(f"{path.name}.tier_defaults must be an object")
    if not isinstance(files, dict):
        raise ValueError(f"{path.name}.files must be an object")

    _validate_section_obj(tier_defaults, f"{path.name}.tier_defaults")

    for slug, overrides in files.items():
        if not isinstance(slug, str):
            raise ValueError(f"{path.name}.files keys must be strings")
        if not isinstance(overrides, dict):
            raise ValueError(f"{path.name}.files[{slug}] must be an object")
        _validate_section_obj(overrides, f"{path.name}.files[{slug}]")

    return {"tier_defaults": tier_defaults, "files": files}
