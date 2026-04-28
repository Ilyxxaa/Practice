# persistence.py
# This file is responsible for saving and loading game data.
# It works with two JSON files:
# 1) settings.json     -> saves sound, car color, difficulty
# 2) leaderboard.json  -> saves top 10 player results

import json
from pathlib import Path

# BASE_DIR is the folder where this file is located.
# We use it so JSON files are created in the project folder,
# not somewhere random depending on where Python was launched from.
BASE_DIR = Path(__file__).resolve().parent

# Path to the settings file.
SETTINGS_FILE = BASE_DIR / "settings.json"

# Path to the leaderboard file.
LEADERBOARD_FILE = BASE_DIR / "leaderboard.json"

# Default settings used when settings.json does not exist
# or when it is broken / missing some values.
DEFAULT_SETTINGS = {
    "sound": True,          # True means crash sound is enabled
    "car_color": "blue",   # default player car tint color
    "difficulty": "normal"  # default game difficulty
}

# Difficulty settings.
# These values are used inside racer.py to control how hard the game is.
DIFFICULTY = {
    # Easy: slower speed and fewer obstacles / traffic cars
    "easy": {"traffic": 0.008, "obstacles": 0.007, "speed": 4.5},

    # Normal: balanced version
    "normal": {"traffic": 0.012, "obstacles": 0.010, "speed": 5.5},

    # Hard: faster speed and more obstacles / traffic cars
    "hard": {"traffic": 0.018, "obstacles": 0.015, "speed": 6.5}
}


def load_json(path, default):
    """
    Universal JSON loading function.

    path    -> file path to load
    default -> value returned if file does not exist or is broken

    This function is used for both settings.json and leaderboard.json.
    """
    try:
        # Check if file exists before trying to open it.
        if path.exists():
            # Open file with UTF-8 encoding so Russian/English text works correctly.
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

                # Validate type.
                # Example: settings must be dict, leaderboard must be list.
                if isinstance(data, type(default)):
                    return data

    # If JSON is broken or file cannot be read, ignore the error
    # and recreate the file below using default data.
    except (json.JSONDecodeError, OSError):
        pass

    # If file is missing or invalid, create a new file with default data.
    save_json(path, default)

    # Return a copy so DEFAULT_SETTINGS or default list is not modified directly.
    return default.copy() if isinstance(default, dict) else list(default)


def save_json(path, data):
    """
    Universal JSON saving function.

    path -> file path where data will be saved
    data -> Python object to save, usually dict or list
    """
    with open(path, "w", encoding="utf-8") as f:
        # indent=4 makes JSON readable.
        # ensure_ascii=False keeps non-English characters normal.
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_settings():
    """
    Loads game settings from settings.json.
    If some setting is missing, it is added from DEFAULT_SETTINGS.
    """
    settings = load_json(SETTINGS_FILE, DEFAULT_SETTINGS)

    # Add missing settings if the file exists but does not contain all keys.
    for key, value in DEFAULT_SETTINGS.items():
        settings.setdefault(key, value)

    # Validate difficulty.
    # If difficulty has an incorrect value, reset it to normal.
    if settings["difficulty"] not in DIFFICULTY:
        settings["difficulty"] = "normal"

    return settings


def save_settings(settings):
    """
    Saves current settings to settings.json.
    Called when player changes sound, car color, or difficulty.
    """
    save_json(SETTINGS_FILE, settings)


def load_leaderboard():
    """
    Loads leaderboard from leaderboard.json.
    Leaderboard must be a list of results.
    """
    data = load_json(LEADERBOARD_FILE, [])
    return data if isinstance(data, list) else []


def add_score(name, score, distance, coins):
    """
    Adds one new player result to the leaderboard.
    Then sorts all results and keeps only the best 10.
    """
    # Load existing leaderboard first.
    board = load_leaderboard()

    # Add a new result.
    board.append({
        "name": name[:12] or "Player",  # limit username to 12 characters
        "score": int(score),             # final score
        "distance": int(distance),       # distance driven
        "coins": int(coins)              # collected coins
    })

    # Sort by score from highest to lowest.
    board.sort(key=lambda item: item.get("score", 0), reverse=True)

    # Keep only top 10 records.
    board = board[:10]

    # Save updated leaderboard to file.
    save_json(LEADERBOARD_FILE, board)

    return board
