"""Tests for internal markdown link integrity in rust-ffmpeg skill."""

import re
from pathlib import Path

import pytest

# Match [text](path) or [text](path#anchor); capture path (without anchor)
LINK_PATTERN = re.compile(r"\[([^\]]*)\]\(([^\)#]+)(?:#.*)?\)")


def _extract_internal_links(content: str, base_dir: Path) -> list[tuple[str, Path]]:
    """Extract relative/internal links from markdown content. Returns list of (raw_path, resolved_path)."""
    links = []
    for match in LINK_PATTERN.finditer(content):
        raw_path = match.group(2).strip()
        if not raw_path:
            continue
        if raw_path.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (base_dir / raw_path).resolve()
        links.append((raw_path, resolved))
    return links


def _collect_all_md_files(skill_root: Path) -> list[Path]:
    """Collect all .md files in the skill (SKILL.md + references/**/*.md)."""
    files = []
    if (skill_root / "SKILL.md").exists():
        files.append(skill_root / "SKILL.md")
    refs = skill_root / "references"
    if refs.exists():
        files.extend(refs.rglob("*.md"))
    return files


def _find_broken_links(skill_root: Path) -> list[tuple[Path, str, Path]]:
    """Return list of (source_file, raw_link, resolved_path) for broken links."""
    broken = []
    for md_file in _collect_all_md_files(skill_root):
        content = md_file.read_text(encoding="utf-8")
        base_dir = md_file.parent
        for raw_path, resolved in _extract_internal_links(content, base_dir):
            if not resolved.exists():
                broken.append((md_file, raw_path, resolved))
    return broken


class TestInternalLinks:
    """Verify all internal markdown links resolve to existing files."""

    def test_no_broken_links(self, skill_root: Path) -> None:
        """All internal links in SKILL.md and references/*.md must resolve to existing files."""
        broken = _find_broken_links(skill_root)
        if broken:
            lines = []
            for src, raw, resolved in broken:
                rel_src = src.relative_to(skill_root)
                lines.append(f"  {rel_src}: {raw} -> {resolved} (not found)")
            pytest.fail("Broken internal links:\n" + "\n".join(lines))
