"""Database module for AI Incident Management System.

Provides SQLite database connection and operations.
"""

import os
import sqlite3
from sqlite3 import Error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "incidents.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")


def initialize_database():
    """Create tables if they don't exist."""
    db_exists = os.path.exists(DB_PATH)

    if not db_exists:
        print(f"[DB] Creating new database at {DB_PATH}")
    else:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents'")
        if cursor.fetchone():
            conn.close()
            return
        conn.close()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
        cursor.executescript(schema_sql)

    sample_technicians = [
        (1, "Иван Петров", "ИТ поддръжка"),
        (2, "Мария Иванова", "Мрежи"),
        (3, "Георги Димитров", "Сигурност")
    ]
    for tech in sample_technicians:
        cursor.execute("INSERT INTO technicians (id, name, department) VALUES (?, ?, ?)", tech)

    conn.commit()
    conn.close()
    print("[DB] Database initialized successfully")


def get_connection():
    """Return a new DB connection."""
    try:
        initialize_database()
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"[DB ERROR] {e}")
        return None


def execute(query: str, params=(), commit: bool = True):
    """Execute INSERT/UPDATE/DELETE query."""
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if commit:
            conn.commit()
        lastrowid = cursor.lastrowid
        return lastrowid if lastrowid else True
    except Error as e:
        print(f"[DB EXECUTE ERROR] {e}")
        return None
    finally:
        conn.close()


def fetch_all(query: str, params=()):
    """Fetch all rows for SELECT query."""
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"[DB FETCH_ALL ERROR] {e}")
        return []
    finally:
        conn.close()


def fetch_one(query: str, params=()):
    """Fetch single row for SELECT query."""
    rows = fetch_all(query, params)
    return rows[0] if rows else None