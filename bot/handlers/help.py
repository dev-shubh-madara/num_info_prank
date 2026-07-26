"""
Handler: /help command
"""
from pyrogram import filters
from pyrogram.enums import ParseMode

from client import app
from config import DAILY_FREE
from helpers import bq
from keyboards import kb_main


@app.on_message(filters.command("help") & filters.private)
async def cmd_help(client, msg):
    await msg.reply(
        bq(
            "📖 <b>Help — MADARA DEFAULTER Bot</b>\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🔍 <b>Search:</b> Press Search Number button\n"
            "🔗 <b>Referral:</b> Share your link for bonus searches\n"
            "💳 <b>Credits:</b> Check your search balance\n"
            "🌐 <b>Network:</b> See your referral stats\n"
            "🛡️ <b>Protect:</b> Hide your number from searches\n\n"
            f"📊 <b>Limits:</b> {DAILY_FREE} free searches/day + bonus from referrals\n\n"
            "👨‍💻 <b>Developer:</b> MADARA DEFAULTER\n"
            "🏷️ <b>Brand:</b> MADARA X BRAND"
        ),
        parse_mode=ParseMode.HTML,
        reply_markup=kb_main(),
    )
