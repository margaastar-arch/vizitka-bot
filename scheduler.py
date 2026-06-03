# scheduler.py
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
import db

logger = logging.getLogger(__name__)


async def check_stale_leads(bot: Bot):
    """Send one reminder to users who went silent for 24h. Run hourly."""
    stale = db.get_stale_leads(hours=24)
    for lead in stale:
        try:
            await bot.send_message(
                lead["user_id"],
                "Хотели рассказать о своём проекте, но что-то отвлекло? "
                "Напишите /start — я здесь.",
            )
            db.update_lead(lead["user_id"], reminded=1)
        except Exception as e:
            logger.warning("Failed to remind user %s: %s", lead["user_id"], e)


def create_scheduler(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        check_stale_leads,
        trigger="interval",
        hours=1,
        kwargs={"bot": bot},
        id="stale_leads_reminder",
    )
    return scheduler
