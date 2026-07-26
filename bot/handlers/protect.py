"""
Handler: /protect and /unprotect commands (owner only)
Owner can protect/unprotect any number so it cannot be searched.
"""
from pyrogram import filters
from pyrogram.enums import ParseMode

from client import app
from config import OWNER_ID
from database import protect_number, unprotect_number, list_protected
from helpers import bq
from keyboards import kb_back


def _clean_number(raw: str) -> str:
    return raw.replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")


@app.on_message(filters.command("protect") & filters.private & filters.user(OWNER_ID))
async def cmd_protect(client, msg):
    if len(msg.command) < 2:
        await msg.reply(
            bq(
                "🛡️ <b>Protect a Number</b>\n\n"
                "Usage: <code>/protect &lt;number&gt;</code>\n\n"
                "Example: <code>/protect 9876543210</code>"
            ),
            parse_mode=ParseMode.HTML,
        )
        return

    number = _clean_number(msg.command[1])
    if not number.isdigit() or not (7 <= len(number) <= 15):
        await msg.reply(
            bq("❌ <b>Invalid number format.</b>\n\nPlease send digits only."),
            parse_mode=ParseMode.HTML,
        )
        return

    added = await protect_number(number)
    if added:
        await msg.reply(
            bq(
                f"✅ <b>Number Protected!</b>\n\n"
                f"📱 <code>{number}</code> has been added to the protected list.\n\n"
                f"No one can search this number on the bot anymore.\n\n"
                f"👨‍💻 <b>Owner:</b> MADARA DEFAULTER"
            ),
            parse_mode=ParseMode.HTML,
        )
    else:
        await msg.reply(
            bq(f"⚠️ <b>Already Protected</b>\n\n<code>{number}</code> is already in the protected list."),
            parse_mode=ParseMode.HTML,
        )


@app.on_message(filters.command("unprotect") & filters.private & filters.user(OWNER_ID))
async def cmd_unprotect(client, msg):
    if len(msg.command) < 2:
        await msg.reply(
            bq(
                "🔓 <b>Unprotect a Number</b>\n\n"
                "Usage: <code>/unprotect &lt;number&gt;</code>\n\n"
                "Example: <code>/unprotect 9876543210</code>"
            ),
            parse_mode=ParseMode.HTML,
        )
        return

    number = _clean_number(msg.command[1])
    removed = await unprotect_number(number)
    if removed:
        await msg.reply(
            bq(
                f"🔓 <b>Protection Removed</b>\n\n"
                f"<code>{number}</code> can now be searched again.\n\n"
                f"👨‍💻 <b>Owner:</b> MADARA DEFAULTER"
            ),
            parse_mode=ParseMode.HTML,
        )
    else:
        await msg.reply(
            bq(f"⚠️ <b>Not Found</b>\n\n<code>{number}</code> was not in the protected list."),
            parse_mode=ParseMode.HTML,
        )


@app.on_message(filters.command("protectedlist") & filters.private & filters.user(OWNER_ID))
async def cmd_protected_list(client, msg):
    numbers = await list_protected()
    if not numbers:
        await msg.reply(
            bq("📋 <b>Protected Numbers</b>\n\nNo numbers are protected yet."),
            parse_mode=ParseMode.HTML,
        )
        return

    lines = "\n".join(f"• <code>{n}</code>" for n in numbers)
    await msg.reply(
        bq(
            f"📋 <b>Protected Numbers ({len(numbers)})</b>\n\n"
            f"{lines}\n\n"
            f"Use /unprotect &lt;number&gt; to remove any."
        ),
        parse_mode=ParseMode.HTML,
    )
