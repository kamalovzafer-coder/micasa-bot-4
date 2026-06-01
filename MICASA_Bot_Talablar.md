# MICASA AI Assistant — Bot Talablari
> Versiya: 1.0 | Sana: 2026-05-31

---

## 1. Umumiy Ma'lumot

- **Bot nomi:** MICASA AI Assistant
- **Kompaniya:** MICASA COMPANY (micasa-design.com)
- **Maqsad:** Kompaniya ichidagi dizaynerlar, arxitektorlar, menejerlar va CEOlar uchun AI assistant
- **Kirish:** Faqat admin (Zafer Kamalov) tasdiqlagan foydalanuvchilar
- **Hosting:** Online server, 24/7 ishlaydi (Zafer kompyuteriga bog'liq emas)
- **AI Engine:** Claude API (Anthropic)
- **Server platformasi:** Railway (muqobil: Fly.io)
- **Ma'lumotlar bazasi:** PostgreSQL

---

## 2. Bot Yaratuvchisi va Egasi

- **Yaratuvchi:** Zafer Kamalov (Interior & Exterior Designer, MICASA)
- Bot "Seni kim yasadi?" yoki "Ho'jayining kim?" degan savolga:
  > *"Meni Zafer Kamalov yaratgan — u hozirda MICASA da katta yangiliklar va loyihalar bilan band va meni takomillashtirish ustida ishlayabdi."*
- **Kompaniya rahbari:** Iskandar Mukhamedov (Founder)

---

## 3. MICASA Jamoasi (Bot Biladigan Ma'lumotlar)

### CEO / Rahbariyat
| Ism | Lavozim |
|-----|---------|
| Iskandar Mukhamedov | Founder |
| Yousef Husain Yousef | UAE CEO |
| Oybek Nazirov | Russia CEO |

### Management
| Ism | Lavozim |
|-----|---------|
| Aziza Mukhamedova | International Manager |
| Aybek Jumanazarov | Project Manager |

### Designers
| Ism | Lavozim |
|-----|---------|
| Badriddin Ashrapov | Senior Technical Designer |
| Asalya Azizova | Interior Designer |
| Anvar Mukhibov | Interior & Exterior Designer |
| Zafer Kamalov | Interior & Exterior Designer |
| Tatyana Kasimova | Interior Designer |
| Doniyor Makhmudov | Interior Designer |
| Alisher Sadikov | Interior Designer |
| Kamila Kasimova | Interior Designer |
| Zakir Zakirov | Interior & Exterior Designer |

### Construction / Arxitektura
| Ism | Lavozim |
|-----|---------|
| Abduqodir Mirdadaev | Senior Architect |
| Murod Shavkatov | Senior Architect |
| Ramziddin Shorustamov | Architect |
| Emir-Abdul Sayfutdinov | Architect |
| Jasur | Architect |
| Omon Kasimov | Architect |
| Eldor Nuraliyev | Architect |
| Bohodir Ibraimov | Supply Manager |

### Ofislar
- Dubai, UAE — Al Barsha 1, Rania Business Tower, 405
- Toshkent, O'zbekiston — Taras Shevchenko ko'chasi 32
- Moskva, Rossiya — Letnaya ko'chasi 99s1

---

## 4. Onboarding (Boshlash Oqimi)

1. `/start` bosilganda → **4 til taklif qilinadi:** Русский / English / Türkçe / O'zbek
2. Til tanlangandan keyin → **Ism va Familya** so'raladi
3. Bot saytdagi (micasa-design.com/team) jamoa ro'yxati bilan solishtiradi:
   - **Mos kelsa** → o'sha odamning rasmini yuborib: *"Adashmasam sizni oldin bu yerda ko'rgandim 😄"*
   - **Mos kelmasa** → team sahifasi linki bilan: *"Sizni bu yerda ko'rolmadim, lekin xush kelibsiz!"*
4. **Yo'nalish so'raladi:** Arxitektor / Dizayner / Menejer / CEO
5. Bot shunga qarab moslashib muloqot qiladi — ismini doim ishlatadi, hazil ham qiladi
6. Bir necha kun gaplashmasa → keyingi suhbatda: *"Oxirgi marta [kun/vaqt]da gaplashdik, nimaga shuncha vaqt yo'q bo'lib ketding?"*

---

## 5. Foydalanuvchi Boshqaruvi (Admin)

- Har yangi `/start` → **Zaferga so'rov** keladi (ismi, lavozimi)
- Zafer **✅ Qabul / ❌ Rad** tugmalari orqali tasdiqlaydi
- Tasdiqlangunga qadar foydalanuvchi: *"Tez orada sizga ruxsat beriladi"* ko'radi
- `/users` komandasi → **barcha foydalanuvchilar ro'yxati** (ismi, lavozimi, oxirgi faollik + 🚫 Uzish tugmasi)
- Zafer istagan odamni istalgan vaqt uzib qo'ya oladi

---

## 6. Bot Bo'limlari (4 ta)

### 6.1 AI Chat
- Erkin suhbat, fikr almashish, tavsiyalar
- **Qisqa, sodda, jonli** — uzun matnlar YO'Q
- Rasmiy emas — hazil, o'sha odamning uslubiga moslashadi
- Vaqt o'tgani sari har bir odamga yanada yaqinlashadi
- Har birini ismi bilan chaqiradi

### 6.2 AI Senior Designer
- Zafer o'qitgan ma'lumotlar bazasi asosida ishlaydi
- Rasmlar, renderlar, JPG, PDF — tahlil qiladi
- Qisqa va aniq fikr bildiradi, kamchiliklarni aytadi
- Kompaniya premium uslubini tushunadi
- Referenslardan detallar oladi: *"Bu sanzul atmosferasi", "Bu tosh turi", "Kamera rakursi"* kabi tavsiyalar beradi

### 6.3 AI Senior Architect
- Planirovka, ergonomika, plan chizmalari
- Ishchi chizmalardagi xatoliklarni topadi
- Aniq tuzatish tavsiyalari beradi
- Rasmlar va PDF fayllarni tahlil qiladi

### 6.4 Kataloglar Bo'limi
- Kompaniya hamkorlarining bo'limlari (Minotti va boshqalar)
- Foydalanuvchi bo'limni ochsa → bot o'sha hamkorning kataloglarini yuboradi
- **Admin (faqat Zafer):** katalog bo'limiga fayl yuklash tugmasi mavjud
- Fayl formatlari: PDF, ZIP, JPG, PNG va boshqa barcha formatlar

---

## 7. O'qitish Tizimi (RAG)

- Admin panel → "📚 O'qitish" bo'limi → kategoriya tanlash (Designer / Architect / Umumiy)
- Fayl yuboriladi → matn ajratiladi → bo'laklarga bo'linadi → vektor bazasiga saqlanadi
- Foydalanuvchi savol berganda → tegishli bilimlar topiladi → javobga qo'shiladi
- Rasmlar → Claude Vision orqali tahlil qilinadi → tavsif saqlanadi
- Bot vaqt o'tgani sari bilimlar bilan o'sib boradi

---

## 8. Avtomatik Xabarlar

- Foydalanuvchi **1 hafta faol bo'lmasa** → bot avtomatik xabar yuboradi:
  > *"Oxirgi bir necha kunda sizni ko'rmadim, tinchlikmi? Sog'ligingiz yaxshimi?"*
- Har bir odamga ismi bilan, samimiy ohangda

---

## 9. Navigatsiya

- Har bir bo'limda **⬅️ Orqaga** tugmasi mavjud
- Asosiy menyuga qaytish uchun `/start` bosish shart emas

---

## 10. Texnik Arxitektura (Qisqacha)

| Komponent | Texnologiya |
|-----------|-------------|
| Bot framework | Python (aiogram) |
| AI engine | Claude API (Anthropic) |
| Ma'lumotlar bazasi | PostgreSQL |
| Vector DB | Supabase pgvector yoki Pinecone |
| Hosting | Railway (24/7) |
| Fayl saqlash | Railway yoki S3-compatible storage |

---

*Hujjat yaratildi: 2026-05-31 | Zafer Kamalov, MICASA*
