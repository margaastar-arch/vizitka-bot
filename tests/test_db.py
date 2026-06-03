# tests/test_db.py
import pytest
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import db


@pytest.fixture
def tmp_db(tmp_path):
    path = str(tmp_path / "test.db")
    db.init(path)
    return path


def test_save_and_get_lead(tmp_db):
    db.save_lead(123, username="alice", source="vizitka")
    lead = db.get_lead(123)
    assert lead["user_id"] == 123
    assert lead["username"] == "alice"
    assert lead["status"] == "started"
    assert lead["reminded"] == 0


def test_update_lead(tmp_db):
    db.save_lead(456, username="bob", source="vizitka")
    db.update_lead(456, status="hot", time_slots="вт 18:00")
    lead = db.get_lead(456)
    assert lead["status"] == "hot"
    assert lead["time_slots"] == "вт 18:00"


def test_save_lead_upsert(tmp_db):
    db.save_lead(789, username="old", source="vizitka")
    db.save_lead(789, username="new", source="vizitka")
    lead = db.get_lead(789)
    assert lead["username"] == "new"


def test_get_stale_leads_empty(tmp_db):
    db.save_lead(111, username="fresh", source="vizitka")
    stale = db.get_stale_leads(hours=24)
    assert stale == []


def test_get_stale_leads_returns_old(tmp_db):
    import sqlite3
    from datetime import datetime, timedelta
    db.save_lead(222, username="old_user", source="vizitka")
    old_time = (datetime.utcnow() - timedelta(hours=25)).isoformat()
    conn = sqlite3.connect(tmp_db)
    conn.execute(
        "UPDATE leads SET last_active_at = ? WHERE user_id = ?",
        (old_time, 222)
    )
    conn.commit()
    conn.close()
    stale = db.get_stale_leads(hours=24)
    assert len(stale) == 1
    assert stale[0]["user_id"] == 222
