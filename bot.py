# bot.py
import asyncio
import logging
import db
import config
from aiogram import Bot, Dispatcher
from aiogram.types import ErrorEvent
from storage import SQLiteStorage
from handlers.start import router as start_router
from handlers.flow import router as flow_router
from handlers.confirm import router as confirm_router
from handlers.commands import router as commands_router
from handlers.fallback import router as fallback_router, RECOVERY
from scheduler import create_scheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def on_error(event: ErrorEvent, bot: Bot):
    """Catch any unhandled exception so a crash inside a handler never leaves
    the user in silence. Log it and send the recovery prompt."""
    logger.exception("Update caused an error: %s", event.exception)
    update = event.update
    chat_id = None
    if update.message:
        chat_id = update.message.chat.id
    elif update.callback_query and update.callback_query.message:
        chat_id = update.callback_query.message.chat.id
    if chat_id is not None:
        try:
            await bot.send_message(chat_id, RECOVERY)
        except Exception:
            logger.exception("Failed to send recovery message to %s", chat_id)


async def main():
    db.init(config.DB_PATH)

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=SQLiteStorage())

    # Order matters: start router first (catches /start globally),
    # fallback router last (catches anything no one else handled).
    dp.include_router(start_router)
    dp.include_router(flow_router)
    dp.include_router(confirm_router)
    dp.include_router(commands_router)
    dp.include_router(fallback_router)

    dp.errors.register(on_error)

    scheduler = create_scheduler(bot)
    scheduler.start()

    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
