"""
Handler: All inline keyboard callback queries
Force-join is checked on every feature callback.
"""
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ButtonStyle

from client import app
from config import WAITING, GROUP_LINK
from database import upsert_user, referral_count, has_searches, remaining
from helpers import member_check
from templates import (
    txt_start, txt_not_joined, txt_referral, txt_credits,
    txt_network, txt_developer, txt_protect_info, txt_unlimited_info,
    txt_awaiting_number, txt_limit_reached,
)
from keyboards import kb_main, kb_join, kb_back, kb_cancel, kb_refer_home


# ── Inline keyboard shown after join-prompt callbacks ─────────────────────────
def kb_unlimited() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👥 Join Group — Unlimited", url=GROUP_LINK, style=ButtonStyle.SUCCESS)],
        [InlineKeyboardButton("🏠 Back to Home", callback_data="home", style=ButtonStyle.PRIMARY)],
    ])


# ── Shared force-join gate for callbacks ──────────────────────────────────────
async def _gate(client, cb) -> bool:
    """Returns True if the user has joined the group; answers with alert if not."""
    if await member_check(client, cb.from_user.id):
        return True
    await cb.answer("🚫 You must join the group first! Press /start.", show_alert=True)
    return False


# ══════════════════════════════════════════════════════════════════════════════
#  CALLBACKS
# ══════════════════════════════════════════════════════════════════════════════

@app.on_callback_query(filters.regex("^check_join$"))
async def cb_check_join(client, cb):
    if await member_check(client, cb.from_user.id):
        u = cb.from_user
        await upsert_user(u.id, u.username, u.first_name or "User")
        await cb.message.edit_text(
            txt_start(u.first_name or "User"),
            reply_markup=kb_main(),
            parse_mode=ParseMode.HTML,
        )
        await cb.answer("✅ Verified! Welcome aboard.")
    else:
        await cb.answer("❌ Still not joined. Please join first!", show_alert=True)


@app.on_callback_query(filters.regex("^home$"))
async def cb_home(client, cb):
    WAITING.discard(cb.from_user.id)
    await cb.message.edit_text(
        txt_start(cb.from_user.first_name or "User"),
        reply_markup=kb_main(),
        parse_mode=ParseMode.HTML,
    )
    await cb.answer()


@app.on_callback_query(filters.regex("^referral$"))
async def cb_referral(client, cb):
    if not await _gate(client, cb):
        return
    u       = cb.from_user
    db_user = await upsert_user(u.id, u.username, u.first_name or "User")
    refs    = await referral_count(u.id)
    me      = await client.get_me()
    await cb.message.edit_text(
        txt_referral(u.id, me.username, refs, db_user["bonus_searches"]),
        reply_markup=kb_back(),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )
    await cb.answer()


@app.on_callback_query(filters.regex("^credits$"))
async def cb_credits(client, cb):
    if not await _gate(client, cb):
        return
    u       = cb.from_user
    db_user = await upsert_user(u.id, u.username, u.first_name or "User")
    await cb.message.edit_text(
        txt_credits(db_user),
        reply_markup=kb_back(),
        parse_mode=ParseMode.HTML,
    )
    await cb.answer()


@app.on_callback_query(filters.regex("^network$"))
async def cb_network(client, cb):
    if not await _gate(client, cb):
        return
    u       = cb.from_user
    db_user = await upsert_user(u.id, u.username, u.first_name or "User")
    refs    = await referral_count(u.id)
    await cb.message.edit_text(
        txt_network(refs, db_user["bonus_searches"]),
        reply_markup=kb_back(),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )
    await cb.answer()


@app.on_callback_query(filters.regex("^developer$"))
async def cb_developer(client, cb):
    if not await _gate(client, cb):
        return
    await cb.message.edit_text(
        txt_developer(),
        reply_markup=kb_back(),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )
    await cb.answer()


@app.on_callback_query(filters.regex("^protect_info$"))
async def cb_protect_info(client, cb):
    if not await _gate(client, cb):
        return
    await cb.message.edit_text(
        txt_protect_info(),
        reply_markup=kb_back(),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )
    await cb.answer()


@app.on_callback_query(filters.regex("^unlimited$"))
async def cb_unlimited(client, cb):
    await cb.message.edit_text(
        txt_unlimited_info(),
        reply_markup=kb_unlimited(),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )
    await cb.answer()


@app.on_callback_query(filters.regex("^search$"))
async def cb_search(client, cb):
    if not await _gate(client, cb):
        return
    u       = cb.from_user
    db_user = await upsert_user(u.id, u.username, u.first_name or "User")

    if not has_searches(db_user):
        me       = await client.get_me()
        ref_link = f"https://t.me/{me.username}?start=ref_{u.id}"
        await cb.message.edit_text(
            txt_limit_reached(db_user, ref_link),
            reply_markup=kb_refer_home(),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
        await cb.answer("❌ Daily limit reached! Refer to earn more.", show_alert=True)
        return

    WAITING.add(u.id)
    await cb.message.edit_text(
        txt_awaiting_number(remaining(db_user)),
        reply_markup=kb_cancel(),
        parse_mode=ParseMode.HTML,
    )
    await cb.answer()
