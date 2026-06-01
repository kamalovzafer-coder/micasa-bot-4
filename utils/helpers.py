import base64
import io
from datetime import datetime, timezone

import pdfplumber
from aiogram import Bot


def chunk_text(text: str, size: int = 900, overlap: int = 100) -> list[str]:
    """Split text into overlapping chunks."""
    chunks, start = [], 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap
    return [c.strip() for c in chunks if c.strip()]


async def download_as_bytes(bot: Bot, file_id: str) -> bytes:
    """Download a Telegram file and return raw bytes."""
    file = await bot.get_file(file_id)
    buf = io.BytesIO()
    await bot.download_file(file.file_path, buf)
    buf.seek(0)
    return buf.read()


async def image_to_base64(bot: Bot, file_id: str) -> str:
    """Download image and return base64-encoded string."""
    data = await download_as_bytes(bot, file_id)
    return base64.standard_b64encode(data).decode()


async def extract_pdf_text(bot: Bot, file_id: str) -> str:
    """Download PDF and extract all text with pdfplumber."""
    data = await download_as_bytes(bot, file_id)
    text_parts: list[str] = []
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


def fmt_dt(dt: datetime | None) -> str:
    """Human-readable datetime, e.g. '2026-05-31 14:22'."""
    if dt is None:
        return "—"
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M")


def first_name(full_name: str) -> str:
    """Return first word of a full name."""
    return full_name.strip().split()[0] if full_name else full_name
