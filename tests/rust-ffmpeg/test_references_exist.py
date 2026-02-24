"""Tests that all referenced files from SKILL.md exist."""

from pathlib import Path

import pytest

# Explicit list of files referenced in SKILL.md (Layer 2, Library References, Quick Start, Installation, etc.)
EXPECTED_REFERENCES = [
    "references/ffmpeg_sidecar.md",
    "references/scenarios/video_transcoding.md",
    "references/scenarios/audio_extraction.md",
    "references/scenarios/transcoding.md",
    "references/scenarios/streaming_rtmp_hls.md",
    "references/scenarios/hardware_acceleration.md",
    "references/scenarios/batch_processing.md",
    "references/scenarios/subtitles.md",
    "references/scenarios/modern_codecs.md",
    "references/scenarios/debugging.md",
    "references/scenarios/filters_effects.md",
    "references/scenarios/image_sequences.md",
    "references/scenarios/testing.md",
    "references/scenarios/integration.md",
    "references/scenarios/gif_creation.md",
    "references/scenarios/metadata_chapters.md",
    "references/scenarios/capture.md",
    "references/ffmpeg_next.md",
    "references/ffmpeg_sys_next.md",
    "references/ffmpeg_sys_next/custom_io.md",
    "references/library_selection.md",
    "references/ez_ffmpeg/cli_migration.md",
    "references/quick_start.md",
    "references/ez_ffmpeg.md",
    "references/ffmpeg_next.md",
    "references/ffmpeg_sys_next.md",
    "references/installation.md",
]


class TestReferencesExist:
    """Verify all files referenced in SKILL.md exist."""

    def test_all_expected_references_exist(self, skill_root: Path) -> None:
        """Each file in the expected references list must exist under skill root."""
        missing = []
        for rel_path in sorted(set(EXPECTED_REFERENCES)):
            full_path = skill_root / rel_path
            if not full_path.exists():
                missing.append(rel_path)
        if missing:
            pytest.fail("Missing referenced files:\n  " + "\n  ".join(missing))
