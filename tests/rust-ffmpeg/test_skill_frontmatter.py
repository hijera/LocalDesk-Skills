"""Tests for SKILL.md YAML frontmatter validation."""

import pytest


class TestSkillFrontmatter:
    """Validate SKILL.md frontmatter structure and required fields."""

    def test_frontmatter_has_name(self, skill_frontmatter: dict) -> None:
        """Frontmatter must contain non-empty name."""
        assert "name" in skill_frontmatter
        assert isinstance(skill_frontmatter["name"], str)
        assert len(skill_frontmatter["name"].strip()) > 0

    def test_frontmatter_name_is_rust_ffmpeg(self, skill_frontmatter: dict) -> None:
        """Skill name must be rust-ffmpeg."""
        assert skill_frontmatter.get("name") == "rust-ffmpeg"

    def test_frontmatter_has_description(self, skill_frontmatter: dict) -> None:
        """Frontmatter must contain non-empty description."""
        assert "description" in skill_frontmatter
        assert isinstance(skill_frontmatter["description"], str)
        assert len(skill_frontmatter["description"].strip()) > 0

    def test_description_length_reasonable(self, skill_frontmatter: dict) -> None:
        """Description should not exceed 4096 characters (Agent Skills spec allows up to 1024 for discovery; rust-ffmpeg uses extended triggers)."""
        desc = skill_frontmatter.get("description", "")
        assert len(desc) < 4096, "Description exceeds 4096 characters"

    def test_frontmatter_has_license(self, skill_frontmatter: dict) -> None:
        """Frontmatter should contain license (MIT)."""
        assert skill_frontmatter.get("license") == "MIT"

    def test_frontmatter_metadata_optional(self, skill_frontmatter: dict) -> None:
        """Metadata (author, version) are optional but should be present if metadata exists."""
        if "metadata" in skill_frontmatter:
            meta = skill_frontmatter["metadata"]
            assert isinstance(meta, dict)
            if "author" in meta:
                assert isinstance(meta["author"], str)
            if "version" in meta:
                assert isinstance(meta["version"], str)
