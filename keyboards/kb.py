from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from data.translations import t

remove_kb = ReplyKeyboardRemove()


# ── Language selection ────────────────────────────────────────────────────────
def lang_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbek",  callback_data="lang:uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
        ],
        [
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
            InlineKeyboardButton(text="🇹🇷 Türkçe",  callback_data="lang:tr"),
        ],
    ])


# ── Role selection ────────────────────────────────────────────────────────────
def role_keyboard(lang: str) -> InlineKeyboardMarkup:
    roles = {
        "uz": ["🎨 Dizayner", "🏗️ Arxitektor", "📋 Menejer", "👔 CEO"],
        "ru": ["🎨 Дизайнер", "🏗️ Архитектор", "📋 Менеджер", "👔 CEO"],
        "en": ["🎨 Designer",  "🏗️ Architect",  "📋 Manager",  "👔 CEO"],
        "tr": ["🎨 Tasarımcı","🏗️ Mimar",       "📋 Yönetici", "👔 CEO"],
    }
    labels = roles.get(lang, roles["uz"])
    data   = ["Dizayner", "Arxitektor", "Menejer", "CEO"]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=labels[i], callback_data=f"role:{data[i]}")]
        for i in range(4)
    ])


# ── Admin approve / reject new user ──────────────────────────────────────────
def approval_keyboard(telegram_id: int, lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=t(lang, "approve_btn"),
                callback_data=f"approve:{telegram_id}",
            ),
            InlineKeyboardButton(
                text=t(lang, "reject_btn"),
                callback_data=f"reject:{telegram_id}",
            ),
        ],
    ])


# ── Main menu ─────────────────────────────────────────────────────────────────
def main_menu_keyboard(lang: str, is_admin: bool = False) -> ReplyKeyboardMarkup:
    labels = {
        "uz": ["💬 AI Chat", "🎨 AI Senior Designer", "🏗️ AI Senior Architect", "📚 Kataloglar", "⚙️ Admin Panel"],
        "ru": ["💬 AI Chat", "🎨 AI Senior Designer", "🏗️ AI Senior Architect", "📚 Каталоги",   "⚙️ Admin Panel"],
        "en": ["💬 AI Chat", "🎨 AI Senior Designer", "🏗️ AI Senior Architect", "📚 Catalogs",   "⚙️ Admin Panel"],
        "tr": ["💬 AI Chat", "🎨 AI Senior Designer", "🏗️ AI Senior Architect", "📚 Kataloglar", "⚙️ Admin Panel"],
    }
    lbls = labels.get(lang, labels["uz"])
    rows = [
        [KeyboardButton(text=lbls[0])],
        [KeyboardButton(text=lbls[1])],
        [KeyboardButton(text=lbls[2])],
        [KeyboardButton(text=lbls[3])],
    ]
    if is_admin:
        rows.append([KeyboardButton(text=lbls[4])])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


# ── Back button ───────────────────────────────────────────────────────────────
def back_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t(lang, "back_button"))]],
        resize_keyboard=True,
    )


# ── Catalog brand list ────────────────────────────────────────────────────────
def catalog_brands_keyboard(brands: list[dict], lang: str) -> InlineKeyboardMarkup:
    """brands = list of {'id': int, 'name': str}"""
    rows = [
        [InlineKeyboardButton(text=b["name"], callback_data=f"brand:{b['id']}")]
        for b in brands
    ]
    rows.append([InlineKeyboardButton(text=t(lang, "back_button"), callback_data="catalog:back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ── Admin panel ───────────────────────────────────────────────────────────────
def admin_panel_keyboard(lang: str) -> InlineKeyboardMarkup:
    labels = {
        "uz": ["👥 Foydalanuvchilar", "📚 O'qitish (KB)", "📁 Katalog qo'shish", "📊 Statistika"],
        "ru": ["👥 Пользователи",     "📚 Обучение (KB)",  "📁 Добавить каталог",  "📊 Статистика"],
        "en": ["👥 Users",            "📚 Knowledge Base", "📁 Add Catalog",       "📊 Statistics"],
        "tr": ["👥 Kullanıcılar",     "📚 Eğitim (KB)",    "📁 Katalog ekle",      "📊 İstatistikler"],
    }
    lbls = labels.get(lang, labels["uz"])
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=lbls[0], callback_data="admin:users")],
        [InlineKeyboardButton(text=lbls[1], callback_data="admin:kb")],
        [InlineKeyboardButton(text=lbls[2], callback_data="admin:catalog")],
        [InlineKeyboardButton(text=lbls[3], callback_data="admin:stats")],
    ])


# ── KB category selection (admin) ─────────────────────────────────────────────
def kb_category_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎨 Designer",  callback_data="kbcat:designer")],
        [InlineKeyboardButton(text="🏗️ Architect", callback_data="kbcat:architect")],
        [InlineKeyboardButton(text="📋 Umumiy",    callback_data="kbcat:general")],
    ])


# ── User management (block / unblock) ─────────────────────────────────────────
def user_manage_keyboard(telegram_id: int, is_blocked: bool, lang: str) -> InlineKeyboardMarkup:
    if is_blocked:
        action_btn = InlineKeyboardButton(
            text=t(lang, "unblock_btn"),
            callback_data=f"unblock:{telegram_id}",
        )
    else:
        action_btn = InlineKeyboardButton(
            text=t(lang, "block_btn"),
            callback_data=f"block:{telegram_id}",
        )
    return InlineKeyboardMarkup(inline_keyboard=[[action_btn]])
