"""
Onboarding flow:
/start → choose language → enter full name → (team check) → choose role → wait for approval
"""
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

import config
from database.connection import get_pool
from data.team import find_team_member, TEAM_BASE_URL, TEAM_PAGE_URL
from data.translations import t
from keyboards.kb import (
    lang_keyboard,
    role_keyboard,
    main_menu_keyboard,
    approval_keyboard,
)
from utils.helpers import fmt_dt

router = Router()


class Onboarding(StatesGroup):
    language = State()
    name     = State()
    role     = State()


# ── /start ────────────────────────────────────────────────────────────────────
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM users WHERE telegram_id = $1", message.from_user.id
        )

    if row:
        lang = row["language"] or "uz"
        if row["is_blocked"]:
            await message.answer(t(lang, "blocked_message"))
            return
        if row["is_pending"] or not row["is_approved"]:
            await message.answer(t(lang, "pending_message"))
            return
        # Already approved — show main menu
        fname = (row["full_name"] or "").split()[0]
        is_admin = (message.from_user.id == config.ADMIN_TELEGRAM_ID)
        await message.answer(
            t(lang, "main_menu", name=fname),
            reply_markup=main_menu_keyboard(lang, is_admin=is_admin),
            parse_mode="HTML",
        )
        return

    # New user — start onboarding
    await state.set_state(Onboarding.language)
    await message.answer(
        t("uz", "choose_language"),
        reply_markup=lang_keyboard(),
        parse_mode="HTML",
    )


# ── Language chosen ───────────────────────────────────────────────────────────
@router.callback_query(Onboarding.language, F.data.startswith("lang:"))
async def cb_language(call: CallbackQuery, state: FSMContext):
    lang = call.data.split(":")[1]
    await state.update_data(language=lang)
    await state.set_state(Onboarding.name)
    await call.message.edit_text(t(lang, "enter_name"), parse_mode="HTML")


# ── Full name entered ─────────────────────────────────────────────────────────
@router.message(Onboarding.name)
async def onb_name(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    lang = data.get("language", "uz")
    full_name = message.text.strip()

    if len(full_name) < 3:
        await message.answer(t(lang, "enter_name"), parse_mode="HTML")
        return

    await state.update_data(full_name=full_name)

    # Check against team list
    member = find_team_member(full_name)
    if member:
        photo_url = TEAM_BASE_URL + member["photo"]
        caption = (
            f"{t(lang, 'found_in_team')}\n\n"
            f"<b>{member['name']}</b>\n{member['role']}"
        )
        try:
            await bot.send_photo(message.chat.id, photo=photo_url, caption=caption, parse_mode="HTML")
        except Exception:
            await message.answer(caption, parse_mode="HTML")
    else:
        await message.answer(
            f"{t(lang, 'not_found_in_team')}\n{TEAM_PAGE_URL}",
            parse_mode="HTML",
            disable_web_page_preview=False,
        )

    await state.set_state(Onboarding.role)
    await message.answer(
        t(lang, "choose_role", name=full_name.split()[0]),
        reply_markup=role_keyboard(lang),
        parse_mode="HTML",
    )


# ── Role chosen ───────────────────────────────────────────────────────────────
@router.callback_query(Onboarding.role, F.data.startswith("role:"))
async def cb_role(call: CallbackQuery, state: FSMContext, bot: Bot):
    role = call.data.split(":")[1]
    data = await state.get_data()
    lang      = data.get("language", "uz")
    full_name = data.get("full_name", "")
    tg_user   = call.from_user

    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO users (telegram_id, username, full_name, language, role,
                               is_approved, is_blocked, is_pending)
            VALUES ($1, $2, $3, $4, $5, FALSE, FALSE, TRUE)
            ON CONFLICT (telegram_id) DO UPDATE
              SET full_name = EXCLUDED.full_name,
                  language  = EXCLUDED.language,
                  role      = EXCLUDED.role,
                  is_pending = TRUE
            """,
            tg_user.id,
            tg_user.username or "",
            full_name,
            lang,
            role,
        )

    await state.clear()
    await call.message.edit_text(t(lang, "waiting_approval"), parse_mode="HTML")

    # Notify admin
    username = tg_user.username or "—"
    lang_names = {"uz": "O'zbek", "ru": "Русский", "en": "English", "tr": "Türkçe"}
    text = t(
        "uz",
        "new_user_request",
        name=full_name,
        username=username,
        tid=tg_user.id,
        role=role,
        lang=lang_names.get(lang, lang),
    )
    await bot.send_message(
        config.ADMIN_TELEGRAM_ID,
        text,
        reply_markup=approval_keyboard(tg_user.id, "uz"),
        parse_mode="HTML",
    )


# ── Admin approve callback ────────────────────────────────────────────────────
@router.callback_query(F.data.startswith("approve:"))
async def cb_approve(call: CallbackQuery, bot: Bot):
    if call.from_user.id != config.ADMIN_TELEGRAM_ID:
        return
    target_id = int(call.data.split(":")[1])

    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "UPDATE users SET is_approved=TRUE, is_pending=FALSE WHERE telegram_id=$1 RETURNING *",
            target_id,
        )

    if row:
        lang  = row["language"] or "uz"
        fname = (row["full_name"] or "").split()[0]
        is_admin = (target_id == config.ADMIN_TELEGRAM_ID)
        await bot.send_message(
            target_id,
            t(lang, "approved_message", name=fname),
            reply_markup=main_menu_keyboard(lang, is_admin=is_admin),
            parse_mode="HTML",
        )
        await call.message.edit_text(
            call.message.text + f"\n\n✅ <b>Tasdiqlandi</b> — {row['full_name']}",
            parse_mode="HTML",
        )
    await call.answer()


# ── Admin reject callback ─────────────────────────────────────────────────────
@router.callback_query(F.data.startswith("reject:"))
async def cb_reject(call: CallbackQuery, bot: Bot):
    if call.from_user.id != config.ADMIN_TELEGRAM_ID:
        return
    target_id = int(call.data.split(":")[1])

    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "UPDATE users SET is_pending=FALSE WHERE telegram_id=$1 RETURNING *",
            target_id,
        )

    if row:
        lang = row["language"] or "uz"
        await bot.send_message(target_id, t(lang, "rejected_message"), parse_mode="HTML")
        await call.message.edit_text(
            call.message.text + f"\n\n❌ <b>Rad etildi</b> — {row['full_name']}",
            parse_mode="HTML",
        )
    await call.answer()
