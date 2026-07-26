"""
Handler: /num <number> command inside the group chat
Members who join the group get unlimited searches via this command.
The bot ONLY responds to /num — never to plain messages in the group.
"""
import asyncio
import logging

from pyrogram import filters
from pyrogram.enums import ParseMode

from client import app
from config import GROUP_ID
from database import is_protected
from helpers import api_search, bq, schedule_delete
from templates import txt_result, txt_protected_block

log = logging.getLogger("MadaraBot")


def _clean(raw: str) -> str:
    return raw.replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")


@app.on_message(filters.command("num") & filters.chat(GROUP_ID))
async def group_num(client, msg):
    if len(msg.command) < 2:
        await msg.reply(
            bq(
                "❓ <b>Usage:</b> <code>/num &lt;number&gt;</code>\n\n"
                "Example: <code>/num 9988776655</code>\n\n"
                "👨‍💻 <b>Developer:</b> MADARA DEFAULTER"
            ),
            parse_mode=ParseMode.HTML,
        )
        return

    clean = _clean(msg.command[1])

    if not clean.isdigit() or not (7 <= len(clean) <= 15):
        await msg.reply(
            bq("❌ <b>Invalid number!</b>\n\nDigits only. Example: <code>9988776655</code>"),
            parse_mode=ParseMode.HTML,
        )
        return

    # Protected number gate
    if await is_protected(clean):
        await msg.reply(
            txt_protected_block(clean),
            parse_mode=ParseMode.HTML,
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

    result_msg = await msg.reply(
        txt_result(clean, data),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )

    log.info("Group prank sent — user=%s number=%s", msg.from_user.id if msg.from_user else "?", clean)

    # Auto-delete after 2 min
    asyncio.create_task(
        schedule_delete(client, msg.chat.id, result_msg.id, clean, delay=120)
    )
