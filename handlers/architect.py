"""
AI Senior Architect section — floor plan / drawing analysis + architectural advice.
"""
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from database.connection import get_pool
from data.translations import t
from keyboards.kb import back_keyboard
from services.claude_service import chat_completion, analyze_image, build_system_prompt
from services.knowledge_base import search_knowledge
from utils.helpers import image_to_base64, extract_pdf_text
import config

router = Router()

SECTION = "architect"
ENTRY_LABELS = {"🏗️ AI Senior Architect"}


class ArchitectState(StatesGroup):
    active = State()


async def _get_history(telegram_id: int) -> list[dict]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT role, content FROM chat_history
            WHERE telegram_id=$1 AND section=$2
            ORDER BY created_at DESC LIMIT $3
            """,
            telegram_id, SECTION, config.HISTORY_LIMIT,
        )
    return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]


async def _save(telegram_id: int, role: str, content: str):
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO chat_history (telegram_id, section, role, content) VALUES ($1,$2,$3,$4)",
            telegram_id, SECTION, role, content,
        )


# ── Entry ─────────────────────────────────────────────────────────────────────
@router.message(F.text.in_(ENTRY_LABELS))
async def enter_architect(message: Message, state: FSMContext):
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
    await state.set_state(ArchitectState.active)
    await state.update_data(lang=lang, full_name=row["full_name"], role=row["role"])
    await message.answer(
        t(lang, "architect_welcome", name=fname),
        reply_markup=back_keyboard(lang),
        parse_mode="HTML",
    )


# ── Text ──────────────────────────────────────────────────────────────────────
@router.message(ArchitectState.active, F.text)
async def architect_text(message: Message, state: FSMContext):
    data      = await state.get_data()
    lang      = data.get("lang", "uz")
    full_name = data.get("full_name", "")
    role      = data.get("role", "")
    tid       = message.from_user.id

    kb_context = await search_knowledge("architect", message.text)
    system     = build_system_prompt(SECTION, full_name, role, lang, kb_context)
    history    = await _get_history(tid)

    await _save(tid, "user", message.text)
    thinking = await message.answer("⏳")
    try:
        reply = await chat_completion(system, history, message.text)
    except Exception as e:
        reply = f"❌ Xatolik: {e}"
    await thinking.delete()
    await message.answer(reply, parse_mode="HTML")
    await _save(tid, "assistant", reply)


# ── Image ─────────────────────────────────────────────────────────────────────
@router.message(ArchitectState.active, F.photo)
async def architect_photo(message: Message, state: FSMContext, bot: Bot):
    data      = await state.get_data()
    lang      = data.get("lang", "uz")
    full_name = data.get("full_name", "")
    role      = data.get("role", "")
    tid       = message.from_user.id
    caption   = message.caption or ""

    kb_context = await search_knowledge("architect", caption or "floor plan review")
    system     = build_system_prompt(SECTION, full_name, role, lang, kb_context)
    history    = await _get_history(tid)

    await _save(tid, "user", f"[Image] {caption}")
    thinking = await message.answer("⏳")
    try:
        file_id = message.photo[-1].file_id
        img_b64 = await image_to_base64(bot, file_id)
        reply   = await analyze_image(system, history, img_b64, caption)
    except Exception as e:
        reply = f"❌ Xatolik: {e}"
    await thinking.delete()
    await message.answer(reply, parse_mode="HTML")
    await _save(tid, "assistant", reply)


# ── Document ──────────────────────────────────────────────────────────────────
@router.message(ArchitectState.active, F.document)
async def architect_document(message: Message, state: FSMContext, bot: Bot):
    data      = await state.get_data()
    lang      = data.get("lang", "uz")
    full_name = data.get("full_name", "")
    role      = data.get("role", "")
    tid       = message.from_user.id
    doc       = message.document
    caption   = message.caption or ""

    thinking = await message.answer("⏳")
    try:
        mime = doc.mime_type or ""
        if "pdf" in mime:
            text     = await extract_pdf_text(bot, doc.file_id)
            user_msg = f"[PDF: {doc.file_name}]\n{caption}\n\n{text[:3000]}"
        elif mime.startswith("image/"):
            img_b64    = await image_to_base64(bot, doc.file_id)
            kb_context = await search_knowledge("architect", caption or "plan review")
            system     = build_system_prompt(SECTION, full_name, role, lang, kb_context)
            history    = await _get_history(tid)
            await _save(tid, "user", f"[Image doc] {caption}")
            reply      = await analyze_image(system, history, img_b64, caption, media_type=mime)
            await thinking.delete()
            await message.answer(reply, parse_mode="HTML")
            await _save(tid, "assistant", reply)
            return
        else:
            user_msg = f"[File: {doc.file_name}] {caption}"

        kb_context = await search_knowledge("architect", caption or user_msg[:100])
        system     = build_system_prompt(SECTION, full_name, role, lang, kb_context)
        history    = await _get_history(tid)
        await _save(tid, "user", user_msg[:500])
        reply      = await chat_completion(system, history, user_msg)
    except Exception as e:
        reply = f"❌ Xatolik: {e}"

    await thinking.delete()
    await message.answer(reply, parse_mode="HTML")
    await _save(tid, "assistant", reply)
