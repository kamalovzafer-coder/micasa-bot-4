import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN", "")
CLAUDE_API_KEY: str = os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY", "")
DATABASE_URL: str = os.getenv("DATABASE_URL", "")
ADMIN_TELEGRAM_ID: int = int(os.getenv("ADMIN_TELEGRAM_ID", "0"))

# Fix Railway's postgres:// to postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

CLAUDE_MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1024
HISTORY_LIMIT = 10          # last N messages kept per section
INACTIVE_DAYS = 7           # days before sending "miss you" message
CHUNK_SIZE = 900 