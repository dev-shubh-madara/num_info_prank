"""
MADARA DEFAULTER Prank Bot — Config & Constants
"""
import os

# ── Telegram credentials ────────────────────────────────────────────────────
API_ID      = int(os.environ["API_ID"])
API_HASH    = os.environ["API_HASH"]
BOT_TOKEN   = os.environ["TELEGRAM_BOT_TOKEN"]

# ── Group / Owner ────────────────────────────────────────────────────────────
GROUP_ID    = int(os.environ["GROUP_ID"])
GROUP_LINK  = "https://t.me/+gqpAcHXgggxhZjRl"
OWNER_ID    = 8762430892          # unlimited searches + /protect power

# ── Limits ───────────────────────────────────────────────────────────────────
DAILY_FREE  = 2                   # free searches per user per day

# ── Persistence ──────────────────────────────────────────────────────────────
DB_PATH     = "/tmp/madara_bot.db"

# ── External API ─────────────────────────────────────────────────────────────
SEARCH_API  = "https://ankan-dey-number-search-api.hf.space/search"
SEARCH_KEY  = "Demo"

# ── In-memory state: users currently waiting for a number input ──────────────
WAITING: set[int] = set()
