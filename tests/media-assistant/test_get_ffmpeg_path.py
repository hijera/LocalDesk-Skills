"""Unit tests for get_ffmpeg_path.py."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = REPO_ROOT / "skills" / "media-assistant" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR.parent))

import importlib.util
_spec = importlib.util.spec_from_file_location(
    "get_ffmpeg_path",
    SCRIPTS_DIR / "get_ffmpeg_path.py"
)
get_ffmpeg_path_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(get_ffmpeg_path_module)

get_ffmpeg_path = get_ffmpeg_path_module.get_ffmpeg_path


def test_get_ffmpeg_path_returns_path_when_imageio_available():
    """When imageio_ffmpeg provides path, returns it."""
    fake_module = MagicMock()
    fake_module.get_ffmpeg_exe = MagicMock(return_value="/fake/path/ffmpeg")

    with patch.dict(sys.modules, {"imageio_ffmpeg": fake_module}):
        result = get_ffmpeg_path()
        assert result == "/fake/path/ffmpeg"
        assert isinstance(result, str)
        assert len(result) > 0


def test_get_ffmpeg_path_returns_system_ffmpeg_when_imageio_unavailable():
    """When imageio_ffmpeg not installed but system ffmpeg exists, returns system path."""
    import builtins
    real_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if name == "imageio_ffmpeg":
            raise ImportError("No module named 'imageio_ffmpeg'")
        return real_import(name, *args, **kwargs)

    with patch("builtins.__import__", side_effect=mock_import):
        with patch("shutil.which", return_value="/usr/bin/ffmpeg"):
            result = get_ffmpeg_path()
            assert result == "/usr/bin/ffmpeg"


def test_get_ffmpeg_path_raises_when_not_found():
    """When no ffmpeg available, raises RuntimeError with pip install hint."""
    import builtins
    real_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if name == "imageio_ffmpeg":
            raise ImportError("No module named 'imageio_ffmpeg'")
        return real_import(name, *args, **kwargs)

    with patch("builtins.__import__", side_effect=mock_import):
        with patch("shutil.which", return_value=None):
            with pytest.raises(RuntimeError) as exc_info:
                get_ffmpeg_path()
            msg = str(exc_info.value)
            assert "pip install imageio-ffmpeg" in msg
            assert "ffmpeg" in msg.lower()
