"""UI strings for all 4 supported languages."""

TEXTS: dict[str, dict[str, str]] = {
    # ─── O'ZBEK ───────────────────────────────────────────────────────────────
    "uz": {
        "choose_language": (
            "Assalomu alaykum! 👋\n"
            "Men <b>MICASA AI Assistant</b>.\n\n"
            "Davom etish uchun tilni tanlang:"
        ),
        "enter_name": (
            "Yaxshi! 😊\n"
            "Endi <b>ismingiz va familyangizni</b> kiriting:\n"
            "<i>Masalan: Zafer Kamalov</i>"
        ),
        "found_in_team": (
            "Voy! Adashmasam sizni oldin bu yerda ko'rgandim! 😄\n"
            "Mana siz 👇"
        ),
        "not_found_in_team": (
            "Siz yangi yuzsiniz — <b>xush kelibsiz!</b> 👋\n"
            "Micasa jamoasi bilan tanishing 👇"
        ),
        "choose_role": "Yaxshi, <b>{name}</b>! Qaysi yo'nalishda ishlaysiz?",
        "waiting_approval": (
            "✅ Ma'lumotlaringiz qabul qilindi!\n\n"
            "Zafer tasdiqlagunga qadar biroz kuting.\n"
            "Tez orada javob keladi 🙂"
        ),
        "approved_message": (
            "🎉 <b>Tabriklaymiz, {name}!</b>\n\n"
            "Siz tasdiqlandingiz. Endi MICASA AI Assistant'dan "
            "to'liq foydalana olasiz. Xush kelibsiz! 🚀"
        ),
        "rejected_message": (
            "❌ Kechirasiz, hozircha ruxsat berilmadi.\n"
            "Savollar bo'lsa Zafer bilan bog'laning."
        ),
        "blocked_message": "❌ Sizning akkauntingiz bloklangan. Zafer bilan bog'laning.",
        "pending_message": "⏳ Hali tasdiqlash kutilmoqda. Biroz sabr qiling 🙂",
        "main_menu": "Asosiy menyu 👇\nNima qilamiz, <b>{name}</b>?",
        "back_button": "⬅️ Orqaga",
        "chat_welcome": "Salom <b>{name}</b>! 😊 Gaplashaylik — nima deb yuboresiz?",
        "designer_welcome": "🎨 <b>AI Senior Designer</b> rejimi\nSalom {name}! Rasm yoki savol yuboring.",
        "architect_welcome": "🏗️ <b>AI Senior Architect</b> rejimi\nSalom {name}! Plan yoki savol yuboring.",
        "catalog_welcome": "📚 <b>Kataloglar</b>\nQaysi hamkorni ko'rmoqchisiz?",
        "no_catalogs": "Hozircha kataloglar yo'q. Tez orada qo'shiladi! 🔜",
        "catalog_files_header": "📂 <b>{brand}</b> kataloglari:",
        "no_catalog_files": "Bu bo'limda hali fayl yo'q.",
        "inactive_message": (
            "Salom <b>{name}</b>! 👋\n\n"
            "Oxirgi bir necha kunda sizni ko'rmadim — tinchlikmi? "
            "Sog'ligingiz yaxshimi? 🙂\n\n"
            "Men shu yerdaman, kerak bo'lsa yozing!"
        ),
        # Admin
        "admin_panel": "⚙️ <b>Admin Panel</b>\nNima qilamiz?",
        "users_list_header": "👥 <b>Foydalanuvchilar ro'yxati</b> ({count} ta):\n\n",
        "user_row": "• <b>{name}</b> — {role} | {status}\n  Oxirgi faollik: {last}\n\n",
        "user_blocked": "🚫 {name} bloklandi.",
        "user_unblocked": "✅ {name} blokdan chiqarildi.",
        "choose_kb_category": "📚 Qaysi bo'lim uchun fayl yuklayapsiz?",
        "send_kb_file": "Faylni yuboring (PDF, rasm yoki matn):",
        "kb_saved": "✅ Fayl o'qildi va bilim bazasiga saqlandi!",
        "kb_error": "❌ Faylni o'qishda xatolik. Qayta urinib ko'ring.",
        "choose_catalog_brand": "Qaysi hamkor uchun fayl yuklaysiz?\n(Yangi nom yozsangiz — yangi bo'lim ochiladi)",
        "send_catalog_file": "Katalog faylini yuboring:",
        "catalog_saved": "✅ Katalog saqlandi!",
        "new_user_request": (
            "🔔 <b>Yangi foydalanuvchi so'rovi</b>\n\n"
            "👤 Ism: <b>{name}</b>\n"
            "🆔 Telegram: @{username} ({tid})\n"
            "💼 Yo'nalish: <b>{role}</b>\n"
            "🌐 Til: {lang}\n\n"
            "Ruxsat berasizmi?"
        ),
        "approve_btn": "✅ Qabul qilish",
        "reject_btn": "❌ Rad etish",
        "block_btn": "🚫 Bloklash",
        "unblock_btn": "✅ Blokdan chiqarish",
        "stats_header": (
            "📊 <b>Statistika</b>\n\n"
            "Jami foydalanuvchilar: <b>{total}</b>\n"
            "Tasdiqlanganlar: <b>{approved}</b>\n"
            "Kutayotganlar: <b>{pending}</b>\n"
            "Bloklangan: <b>{blocked}</b>\n"
            "Bilim bazasi yozuvlari: <b>{kb}</b>\n"
            "Katalog brandlari: <b>{brands}</b>"
        ),
    },

    # ─── РУССКИЙ ──────────────────────────────────────────────────────────────
    "ru": {
        "choose_language": (
            "Добрый день! 👋\n"
            "Я <b>MICASA AI Assistant</b>.\n\n"
            "Выберите язык для продолжения:"
        ),
        "enter_name": (
            "Отлично! 😊\n"
            "Введите ваше <b>имя и фамилию</b>:\n"
            "<i>Например: Zafer Kamalov</i>"
        ),
        "found_in_team": "Кажется, я вас уже где-то видел! 😄\nВот вы 👇",
        "not_found_in_team": "Вы новое лицо — <b>добро пожаловать!</b> 👋\nПознакомьтесь с командой Micasa 👇",
        "choose_role": "Отлично, <b>{name}</b>! В какой сфере вы работаете?",
        "waiting_approval": (
            "✅ Ваши данные приняты!\n\n"
            "Ожидайте подтверждения от Zafer.\n"
            "Ответ придёт скоро 🙂"
        ),
        "approved_message": (
            "🎉 <b>Поздравляем, {name}!</b>\n\n"
            "Вы подтверждены. Теперь вы можете пользоваться "
            "MICASA AI Assistant. Добро пожаловать! 🚀"
        ),
        "rejected_message": "❌ К сожалению, доступ не предоставлен.\nОбратитесь к Zafer.",
        "blocked_message": "❌ Ваш аккаунт заблокирован. Обратитесь к Zafer.",
        "pending_message": "⏳ Ожидайте подтверждения. Немного терпения 🙂",
        "main_menu": "Главное меню 👇\nЧто делаем, <b>{name}</b>?",
        "back_button": "⬅️ Назад",
        "chat_welcome": "Привет <b>{name}</b>! 😊 Поговорим — что напишете?",
        "designer_welcome": "🎨 <b>AI Senior Designer</b>\nПривет {name}! Пришлите изображение или вопрос.",
        "architect_welcome": "🏗️ <b>AI Senior Architect</b>\nПривет {name}! Пришлите план или вопрос.",
        "catalog_welcome": "📚 <b>Каталоги</b>\nКакого партнёра хотите посмотреть?",
        "no_catalogs": "Каталоги пока не добавлены. Скоро будут! 🔜",
        "catalog_files_header": "📂 <b>Каталоги {brand}</b>:",
        "no_catalog_files": "В этом разделе пока нет файлов.",
        "inactive_message": (
            "Привет <b>{name}</b>! 👋\n\n"
            "Не видел вас несколько дней — всё в порядке? "
            "Как здоровье? 🙂\n\n"
            "Я здесь, если что — пишите!"
        ),
        "admin_panel": "⚙️ <b>Admin Panel</b>\nЧто делаем?",
        "users_list_header": "👥 <b>Список пользователей</b> ({count}):\n\n",
        "user_row": "• <b>{name}</b> — {role} | {status}\n  Последняя активность: {last}\n\n",
        "user_blocked": "🚫 {name} заблокирован.",
        "user_unblocked": "✅ {name} разблокирован.",
        "choose_kb_category": "📚 Для какого раздела загружаете файл?",
        "send_kb_file": "Отправьте файл (PDF, изображение или текст):",
        "kb_saved": "✅ Файл прочитан и сохранён в базе знаний!",
        "kb_error": "❌ Ошибка при чтении файла. Попробуйте снова.",
        "choose_catalog_brand": "Для какого партнёра загружаете файл?\n(Новое имя — новый раздел)",
        "send_catalog_file": "Отправьте файл каталога:",
        "catalog_saved": "✅ Каталог сохранён!",
        "new_user_request": (
            "🔔 <b>Новый запрос пользователя</b>\n\n"
            "👤 Имя: <b>{name}</b>\n"
            "🆔 Telegram: @{username} ({tid})\n"
            "💼 Направление: <b>{role}</b>\n"
            "🌐 Язык: {lang}\n\n"
            "Разрешить доступ?"
        ),
        "approve_btn": "✅ Принять",
        "reject_btn": "❌ Отклонить",
        "block_btn": "🚫 Заблокировать",
        "unblock_btn": "✅ Разблокировать",
        "stats_header": (
            "📊 <b>Статистика</b>\n\n"
            "Всего пользователей: <b>{total}</b>\n"
            "Подтверждённых: <b>{approved}</b>\n"
            "Ожидающих: <b>{pending}</b>\n"
            "Заблокированных: <b>{blocked}</b>\n"
            "Записей в базе знаний: <b>{kb}</b>\n"
            "Бренды каталогов: <b>{brands}</b>"
        ),
    },

    # ─── ENGLISH ──────────────────────────────────────────────────────────────
    "en": {
        "choose_language": (
            "Hello! 👋\n"
            "I'm <b>MICASA AI Assistant</b>.\n\n"
            "Choose your language to continue:"
        ),
        "enter_name": (
            "Great! 😊\n"
            "Please enter your <b>full name</b>:\n"
            "<i>Example: Zafer Kamalov</i>"
        ),
        "found_in_team": "Wait — haven't I seen you somewhere before?! 😄\nHere you are 👇",
        "not_found_in_team": "You're a new face — <b>welcome!</b> 👋\nMeet the Micasa team 👇",
        "choose_role": "Great, <b>{name}</b>! What is your field of work?",
        "waiting_approval": (
            "✅ Your info has been received!\n\n"
            "Waiting for Zafer's approval.\n"
            "You'll hear back soon 🙂"
        ),
        "approved_message": (
            "🎉 <b>Congratulations, {name}!</b>\n\n"
            "You've been approved. Welcome to MICASA AI Assistant! 🚀"
        ),
        "rejected_message": "❌ Sorry, access was not granted.\nContact Zafer for help.",
        "blocked_message": "❌ Your account has been blocked. Contact Zafer.",
        "pending_message": "⏳ Still waiting for approval. Hang tight 🙂",
        "main_menu": "Main menu 👇\nWhat are we doing, <b>{name}</b>?",
        "back_button": "⬅️ Back",
        "chat_welcome": "Hey <b>{name}</b>! 😊 Let's chat — what's on your mind?",
        "designer_welcome": "🎨 <b>AI Senior Designer</b>\nHey {name}! Send an image or a question.",
        "architect_welcome": "🏗️ <b>AI Senior Architect</b>\nHey {name}! Send a plan or a question.",
        "catalog_welcome": "📚 <b>Catalogs</b>\nWhich partner would you like to browse?",
        "no_catalogs": "No catalogs yet. Coming soon! 🔜",
        "catalog_files_header": "📂 <b>{brand} Catalogs</b>:",
        "no_catalog_files": "No files in this section yet.",
        "inactive_message": (
            "Hey <b>{name}</b>! 👋\n\n"
            "Haven't seen you in a few days — everything okay? "
            "Hope you're well! 🙂\n\n"
            "I'm here whenever you need me."
        ),
        "admin_panel": "⚙️ <b>Admin Panel</b>\nWhat are we doing?",
        "users_list_header": "👥 <b>Users list</b> ({count}):\n\n",
        "user_row": "• <b>{name}</b> — {role} | {status}\n  Last active: {last}\n\n",
        "user_blocked": "🚫 {name} has been blocked.",
        "user_unblocked": "✅ {name} has been unblocked.",
        "choose_kb_category": "📚 Which section is this file for?",
        "send_kb_file": "Send the file (PDF, image, or text):",
        "kb_saved": "✅ File processed and saved to knowledge base!",
        "kb_error": "❌ Error reading file. Please try again.",
        "choose_catalog_brand": "Which partner is this file for?\n(New name = new section)",
        "send_catalog_file": "Send the catalog file:",
        "catalog_saved": "✅ Catalog saved!",
        "new_user_request": (
            "🔔 <b>New User Request</b>\n\n"
            "👤 Name: <b>{name}</b>\n"
            "🆔 Telegram: @{username} ({tid})\n"
            "💼 Role: <b>{role}</b>\n"
            "🌐 Language: {lang}\n\n"
            "Grant access?"
        ),
        "approve_btn": "✅ Approve",
        "reject_btn": "❌ Reject",
        "block_btn": "🚫 Block",
        "unblock_btn": "✅ Unblock",
        "stats_header": (
            "📊 <b>Statistics</b>\n\n"
            "Total users: <b>{total}</b>\n"
            "Approved: <b>{approved}</b>\n"
            "Pending: <b>{pending}</b>\n"
            "Blocked: <b>{blocked}</b>\n"
            "Knowledge base entries: <b>{kb}</b>\n"
            "Catalog brands: <b>{brands}</b>"
        ),
    },

    # ─── TÜRKÇE ───────────────────────────────────────────────────────────────
    "tr": {
        "choose_language": (
            "Merhaba! 👋\n"
            "Ben <b>MICASA AI Assistant</b>.\n\n"
            "Devam etmek için dil seçin:"
        ),
        "enter_name": (
            "Harika! 😊\n"
            "<b>Ad ve soyadınızı</b> girin:\n"
            "<i>Örnek: Zafer Kamalov</i>"
        ),
        "found_in_team": "Dur, sizi daha önce bir yerde görmüştüm! 😄\nİşte siz 👇",
        "not_found_in_team": "Yeni bir yüzsünüz — <b>hoş geldiniz!</b> 👋\nMicasa ekibiyle tanışın 👇",
        "choose_role": "Harika, <b>{name}</b>! Hangi alanda çalışıyorsunuz?",
        "waiting_approval": (
            "✅ Bilgileriniz alındı!\n\n"
            "Zafer'in onayını bekleyin.\n"
            "Yakında cevap gelecek 🙂"
        ),
        "approved_message": (
            "🎉 <b>Tebrikler, {name}!</b>\n\n"
            "Onaylandınız. MICASA AI Assistant'a hoş geldiniz! 🚀"
        ),
        "rejected_message": "❌ Üzgünüz, erişim verilmedi.\nZafer ile iletişime geçin.",
        "blocked_message": "❌ Hesabınız engellendi. Zafer ile iletişime geçin.",
        "pending_message": "⏳ Onay bekleniyor. Biraz sabır 🙂",
        "main_menu": "Ana menü 👇\nNe yapıyoruz, <b>{name}</b>?",
        "back_button": "⬅️ Geri",
        "chat_welcome": "Merhaba <b>{name}</b>! 😊 Sohbet edelim — ne yazıyorsunuz?",
        "designer_welcome": "🎨 <b>AI Senior Designer</b>\nMerhaba {name}! Görsel veya soru gönderin.",
        "architect_welcome": "🏗️ <b>AI Senior Architect</b>\nMerhaba {name}! Plan veya soru gönderin.",
        "catalog_welcome": "📚 <b>Kataloglar</b>\nHangi partneri görmek istiyorsunuz?",
        "no_catalogs": "Henüz katalog yok. Yakında eklenecek! 🔜",
        "catalog_files_header": "📂 <b>{brand} Katalogları</b>:",
        "no_catalog_files": "Bu bölümde henüz dosya yok.",
        "inactive_message": (
            "Merhaba <b>{name}</b>! 👋\n\n"
            "Birkaç gündür sizi görmedim — her şey yolunda mı? "
            "Sağlığınız nasıl? 🙂\n\n"
            "İhtiyacınız olursa buradayım!"
        ),
        "admin_panel": "⚙️ <b>Admin Panel</b>\nNe yapıyoruz?",
        "users_list_header": "👥 <b>Kullanıcı listesi</b> ({count}):\n\n",
        "user_row": "• <b>{name}</b> — {role} | {status}\n  Son aktivite: {last}\n\n",
        "user_blocked": "🚫 {name} engellendi.",
        "user_unblocked": "✅ {name} engeli kaldırıldı.",
        "choose_kb_category": "📚 Bu dosya hangi bölüm için?",
        "send_kb_file": "Dosyayı gönderin (PDF, görsel veya metin):",
        "kb_saved": "✅ Dosya işlendi ve bilgi tabanına kaydedildi!",
        "kb_error": "❌ Dosya okunurken hata oluştu. Tekrar deneyin.",
        "choose_catalog_brand": "Bu dosya hangi partner için?\n(Yeni isim = yeni bölüm)",
        "send_catalog_file": "Katalog dosyasını gönderin:",
        "catalog_saved": "✅ Katalog kaydedildi!",
        "new_user_request": (
            "🔔 <b>Yeni Kullanıcı İsteği</b>\n\n"
            "👤 Ad: <b>{name}</b>\n"
            "🆔 Telegram: @{username} ({tid})\n"
            "💼 Alan: <b>{role}</b>\n"
            "🌐 Dil: {lang}\n\n"
            "Erişim verilsin mi?"
        ),
        "approve_btn": "✅ Onayla",
        "reject_btn": "❌ Reddet",
        "block_btn": "🚫 Engelle",
        "unblock_btn": "✅ Engeli kaldır",
        "stats_header": (
            "📊 <b>İstatistikler</b>\n\n"
            "Toplam kullanıcı: <b>{total}</b>\n"
            "Onaylananlar: <b>{approved}</b>\n"
            "Bekleyenler: <b>{pending}</b>\n"
            "Engellenenler: <b>{blocked}</b>\n"
            "Bilgi tabanı kayıtları: <b>{kb}</b>\n"
            "Katalog markaları: <b>{brands}</b>"
        ),
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    """Return translated string, falling back to 'uz' if key missing."""
    text = TEXTS.get(lang, TEXTS["uz"]).get(key, TEXTS["uz"].get(key, key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    return text
