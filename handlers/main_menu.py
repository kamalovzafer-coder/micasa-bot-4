"""
Main menu navigation — routes button presses to the right section.
"""
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import config
from database.connection import get_pool
from data.translations import t
from keyboards.kb import (
    main_menu_keyboard,
    back_keyboard,
)

router = Router()

# Section entry labels (all languages)
CHAT_LABELS     = {"💬 AI Chat"}
DESIGNER_LABELS = {"🎨 AI Senior Designer"}
ARCHITECT_LABELS = {"🏗️ AI Senior Architect"}
CATALOG_LABELS  = {"📚 Kataloglar", "📚 Каталоги", "📚 Catalogs", "📚 Kataloglar"}
ADMIN_LABELS    = {"⚙️ Admin Panel"}
BACK_LABELS     = {"⬅️ Orqaga", "⬅️ Назад", "⬅️ Back", "⬅️ Geri"}


async def _get_user(telegram_id: int):
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow(
            "SELECT * FROM users WHERE telegram_id = $1", telegram_id
        )


# ── Back button — return to main menu from any section ───────────────────────
@router.message(F.text.in_(BACK_LABELS))
async def back_to_menu(message: Message, state: FSMContext):
    await state.clear()
    row = await _get_user(message.from_user.id)
    if not row:
        return
    lang  = row["language"] or "uz"
    fname = (row["full_name"] or "").split()[0]
    is_admin = (message.from_user.id == config.ADMIN_TELEGRAM_ID)
    await message.answer(
        t(lang, "main_menu", name=fname),
        reply_markup=main_menu_keyboard(lang, is_admin=is_admin),
        parse_mode="HTML",
    )
