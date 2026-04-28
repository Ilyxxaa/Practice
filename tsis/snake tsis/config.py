# config.py
# This file stores constants used by the Snake project.
# You can change database settings here before running the game.

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = GRID_WIDTH * CELL_SIZE
HEIGHT = GRID_HEIGHT * CELL_SIZE

FPS_START = 8
LEVEL_UP_EVERY = 4

# PostgreSQL connection settings.
# Change these values to match your local PostgreSQL database.
DB_CONFIG = {
    "host": "localhost",
    "database": "snake_db",
    "user": "postgres",
    "password": "27082007",
    "port": 5432,
}

# SQL schema required for the task.
# This is also used automatically by db.py to create tables if they do not exist.
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS players (
    id       SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS game_sessions (
    id            SERIAL PRIMARY KEY,
    player_id     INTEGER REFERENCES players(id),
    score         INTEGER   NOT NULL,
    level_reached INTEGER   NOT NULL,
    played_at     TIMESTAMP DEFAULT NOW()
);
"""
