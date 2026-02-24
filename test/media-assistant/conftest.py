"""Pytest fixtures for media-assistant skill tests."""

import sys
from pathlib import Path

# Add skill scripts to path for imports
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SKILL_SCRIPTS = REPO_ROOT / "skills" / "media-assistant" / "scripts"
SKILL_MD = REPO_ROOT / "skills" / "media-assistant" / "SKILL.md"

if SKILL_SCRIPTS.exists() and str(SKILL_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SKILL_SCRIPTS.parent))
