#!/usr/bin/env python3
"""
Get path to ffmpeg executable.

Tries imageio-ffmpeg first (bundled binary), then falls back to system ffmpeg.
Use this when you need to run ffmpeg via subprocess or run_command.

Usage:
    python scripts/get_ffmpeg_path.py

Output: path to ffmpeg executable, or error message to stderr with exit code 1.

If ffmpeg is not found, suggests: pip install imageio-ffmpeg
"""

import sys


def get_ffmpeg_path() -> str:
    """
    Return path to ffmpeg executable.

    Priority:
    1. imageio-ffmpeg (pip install imageio-ffmpeg)
    2. System ffmpeg (ffmpeg in PATH)

    Returns:
        Path to ffmpeg executable.

    Raises:
        RuntimeError: If no ffmpeg found.
    """
    # Try imageio-ffmpeg first
    try:
        from imageio_ffmpeg import get_ffmpeg_exe
        path = get_ffmpeg_exe()
        if path:
            return path
    except ImportError:
        pass

    # Fallback: check system ffmpeg
    import shutil
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg

    raise RuntimeError(
        "FFmpeg not found. Install with: pip install imageio-ffmpeg\n"
        "Or install ffmpeg system-wide: https://ffmpeg.org/download.html"
    )


def main() -> int:
    try:
        path = get_ffmpeg_path()
        print(path)
        return 0
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
