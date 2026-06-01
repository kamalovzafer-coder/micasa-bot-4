"""
Knowledge base — stores text chunks in PostgreSQL.
Uses full-text search to retrieve relevant context.
"""
from database.connection import get_pool
from utils.helpers import chunk_text
import config


async def save_document(category: str, file_name: str, full_text: str) -> int:
    """Chunk text and save to knowledge_base table. Returns number of chunks saved."""
    pool = await get_pool()
    chunks = chunk_text(full_text, size=config.CHUNK_SIZE, overlap=config.CHUNK_OVERLAP)
    async with pool.acquire() as conn:
        for idx, chunk in enumerate(chunks):
            await conn.execute(
                """
                INSERT INTO knowledge_base (category, file_name, content, chunk_index)
                VALUES ($1, $2, $3, $4)
                """,
                category, file_name, chunk, idx,
            )
    return len(chunks)


async def search_knowledge(category: str, query: str, limit: int = 5) -> str:
    """
    Full-text search in knowledge_base.
    Returns a single string of top-k chunks joined by separator.
    Falls back to most recent chunks if FTS returns nothing.
    """
    pool = await get_pool()
    async with pool.acquire() as conn:
        # Try full-text search first
        rows = await conn.fetch(
            """
            SELECT content
            FROM knowledge_base
            WHERE (category = $1 OR category = 'general')
              AND to_tsvector('simple', content) @@ plainto_tsquery('simple', $2)
            ORDER BY ts_rank(to_tsvector('simple', content), plainto_tsquery('simple', $2)) DESC
            LIMIT $3
            """,
            category, query, limit,
        )
        if not rows:
            # Fallback: latest chunks for this category
            rows = await conn.fetch(
                """
                SELECT content FROM knowledge_base
                WHERE category = $1 OR category = 'general'
                ORDER BY created_at DESC
                LIMIT $2
                """,
                category, limit,
            )

    if not rows:
        return ""

    return "\n---\n".join(r["content"] for r in rows)


async def kb_count() -> int:
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchval("SELECT COUNT(*) FROM knowledge_base")
