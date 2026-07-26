"""
Handler: /start command
Handles referral tracking, force-join gate, and sends start banner photo.
"""
import os
from pyrogram import filters
from pyrogram.enums import ParseMode

from client import app
from database import upsert_user, credit_referrer
from helpers import member_check, bq
from templates import txt_start, txt_not_joined
from keyboards import kb_main, kb_join

START_BANNER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "start_banner.jpg")


@app.on_message(filters.command("start") & filters.private)
async def cmd_start(client, msg):
    user = msg.from_user
    args = msg.command[1] if len(msg.command) > 1 else ""

    # ── Referral tracking ──────────────────────────────────────────────────
    referrer_id = None
    if args.startswith("ref_"):
        try:
            rid = int(args[4:])
            if rid != user.id:
                referrer_id = rid
        except ValueError:
            pass

    await upsert_user(user.id, user.username, user.first_name or "User")

    if referrer_id:
        credited = await credit_referrer(referrer_id, user.id)
        if credited:
            try:
                await client.send_message(
                    referrer_id,
                    bq(
                        "🎉 <b>New Referral!</b>\n\n"
                        "Someone joined using your link.\n"
                        "You earned <b>+1 permanent bonus search!</b>\n\n"
                        "👨‍💻 <b>Developer:</b> MADARA DEFAULTER"
                    ),
                    parse_mode=ParseMode.HTML,
                )
            except Exception:
                pass

    # ── Force-join gate ───────────────────────────────────────────────────
    if not await member_check(client, user.id):
        await client.send_photo(
            chat_id=msg.chat.id,
            photo=START_BANNER,
            caption=txt_not_joined(),
            parse_mode=ParseMode.HTML,
            reply_markup=kb_join(),
        )
        return

    # ── Welcome with banner ───────────────────────────────────────────────
    await client.send_photo(
        chat_id=msg.chat.id,
        photo=START_BANNER,
        caption=txt_start(user.first_name or "User"),
        parse_mode=ParseMode.HTML,
        reply_markup=kb_main(),
    )
