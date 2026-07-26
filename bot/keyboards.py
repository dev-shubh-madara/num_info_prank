"""
MADARA DEFAULTER Prank Bot — Keyboard layouts
Uses Kurigram's ButtonStyle for colored inline buttons.
"""
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ButtonStyle

from config import GROUP_LINK


def kb_main() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔗 Referral",        callback_data="referral",     style=ButtonStyle.SUCCESS),
            InlineKeyboardButton("💳 My Credits",      callback_data="credits",      style=ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton("🌐 My Network",      callback_data="network",      style=ButtonStyle.PRIMARY),
            InlineKeyboardButton("👥 My Group",        url=GROUP_LINK,               style=ButtonStyle.SUCCESS),
        ],
        [
            InlineKeyboardButton("👨‍💻 Developer",       callback_data="developer",    style=ButtonStyle.DANGER),
            InlineKeyboardButton("🔍 Search Number",   callback_data="search",       style=ButtonStyle.SUCCESS),
        ],
        [
            InlineKeyboardButton("🛡️ Protect Number",   callback_data="protect_info", style=ButtonStyle.DANGER),
            InlineKeyboardButton("🔥 Unlimited Search", callback_data="unlimited",    style=ButtonStyle.SUCCESS),
        ],
    ])


def kb_back() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🏠 Back to Home", callback_data="home", style=ButtonStyle.PRIMARY),
    ]])


def kb_join() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👥 Join Group",           url=GROUP_LINK,              style=ButtonStyle.SUCCESS)],
        [InlineKeyboardButton("✅ I've Joined — Check",  callback_data="check_join",  style=ButtonStyle.PRIMARY)],
    ])


def kb_cancel() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("❌ Cancel", callback_data="home", style=ButtonStyle.DANGER),
    ]])


def kb_refer_home() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Get Referral Link", callback_data="referral", style=ButtonStyle.SUCCESS)],
        [InlineKeyboardButton("🏠 Back to Home",      callback_data="home",     style=ButtonStyle.PRIMARY)],
    ])
