import psycopg2
from config import db_config


def connect():
    """
    Creates and returns a PostgreSQL connection.
    All files use this function, so DB settings stay in one place: config.py.
    """
    return psycopg2.connect(**db_config)
