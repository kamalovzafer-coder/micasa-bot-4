"""
Admin panel:
- View & manage users (block / unblock)
- Upload knowledge-base files (PDF / image)
- Add catalog files per brand
- View statistics
"""
from aiogram import Router, F, Bot
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

import config
from database.connection import get_pool
from data.translations import t
from keyboards.kb import (
    admin_panel_keyboard,
    kb_category_keyboard,
    user_manage_keyboard,
    back_keyboard,
    main_menu_keyboard,
)
from services.knowledge_base import save_document, kb_count
from utils.helpers import extract_pdf_text, image_to_base64, fmt_dt

router = Router()

ENTRY_LABELS = {"⚙️ Admin Panel"}


# ── Admin-only filter ─────────────────────────────────────────────────────────
class IsAdmin(Filter):
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        uid = event.from_user.id if event.from_user else 0
        return uid == config.ADMIN_TELEGRAM_ID


# ── FSM states ────────────────────────────────────────────────────────────────
class AdminState(StatesGroup):
    panel         = State()
    kb_category   = State()
    kb_waiting    = State()
    catalog_brand = State()
    catalog_file  = State()


# ── Entry ─────────────────────────────────────────────────────────────────────
@router.message(IsAdmin(), F.text.in_(ENTRY_LABELS))
async def enter_admin(message: Message, state: FSMContext):
    await state.set_state(AdminState.panel)
    await message.answer(
        t("uz", "admin_panel"),
        reply_markup=admin_panel_keyboard("uz"),
        parse_mode="HTML",
    )


# ── Panel callbacks ───────────────────────────────────────────────────────────
@router.callback_query(IsAdmin(), AdminState.panel, F.data == "admin:users")
async def admin_users(call: CallbackQuery, state: FSMContext):
    pool = await get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT telegram_id, full_name, role, is_approved, is_blocked, last_active "
            "FROM users ORDER BY created_at DESC LIMIT 50"
        )

    if not rows:
        await call.message.answer("Hali foydalanuvchi yo'q.")
        await call.answer()
        return

    text = t("uz", "users_list_header", count=len(rows))
    for r in rows:
        if r["is_blocked"]:
            status = "🚫 Bloklangan"
        elif r["is_approved"]:
            status = "✅ Tasdiqlangan"
        else:
            status = "⏳ Kutmoqda"
        text += t(
            "uz", "user_row",
            name=r["full_name"] or "—",
            role=r["role"] or "—",
            status=status,
            last=fmt_dt(r["last_active"]),
        )

    await call.message.answer(text, parse_mode="HTML")

    # Send individual manage buttons
    for r in rows:
        kb = user_manage_keyboard(r["telegram_id"], r["is_blocked"], "uz")
        await call.message.answer(
            f"<b>{r['full_name']}</b> ({r['telegram_id']})",
            reply_markup=kb,
            parse_mode="HTML",
        )
    await call.answer()


@router.callback_query(IsAdmin(), F.data.startswith("block:"))
async def cb_block(call: CallbackQuery):
    tid = int(call.data.split(":")[1])
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "UPDATE users SET is_blocked=TRUE WHERE telegram_id=$1 RETURNING full_name, language",
            tid,
        )
    if row:
        await call.message.edit_reply_markup(
            reply_markup=user_manage_keyboard(tid, True, "uz")
        )
        await call.answer(t("uz", "user_blocked", name=row["full_name"]))
    else:
        await call.answer()


@router.callback_query(IsAdmin(), F.data.startswith("unblock:"))
async def cb_unblock(call: CallbackQuery):
    tid = int(call.data.split(":")[1])
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "UPDATE users SET is_blocked=FALSE WHERE telegram_id=$1 RETURNING full_name, language",
            tid,
        )
    if row:
        await call.message.edit_reply_markup(
            reply_markup=user_manage_keyboard(tid, False, "uz")
        )
        await call.answer(t("uz", "user_unblocked", name=row["full_name"]))
    else:
        await call.answer()


# ── Knowledge base ────────────────────────────────────────────────────────────
@router.callback_query(IsAdmin(), AdminState.panel, F.data == "admin:kb")
async def admin_kb(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.kb_category)
    await call.message.answer(
        t("uz", "choose_kb_category"),
        reply_markup=kb_category_keyboard(),
        parse_mode="HTML",
    )
    await call.answer()


@router.callback_query(IsAdmin(), AdminState.kb_category, F.data.startswith("kbcat:"))
async def cb_kb_category(call: CallbackQuery, state: FSMContext):
    category = call.data.split(":")[1]
    await state.update_data(kb_category=category)
    await state.set_state(AdminState.kb_waiting)
    await call.message.answer(t("uz", "send_kb_file"), parse_mode="HTML")
    await call.answer()


