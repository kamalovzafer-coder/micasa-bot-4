"""
AI Chat section — free conversation with Claude.
"""
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from database.connection import get_pool
from data.translations import t
from keyboards.kb import back_keyboard
from services.claude_service import chat_completion, build_system_prompt
import config

router = Router()

SECTION = "chat"
ENTRY_LABELS = {"💬 AI Chat"}


class ChatState(StatesGroup):
    active = State()


async def _get_history(telegram_id: int, limit: int = config.HISTORY_LIMIT) -> list[dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT role, content FROM chat_history
            WHERE telegram_id = $1 AND section = $2
            ORDER BY created_at DESC LIMIT $3
            """,
            telegram_id, SECTION, limit,
        )
    return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]


async def _save_message(telegram_id: int, role: str, content: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO chat_history (telegram_id, section, role, content) VALUES ($1,$2,$3,$4)",
            telegram_id, SECTION, role, content,
        )


# ── Entry ─────────────────────────────────────────────────────────────────────
@router.message(F.text.in_(ENTRY_LABELS))
async def enter_chat(message: Message, state: FSMContext):
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT full_name, language, role FROM users WHERE telegram_id=$1",
            message.from_user.id,
        )
    if not row:
        return
    lang  = row["language"] or "uz"
    fname = (row["full_name"] or "").split()[0]
    await state.set_state(ChatState.active)
    await state.update_data(lang=lang, full_name=row["full_name"], role=row["role"])
    await message.answer(
        t(lang, "chat_welcome", name=fname),
        reply_markup=back_keyboard(lang),
        parse_mode="HTML",
    )


# ── Message handler ───────────────────────────────────────────────────────────
@router.message(ChatState.active, F.text)
async def handle_chat_message(message: Message, state: FSMContext):
    data     = await state.get_data()
    lang     = data.get("lang", "uz")
    full_name = data.get("full_name", "")
    role     = data.get("role", "")
    tid      = message.from_user.id

    system = build_system_prompt(SECTION, full_name, role, lang)
    history = await _get_history(tid)

    await _save_message(tid, "user", message.text)

    thinking = await message.answer("⏳")
    try:
        reply = await chat_completion(system, history, message.text)
    except Exception as e:
        reply = f"❌ Xatolik: {e}"

    await thinking.delete()
    await message.answer(reply, parse_mode="HTML")
    await _save_message(tid, "assistant", reply)
