"""Validation tests for media-assistant SKILL.md."""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SKILL_MD = REPO_ROOT / "skills" / "media-assistant" / "SKILL.md"


def test_skill_md_exists():
    """SKILL.md file exists."""
    assert SKILL_MD.exists(), f"SKILL.md not found at {SKILL_MD}"


def test_skill_md_has_valid_frontmatter():
    """SKILL.md has valid YAML frontmatter with required fields."""
    content = SKILL_MD.read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---", content)
    assert match, "SKILL.md must have YAML frontmatter between --- delimiters"

    frontmatter = match.group(1)
    assert "name:" in frontmatter, "Frontmatter must contain 'name'"
    assert "description:" in frontmatter, "Frontmatter must contain 'description'"


def test_skill_name_matches():
    """Skill name is media-assistant and matches directory."""
    content = SKILL_MD.read_text(encoding="utf-8")
    match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
    assert match, "Could not find name field"
    name = match.group(1).strip().strip("'\"")
    assert name == "media-assistant", f"Expected name 'media-assistant', got '{name}'"


def test_skill_description_non_empty():
    """Skill description is non-empty."""
    content = SKILL_MD.read_text(encoding="utf-8")
    match = re.search(r"^description:\s*(.+)$", content, re.MULTILINE)
    assert match, "Could not find description field"
    desc = match.group(1).strip().strip("'\"")
    assert len(desc) > 0, "Description must not be empty"
    assert len(desc) <= 1024, "Description must be max 1024 characters"


def test_skill_name_format():
    """Skill name follows spec: lowercase, hyphens, no consecutive hyphens."""
    content = SKILL_MD.read_text(encoding="utf-8")
    match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
    assert match
    name = match.group(1).strip().strip("'\"")
    assert name == name.lower(), "Name must be lowercase"
    assert "--" not in name, "Name must not contain consecutive hyphens"
    assert not name.startswith("-"), "Name must not start with hyphen"
    assert not name.endswith("-"), "Name must not end with hyphen"
    assert re.match(r"^[a-z0-9\-]+$", name), "Name must contain only a-z, 0-9, hyphens"
