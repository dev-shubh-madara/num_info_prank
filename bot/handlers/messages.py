"""
Handler: Plain text messages — processes number input from users
"""
import asyncio
import logging

from pyrogram import filters
from pyrogram.enums import ParseMode

from client import app
from config import WAITING
from database import upsert_user, has_searches, remaining, spend_search, is_protected
from helpers import member_check, api_search, schedule_delete, bq
from templates import (
    txt_not_joined, txt_awaiting_number, txt_limit_reached,
    txt_result, txt_protected_block,
)
from keyboards import kb_join, kb_cancel, kb_refer_home

log = logging.getLogger("MadaraBot")


@app.on_message(
    filters.private & filters.text & ~filters.command(["start", "help", "protect", "unprotect", "protectedlist"])
)
async def handle_text(client, msg):
    u = msg.from_user

    # Force-join gate
    if not await member_check(client, u.id):
        await msg.reply(
            txt_not_joined(),
            reply_markup=kb_join(),
            parse_mode=ParseMode.HTML,
        )
        return

    if u.id not in WAITING:
        await msg.reply(
            bq("❓ Use the <b>🔍 Search Number</b> button to start a search.\n\nSend /start to open the menu."),
            parse_mode=ParseMode.HTML,
        )
        return

    raw   = msg.text.strip()
    clean = raw.replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

    if not clean.isdigit() or not (7 <= len(clean) <= 15):
        await msg.reply(
            bq("❌ <b>Invalid number!</b>\n\nPlease send digits only.\nExample: <code>9988776655</code>"),
            parse_mode=ParseMode.HTML,
        )
        return  # stay in WAITING so user can retry

    WAITING.discard(u.id)

    # ── Protected number check ─────────────────────────────────────────────
    if await is_protected(clean):
        await msg.reply(
            txt_protected_block(clean),
            parse_mode=ParseMode.HTML,
        )
        return

    db_user = await upsert_user(u.id, u.username, u.first_name or "User")
    if not has_searches(db_user):
        me       = await client.get_me()
        ref_link = f"https://t.me/{me.username}?start=ref_{u.id}"
        await msg.reply(
            txt_limit_reached(db_user, ref_link),
            reply_markup=kb_refer_home(),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
        return

    searching = await msg.reply(
        bq("🔍 <b>Searching database...</b>\n\n⏳ Please wait a moment..."),
        parse_mode=ParseMode.HTML,
    )

    data = await api_search(clean)

    try:
        await searching.delete()
    except Exception:
        pass

    if not data:
        await msg.reply(
            bq(f"❌ <b>No data found</b> for <code>{clean}</code>\n\nTry a different number."),
            parse_mode=ParseMode.HTML,
        )
        return

    await spend_search(u.id, db_user["daily_used"])

    result_msg = await msg.reply(
        txt_result(clean, data),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )

    log.info("Prank details sent — user=%s number=%s", u.id, clean)

    # Auto-delete after 2 min (background — doesn't block handler)
    asyncio.create_task(
        schedule_delete(client, msg.chat.id, result_msg.id, clean, delay=120)
    )