@router.message(IsAdmin(), AdminState.kb_waiting, F.document)
async def kb_receive_document(message: Message, state: FSMContext, bot: Bot):
    data     = await state.get_data()
    category = data.get("kb_category", "general")
    doc      = message.document
    mime     = doc.mime_type or ""

    try:
        if "pdf" in mime:
            text = await extract_pdf_text(bot, doc.file_id)
        elif mime.startswith("image/"):
            # For images: ask Claude to describe them and store the description
            import base64
            from utils.helpers import download_as_bytes
            raw     = await download_as_bytes(bot, doc.file_id)
            b64     = base64.standard_b64encode(raw).decode()
            from services.claude_service import get_client
            client  = get_client()
            resp    = await client.messages.create(
                model=config.CLAUDE_MODEL,
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image", "source": {"type": "base64", "media_type": mime, "data": b64}},
                        {"type": "text",  "text": "Describe this image in detail for a design knowledge base."},
                    ],
                }],
            )
            text = resp.content[0].text
        else:
            # Plain text / other
            from utils.helpers import download_as_bytes
            raw  = await download_as_bytes(bot, doc.file_id)
            text = raw.decode("utf-8", errors="ignore")

        chunks = await save_document(category, doc.file_name or "", text)
        await message.answer(f"✅ Saqlandi! {chunks} ta bo'lak.")
    except Exception as e:
        await message.answer(t("uz", "kb_error") + f"\n{e}")

    await state.set_state(AdminState.panel)
    await message.answer(t("uz", "admin_panel"), reply_markup=admin_panel_keyboard("uz"), parse_mode="HTML")


@router.message(IsAdmin(), AdminState.kb_waiting, F.photo)
async def kb_receive_photo(message: Message, state: FSMContext, bot: Bot):
    data     = await state.get_data()
    category = data.get("kb_category", "general")
    try:
        img_b64 = await image_to_base64(bot, message.photo[-1].file_id)
        from services.claude_service import get_client
        client  = get_client()
        resp    = await client.messages.create(
            model=config.CLAUDE_MODEL,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": img_b64}},
                    {"type": "text",  "text": "Describe this design image in detail for a knowledge base."},
                ],
            }],
        )
        text   = resp.content[0].text
        chunks = await save_document(category, "photo", text)
        await message.answer(f"✅ Rasm tahlil qilindi va saqlandi! {chunks} ta bo'lak.")
    except Exception as e:
        await message.answer(t("uz", "kb_error") + f"\n{e}")

    await state.set_state(AdminState.panel)
    await message.answer(t("uz", "admin_panel"), reply_markup=admin_panel_keyboard("uz"), parse_mode="HTML")


# ── Catalog management ────────────────────────────────────────────────────────
@router.callback_query(IsAdmin(), AdminState.panel, F.data == "admin:catalog")
async def admin_catalog(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.catalog_brand)
    await call.message.answer(t("uz", "choose_catalog_brand"), parse_mode="HTML")
    await call.answer()


@router.message(IsAdmin(), AdminState.catalog_brand, F.text)
async def catalog_brand_name(message: Message, state: FSMContext):
    brand_name = message.text.strip()
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "INSERT INTO catalog_brands (name) VALUES ($1) ON CONFLICT (name) DO UPDATE SET name=EXCLUDED.name RETURNING id",
            brand_name,
        )
    await state.update_data(catalog_brand_id=row["id"], catalog_brand_name=brand_name)
    await state.set_state(AdminState.catalog_file)
    await message.answer(t("uz", "send_catalog_file"), parse_mode="HTML")


@router.message(IsAdmin(), AdminState.catalog_file, F.document)
async def catalog_receive_document(message: Message, state: FSMContext):
    data     = await state.get_data()
    brand_id = data.get("catalog_brand_id")
    doc      = message.document
    mime     = doc.mime_type or ""
    ftype    = "photo" if mime.startswith("image/") else "document"

    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO catalog_files (brand_id, file_id, file_name, file_type) VALUES ($1,$2,$3,$4)",
            brand_id, doc.file_id, doc.file_name or "", ftype,
        )
    await message.answer(t("uz", "catalog_saved"))
    # Stay in catalog_file state so admin can keep uploading
    await message.answer("Yana fayl yuboring yoki /done yozing.")


@router.message(IsAdmin(), AdminState.catalog_file, F.photo)
async def catalog_receive_photo(message: Message, state: FSMContext):
    data     = await state.get_data()
    brand_id = data.get("catalog_brand_id")
    file_id  = message.photo[-1].file_id
    caption  = message.caption or data.get("catalog_brand_name", "")

    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO catalog_files (brand_id, file_id, file_name, file_type) VALUES ($1,$2,$3,'photo')",
            brand_id, file_id, caption,
        )
    await message.answer(t("uz", "catalog_saved"))
    await message.answer("Yana fayl yuboring yoki /done yozing.")


@router.message(IsAdmin(), AdminState.catalog_file, F.text == "/done")
async def catalog_done(message: Message, state: FSMContext):
    await state.set_state(AdminState.panel)
    await message.answer(t("uz", "admin_panel"), reply_markup=admin_panel_keyboard("uz"), parse_mode="HTML")


# ── Statistics ────────────────────────────────────────────────────────────────
@router.callback_query(IsAdmin(), AdminState.panel, F.data == "admin:stats")
async def admin_stats(call: CallbackQuery):
    pool = await get_pool()
    async with pool.acquire() as conn:
        total    = await conn.fetchval("SELECT COUNT(*) FROM users")
        approved = await conn.fetchval("SELECT COUNT(*) FROM users WHERE is_approved=TRUE")
        pending  = await conn.fetchval("SELECT COUNT(*) FROM users WHERE is_pending=TRUE")
        blocked  = await conn.fetchval("SELECT COUNT(*) FROM users WHERE is_blocked=TRUE")
        kb       = await conn.fetchval("SELECT COUNT(*) FROM knowledge_base")
        brands   = await conn.fetchval("SELECT COUNT(*) FROM catalog_brands")

    text = t(
        "uz", "stats_header",
        total=total, approved=approved,
        pending=pending, blocked=blocked,
        kb=kb, brands=brands,
    )
    await call.message.answer(text, parse_mode="HTML")
    await call.answer()
