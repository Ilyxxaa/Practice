# TSIS4 Snake Game

Extended Snake game using Pygame and PostgreSQL (`psycopg2`).

## Files

```text
TSIS4/
├── main.py
├── game.py
├── db.py
├── settings_manager.py
├── settings.json
├── config.py
└── assets/
```

## Install

```bash
pip install pygame psycopg2-binary
```

## PostgreSQL setup

Create database:

```sql
CREATE DATABASE snake_db;
```

Then edit `config.py` if your PostgreSQL username/password are different.
Tables are created automatically by `db.py`, but schema is:

```sql
CREATE TABLE players (
    id       SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE game_sessions (
    id            SERIAL PRIMARY KEY,
    player_id     INTEGER REFERENCES players(id),
    score         INTEGER   NOT NULL,
    level_reached INTEGER   NOT NULL,
    played_at     TIMESTAMP DEFAULT NOW()
);
```

## Run

```bash
python main.py
```
