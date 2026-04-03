import psycopg2
from config import db_config

def connect():
    return psycopg2.connect(**db_config)