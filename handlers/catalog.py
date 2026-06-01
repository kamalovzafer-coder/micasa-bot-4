"""
Catalogs section — browse partner catalogs and download files.
"""
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from database.connection import get_pool
from data.translations import t
from keyboards.kb import back_keyboard, catalog_brands_keyboard
import config

router = Router()

ENTRY_LABELS = {"📚 Kataloglar", "📚 Каталоги", "📚 Catalogs"}


class CatalogState(StatesGroup):
    browsing = State()


async def _get_user_lang(telegram_id: int) -> str:
    pool = await get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT language FROM users WHERE telegram_id=$1", telegram_id
        )
    return row["language"] if row else "uz"


# ── Entry ─────────────────────────────────────────────────────────────────────
@router.message(F.text.in_(ENTRY_LABELS))
async def enter_catalog(message: Message, state: FSMContext):
    lang = await _get_user_lang(message.from_user.id)
    await state.set_state(CatalogState.browsing)
    await state.update_data(lang=lang)

    pool = await get_pool()
    async with pool.acquire() as conn:
        brands = await conn.fetch(
            "SELECT id, name FROM catalog_brands ORDER BY name"
        )

    if not brands:
        await message.answer(
            t(lang, "no_catalogs"),
            reply_markup=back_keyboard(lang),
            parse_mode="HTML",
        )
        return

    brand_list = [{"id": b["id"], "name": b["name"]} for b in brands]
    await message.answer(
        t(lang, "catalog_welcome"),
        reply_markup=catalog_brands_keyboard(brand_list, lang),
        parse_mode="HTML",
    )


# ── Brand selected ────────────────────────────────────────────────────────────
@router.callback_query(CatalogState.browsing, F.data.startswith("brand:"))
async def cb_brand(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    lang     = data.get("lang", "uz")
    brand_id = int(call.data.split(":")[1])

    pool = await get_pool()
    async with pool.acquire() as conn:
        brand = await conn.fetchrow(
            "SELECT name FROM catalog_brands WHERE id=$1", brand_id
        )
        files = await conn.fetch(
            "SELECT file_id, file_name, file_type FROM catalog_files WHERE brand_id=$1 ORDER BY uploaded_at",
            brand_id,
        )

    if not brand:
        await call.answer()
        return

    brand_name = brand["name"]
    await call.message.answer(
        t(lang, "catalog_files_header", brand=brand_name),
        parse_mode="HTML",
    )

    if not files:
        await call.message.answer(t(lang, "no_catalog_files"))
    else:
        for f in files:
            try:
                ftype = f["file_type"] or "document"
                fname = f["file_name"] or brand_name
                if ftype == "photo":
                    await bot.send_photo(call.message.chat.id, photo=f["file_id"], caption=fname)
                else:
                    await bot.send_document(
                        call.message.chat.id,
                        document=f["file_id"],
                        caption=fname,
                    )
            except Exception:
                pass

    await call.answer()


# ── Back from catalog brand list ──────────────────────────────────────────────
@router.callback_query(CatalogState.browsing, F.data == "catalog:back")
async def cb_catalog_back(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.delete()
    await call.answer()
