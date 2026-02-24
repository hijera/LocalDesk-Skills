"""Pytest fixtures for rust-ffmpeg skill tests."""

from pathlib import Path

import pytest


@pytest.fixture
def skill_root() -> Path:
    """Return the absolute path to the rust-ffmpeg skill directory."""
    # conftest.py is in tests/rust-ffmpeg/; repo root is tests/../; skill is skills/rust-ffmpeg/
    repo_root = Path(__file__).resolve().parent.parent.parent
    return repo_root / "skills" / "rust-ffmpeg"


@pytest.fixture
def skill_md_content(skill_root: Path) -> str:
    """Return the raw content of SKILL.md."""
    skill_md = skill_root / "SKILL.md"
    return skill_md.read_text(encoding="utf-8")


@pytest.fixture
def skill_frontmatter(skill_md_content: str) -> dict:
    """Parse and return the YAML frontmatter from SKILL.md."""
    import yaml

    if not skill_md_content.strip().startswith("---"):
        return {}
    parts = skill_md_content.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}
