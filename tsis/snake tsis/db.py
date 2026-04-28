# db.py
# This file contains all PostgreSQL work.
# The game imports these functions to save scores, load leaderboard,
# and show personal best scores.

import psycopg2
from psycopg2 import sql
from config import DB_CONFIG, SCHEMA_SQL


def get_connection():
    """
    Opens a connection to PostgreSQL using settings from config.py.
    If connection fails, the caller handles the error and the game still runs.
    """
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    """
    Creates required database tables if they do not exist.
    Tables:
    - players
    - game_sessions
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(SCHEMA_SQL)
            conn.commit()
        return True
    except Exception as e:
        print("Database initialization failed:", e)
        return False


def get_or_create_player(username):
    """
    Finds a player by username.
    If the player does not exist, creates a new record.
    Returns player_id or None if database is unavailable.
    """
    username = (username or "Player")[:50]
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM players WHERE username = %s", (username,))
                row = cur.fetchone()
                if row:
                    return row[0]

                cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
                player_id = cur.fetchone()[0]
                conn.commit()
                return player_id
    except Exception as e:
        print("get_or_create_player failed:", e)
        return None


def save_game_result(username, score, level_reached):
    """
    Saves finished game result to PostgreSQL.
    Stores username, score, level and timestamp.
    """
    player_id = get_or_create_player(username)
    if player_id is None:
        return False

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO game_sessions (player_id, score, level_reached)
                    VALUES (%s, %s, %s)
                    """,
                    (player_id, int(score), int(level_reached)),
                )
            conn.commit()
        return True
    except Exception as e:
        print("save_game_result failed:", e)
        return False


def get_leaderboard(limit=10):
    """
    Loads Top 10 all-time scores from PostgreSQL.
    Returns list of tuples: username, score, level, date.
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT p.username, g.score, g.level_reached, g.played_at
                    FROM game_sessions g
                    JOIN players p ON p.id = g.player_id
                    ORDER BY g.score DESC, g.level_reached DESC, g.played_at ASC
                    LIMIT %s
                    """,
                    (limit,),
                )
                return cur.fetchall()
    except Exception as e:
        print("get_leaderboard failed:", e)
        return []


def get_personal_best(username):
    """
    Loads personal best score for selected username.
    If player has no results, returns 0.
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT COALESCE(MAX(g.score), 0)
                    FROM game_sessions g
                    JOIN players p ON p.id = g.player_id
                    WHERE p.username = %s
                    """,
                    ((username or "Player")[:50],),
                )
                row = cur.fetchone()
                return int(row[0] or 0)
    except Exception as e:
        print("get_personal_best failed:", e)
        return 0
