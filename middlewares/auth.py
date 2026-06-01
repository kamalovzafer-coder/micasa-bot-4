"""
Auth middleware:
- Updates last_active for every message from a known user.
- Blocks messages from users who are not yet approved or are blocked
  (except /start which is always allowed).
"""
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

import config
from database.connection import get_pool
from data.translations import t


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        user = event.from_user
        if user is None:
            return await handler(event, data)

        # /start is always allowed
        if event.text and event.text.startswith("/start"):
            return await handler(event, data)

        pool = await get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT is_approved, is_blocked, is_pending, language FROM users WHERE telegram_id = $1",
                user.id,
            )

        if row is None:
            # Unknown user — let /start handler create them
            return await handler(event, data)

        lang = row["language"] or "uz"

        if row["is_blocked"]:
            await event.answer(t(lang, "blocked_message"))
            return

        if row["is_pending"] or not row["is_approved"]:
            await event.answer(t(lang, "pending_message"))
            return

        # Update last_active
        async with pool.acquire() as conn:
            await conn.execute(
                "UPDATE users SET last_active = NOW() WHERE telegram_id = $1",
                user.id,
            )

        return await handler(event, data)
