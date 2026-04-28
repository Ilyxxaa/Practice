# settings_manager.py
# Local JSON settings for the Snake game.
# This file uses only Python built-in json module.

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SETTINGS_FILE = BASE_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "snake_color": [0, 180, 0],
    "grid": True,
    "sound": True,
}


def load_settings():
    """
    Loads settings from settings.json.
    If file is missing or broken, creates it with default values.
    """
    try:
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                for key, value in DEFAULT_SETTINGS.items():
                    data.setdefault(key, value)
                return data
    except (json.JSONDecodeError, OSError):
        pass

    save_settings(DEFAULT_SETTINGS)
    return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    """
    Saves settings to settings.json.
    """
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)
