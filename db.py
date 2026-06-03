# db.py
import sqlite3
import json
from datetime import datetime, timedelta
from typing import Optional

_DB_PATH = "vizitka_bot.db"


def init(path: str = None):
    global _DB_PATH
    if path:
        _DB_PATH = path
    _create_tables()


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _create_tables():
    with _conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id         INTEGER NOT NULL UNIQUE,
                username        TEXT,
                segment         TEXT,
                source          TEXT DEFAULT 'vizitka',
                answers         TEXT DEFAULT '{}',
                time_slots      TEXT,
                status          TEXT DEFAULT 'started',
                created_at      TEXT,
                last_active_at  TEXT,
                reminded        INTEGER DEFAULT 0
            )
        """)


def save_lead(user_id: int, username: Optional[str], source: str = "vizitka"):
    now = datetime.utcnow().isoformat()
    with _conn() as conn:
        conn.execute("""
            INSERT INTO leads (user_id, username, source, created_at, last_active_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username       = excluded.username,
                source         = excluded.source,
                status         = 'started',
                answers        = '{}',
                segment        = NULL,
                time_slots     = NULL,
                reminded       = 0,
                last_active_at = excluded.last_active_at
        """, (user_id, username, source, now, now))


def update_lead(user_id: int, **kwargs):
    """Update any subset of columns. Also bumps last_active_at."""
    kwargs["last_active_at"] = datetime.utcnow().isoformat()
    sets = ", ".join(f"{k} = ?" for k in kwargs)
    values = list(kwargs.values()) + [user_id]
    with _conn() as conn:
        conn.execute(f"UPDATE leads SET {sets} WHERE user_id = ?", values)


def get_lead(user_id: int) -> Optional[dict]:
    with _conn() as conn:
        row = conn.execute(
            "SELECT * FROM leads WHERE user_id = ?", (user_id,)
        ).fetchone()
    return dict(row) if row else None


def get_stale_leads(hours: int = 24) -> list[dict]:
    """Leads that are not finished, not yet reminded, inactive for `hours` hours."""
    cutoff = (datetime.utcnow() - timedelta(hours=hours)).isoformat()
    with _conn() as conn:
        rows = conn.execute("""
            SELECT * FROM leads
            WHERE status = 'started'
              AND reminded = 0
              AND last_active_at < ?
        """, (cutoff,)).fetchall()
    return [dict(r) for r in rows]
