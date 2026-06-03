# config.py
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.environ["BOT_TOKEN"]
MARGA_CHAT_ID: int = int(os.environ["MARGA_CHAT_ID"])
DB_PATH: str = os.getenv("DB_PATH", "vizitka_bot.db")
