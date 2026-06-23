# storage.py
# Persistent FSM storage backed by the existing SQLite DB.
# Why: MemoryStorage keeps brief progress only in RAM, so every bot restart
# (systemd Restart=on-failure) wiped it and users mid-brief got silence.
from typing import Any, Dict, Optional

from aiogram.fsm.state import State
from aiogram.fsm.storage.base import BaseStorage, StorageKey

import db


def _key_str(key: StorageKey) -> str:
    return (
        f"{key.bot_id}:{key.chat_id}:{key.user_id}:"
        f"{key.thread_id}:{key.business_connection_id}:{key.destiny}"
    )


class SQLiteStorage(BaseStorage):
    async def set_state(self, key: StorageKey, state=None) -> None:
        value = state.state if isinstance(state, State) else state
        db.fsm_write_state(_key_str(key), value)

    async def get_state(self, key: StorageKey) -> Optional[str]:
        state, _ = db.fsm_read(_key_str(key))
        return state

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        db.fsm_write_data(_key_str(key), data)

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        _, data = db.fsm_read(_key_str(key))
        return data

    async def close(self) -> None:
        pass
