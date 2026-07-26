#!/usr/bin/env python3
"""
MADARA DEFAULTER Prank Bot — Entry Point
────────────────────────────────────────
Run:  python main.py

Repo layout:
  config.py          — constants, env vars, shared state
  client.py          — Pyrogram/Kurigram Client instance
  database.py        — SQLite schema + all DB helpers
  helpers.py         — member_check, api_search, schedule_delete, bq
  templates.py       — all message text builders
  keyboards.py       — all InlineKeyboardMarkup builders
  handlers/
    __init__.py      — imports every handler module (registers decorators)
    start.py         — /start
    help.py          — /help
    protect.py       — /protect, /unprotect, /protectedlist  (owner only)
    callbacks.py     — all inline button callbacks
    messages.py      — plain-text number input
"""
import logging

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger("MadaraBot")

# ── Bootstrap ─────────────────────────────────────────────────────────────────
from database import init_db   # noqa: E402
from client import app         # noqa: E402
import handlers                # noqa: E402, F401  — registers all @app.on_* decorators

if __name__ == "__main__":
    init_db()
    log.info("Database ready")
    log.info("Starting MADARA DEFAULTER Prank Bot 🔥")
    app.run()                  # Pyrogram manages its own event loop
