"""
MICASA AI Assistant — Telegram Bot
Entry point: registers all routers, starts scheduler, runs polling.
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
from database.connection import close_pool
from database.setup import create_tables
from middlewares.auth import AuthMiddleware
from services.scheduler import start_scheduler

from handlers import onboarding, main_menu, ai_chat, designer, architect, catalog, admin

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    if not config.BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not set")
    if not config.CLAUDE_API_KEY:
        raise ValueError("CLAUDE_API_KEY is not set")
    if not config.DATABASE_URL:
        raise ValueError("DATABASE_URL is not set")
    if not config.ADMIN_TELEGRAM_ID:
        raise ValueError("ADMIN_TELEGRAM_ID is not set")

    logger.info("Creating database tables…")
    await create_tables()
    logger.info("Database ready.")

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(AuthMiddleware())

    dp.include_router(onboarding.router)
    dp.include_router(admin.router)
    dp.include_router(main_menu.router)
    dp.include_router(ai_chat.router)
    dp.include_router(designer.router)
    dp.include_router(architect.router)
    dp.include_router(catalog.router)

    start_scheduler(bot)
    logger.info("Scheduler started.")

    logger.info("Bot polling started — @MICASAASSISTAN_bot")
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await close_pool()
        await bot.session.close()
        logger.info("Bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())
