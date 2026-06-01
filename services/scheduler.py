"""
APScheduler — daily job that notifies users inactive for 7+ days.
"""
from datetime import datetime, timedelta, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot

import config
from database.connection import get_pool
from data.translations import t

scheduler = AsyncIOScheduler(timezone="UTC")


async def notify_inactive_users(bot: Bot) -> None:
    pool = await get_pool()
    cutoff = datetime.now(timezone.utc) - timedelta(days=config.INACTIVE_DAYS)

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT telegram_id, full_name, language
            FROM users
            WHERE is_approved = TRUE
              AND is_blocked  = FALSE
              AND last_active < $1
            """,
            cutoff,
        )

    for row in rows:
        lang  = row["language"] or "uz"
        fname = (row["full_name"] or "").split()[0]
        text  = t(lang, "inactive_message", name=fname)
        try:
            await bot.send_message(row["telegram_id"], text, parse_mode="HTML")
        except Exception:
            pass  # user may have blocked the bot


def start_scheduler(bot: Bot) -> None:
    # Run every day at 10:00 UTC
    scheduler.add_job(
        notify_inactive_users,
        trigger="cron",
        hour=10,
        minute=0,
        args=[bot],
        id="inactive_notify",
        replace_existing=True,
    )
    scheduler.start()
