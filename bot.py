# bot.py
import asyncio
import logging
import db
import config
from aiogram import Bot, Dispatcher
from storage import SQLiteStorage
from handlers.start import router as start_router
from handlers.flow import router as flow_router
from handlers.confirm import router as confirm_router
from handlers.commands import router as commands_router
from scheduler import create_scheduler

logging.basicConfig(level=logging.INFO)


async def main():
    db.init(config.DB_PATH)

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=SQLiteStorage())

    # Order matters: start router first (catches /start globally)
    dp.include_router(start_router)
    dp.include_router(flow_router)
    dp.include_router(confirm_router)
    dp.include_router(commands_router)

    scheduler = create_scheduler(bot)
    scheduler.start()

    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
