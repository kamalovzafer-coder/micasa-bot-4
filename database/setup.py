from database.connection import get_pool

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id              SERIAL PRIMARY KEY,
    telegram_id     BIGINT  UNIQUE NOT NULL,
    username        VARCHAR(255),
    full_name       VARCHAR(255),
    language        VARCHAR(10)  DEFAULT 'uz',
    role            VARCHAR(50),
    is_approved     BOOLEAN DEFAULT FALSE,
    is_blocked      BOOLEAN DEFAULT FALSE,
    is_pending      BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    last_active     TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS chat_history (
    id          SERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
    section     VARCHAR(30) DEFAULT 'chat',
    role        VARCHAR(20) NOT NULL,
    content     TEXT NOT NULL,
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS knowledge_base (
    id          SERIAL PRIMARY KEY,
    category    VARCHAR(50)  NOT NULL,
    file_name   VARCHAR(255) DEFAULT '',
    content     TEXT         NOT NULL,
    chunk_index INTEGER      DEFAULT 0,
    created_at  TIMESTAMP    DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS catalog_brands (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) UNIQUE NOT NULL,
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS catalog_files (
    id          SERIAL PRIMARY KEY,
    brand_id    INTEGER REFERENCES catalog_brands(id) ON DELETE CASCADE,
    file_id     VARCHAR(255) NOT NULL,
    file_name   VARCHAR(255) DEFAULT '',
    file_type   VARCHAR(50)  DEFAULT 'document',
    uploaded_at TIMESTAMP    DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_telegram_id     ON users(telegram_id);
CREATE INDEX IF NOT EXISTS idx_chat_history_user     ON chat_history(telegram_id, section);
CREATE INDEX IF NOT EXISTS idx_kb_category           ON knowledge_base(category);
CREATE INDEX IF NOT EXISTS idx_catalog_files_brand   ON catalog_files(brand_id);
"""


async def create_tables() -> None:
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(CREATE_TABLES_SQL)
