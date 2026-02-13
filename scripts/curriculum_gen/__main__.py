from __future__ import annotations

from pathlib import Path

from .generator import generate


def main() -> None:
    """
    CLI entrypoint.

    Assumes this package lives somewhere under your repo and that:
      repo_root/
        docs/
        curriculum_config/
    """
    repo_root = Path(__file__).resolve().parents[2]
    out = generate(repo_root=repo_root)
    print(f"Generated curriculum at: {out}")


if __name__ == "__main__":
    main()