"""
MADARA DEFAULTER Prank Bot — Message templates
All messages are wrapped in <blockquote> via bq().
"""
from config import DAILY_FREE, GROUP_LINK
from helpers import bq


def txt_start(name: str) -> str:
    return bq(
        f"👋 <b>Hello, {name}!</b>\n\n"
        f"Welcome to <b>MADARA DEFAULTER</b> Prank Bot 🔥\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎭 Send any mobile number and I'll fetch prank details!\n\n"
        f"📊 <b>Daily Plan:</b>\n"
        f"• 🆓 {DAILY_FREE} free searches every day\n"
        f"• 🔗 +1 permanent search per referral\n"
        f"• 🛡️ Protect your number from being searched\n\n"
        f"⬇️ <b>Tap a button below to get started:</b>"
    )


def txt_not_joined() -> str:
    return bq(
        "🚫 <b>Access Denied!</b>\n\n"
        "You must join our group before using this bot.\n\n"
        "1️⃣ Press <b>Join Group</b> below\n"
        "2️⃣ Then press <b>✅ I've Joined</b> to verify\n\n"
        "👥 <b>Group:</b> MADARA X BRAND\n"
        "👨‍💻 <b>Developer:</b> MADARA DEFAULTER"
    )


def txt_referral(user_id: int, bot_username: str, refs: int, bonus: int) -> str:
    link = f"https://t.me/{bot_username}?start=ref_{user_id}"
    return bq(
        f"🔗 <b>Your Referral Link</b>\n\n"
        f"<code>{link}</code>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 <b>Total Referrals:</b> {refs}\n"
        f"🎁 <b>Bonus Searches Earned:</b> {bonus}\n\n"
        f"📢 Share your link — every successful referral\n"
        f"gives you <b>+1 permanent bonus search!</b>\n\n"
        f"👨‍💻 <b>Developer:</b> MADARA DEFAULTER\n"
        f"🏷️ <b>Brand:</b> MADARA X BRAND"
    )


def txt_credits(user: dict) -> str:
    from database import remaining
    rem = remaining(user)
    rem_display = "∞ (Owner)" if rem == 9999 else rem
    return bq(
        f"💳 <b>My Search Credits</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🆓 <b>Free/Day:</b> {DAILY_FREE}\n"
        f"🎁 <b>Bonus Balance:</b> {user['bonus_searches']}\n"
        f"📊 <b>Used Today:</b> {user['daily_used']}\n"
        f"✅ <b>Remaining Today:</b> {rem_display}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 Refer friends to earn permanent bonus searches!\n\n"
        f"👨‍💻 <b>Developer:</b> MADARA DEFAULTER\n"
        f"🏷️ <b>Brand:</b> MADARA X BRAND"
    )


def txt_network(refs: int, bonus: int) -> str:
    return bq(
        f"🌐 <b>My Network</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 <b>People You Referred:</b> {refs}\n"
        f"🎁 <b>Bonus Searches Earned:</b> {bonus}\n\n"
        f"📈 Each referral = <b>1 permanent extra search</b>\n"
        f"Keep sharing your link to grow your limit!\n\n"
        f"🔗 <b>Group:</b> <a href=\"{GROUP_LINK}\">MADARA X BRAND</a>\n"
        f"👨‍💻 <b>Developer:</b> MADARA DEFAULTER"
    )


def txt_developer() -> str:
    return bq(
        f"👨‍💻 <b>Developer Info</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔥 <b>Developer:</b> MADARA DEFAULTER\n"
        f"🏷️ <b>Brand:</b> MADARA X BRAND\n"
        f"🔗 <b>Group:</b> <a href=\"{GROUP_LINK}\">Join Here</a>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ <i>This bot is for entertainment/pranking only.</i>\n"
        f"<i>All data shown is labelled as fake.</i>\n\n"
        f"💻 <b>Built with:</b> Kurigram (Python)"
    )


def txt_protect_info() -> str:
    return bq(
        f"🛡️ <b>Protect Your Number</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Want to hide your number from being searched on this bot?\n\n"
        f"Once protected, <b>no one</b> can look up that number — "
        f"the bot will refuse the search entirely.\n\n"
        f"📩 <b>How to request protection:</b>\n"
        f"Contact the bot owner via the group and share your number.\n"
        f"The owner will add it to the protected list.\n\n"
        f"🔗 <b>Group:</b> <a href=\"{GROUP_LINK}\">MADARA X BRAND</a>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👨‍💻 <b>Developer:</b> MADARA DEFAULTER\n"
        f"🏷️ <b>Brand:</b> MADARA X BRAND"
    )


def txt_awaiting_number(rem) -> str:
    rem_display = "∞ (Owner)" if rem == 9999 else rem
    return bq(
        f"🔍 <b>Enter Mobile Number</b>\n\n"
        f"Send the number you want to prank-search.\n\n"
        f"📌 <b>Example:</b> <code>9988776655</code>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ <b>Searches remaining today:</b> {rem_display}\n\n"
        f"⬇️ <i>Type the number and send it:</i>"
    )


def txt_limit_reached(user: dict, ref_link: str) -> str:
    return bq(
        f"🚫 <b>Daily Limit Reached!</b>\n\n"
        f"You've used all searches for today.\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🆓 <b>Free/Day:</b> {DAILY_FREE}\n"
        f"📊 <b>Used Today:</b> {user['daily_used']}\n"
        f"🎁 <b>Bonus Balance:</b> {user['bonus_searches']}\n\n"
        f"🔗 <b>Earn more by referring friends!</b>\n"
        f"1 referral = 1 permanent extra search 🎯\n\n"
        f"Your link:\n<code>{ref_link}</code>"
    )


def txt_result(mobile: str, d: dict) -> str:
    def v(k): return d.get(k) or "N/A"
    return bq(
        f"╔══════════════════════════╗\n"
        f"      🔍 USER DETAILS FOUND\n"
        f"╚══════════════════════════╝\n\n"
        f"📱 <b>Number:</b> <code>{mobile}</code>\n\n"
        f"👤 <b>Full Name:</b> {v('name')}\n"
        f"👨 <b>Father's Name:</b> {v('fname')}\n"
        f"🪪 <b>Aadhar No.:</b> <code>{v('aadhar')}</code>\n"
        f"📍 <b>Address:</b> {v('address')}\n"
        f"📡 <b>Circle / Operator:</b> {v('circle')}\n"
        f"📧 <b>Email:</b> {v('email')}\n"
        f"📞 <b>Alt. Number:</b> {v('alt')}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"⚠️ <b>DISCLAIMER:</b>\n"
        f"<i>These are FAKE details, NOT real information.\n"
        f"Made only for PRANKING people.\n"
        f"Do NOT misuse this data.</i>\n\n"
        f"👨‍💻 <b>Developer:</b> MADARA DEFAULTER\n"
        f"🏷️ <b>Credits:</b> MADARA X BRAND\n"
        f"🔗 <b>Group:</b> <a href=\"{GROUP_LINK}\">Join Here</a>\n\n"
        f"🗑️ <i>This message self-destructs in 2 minutes...</i>"
    )


def txt_unlimited_info() -> str:
    return bq(
        f"🔥 <b>Unlimited Searches — FREE!</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Want <b>unlimited</b> number searches at no cost?\n\n"
        f"📌 <b>How it works:</b>\n"
        f"1️⃣ Join our official group below\n"
        f"2️⃣ Inside the group, use the command:\n"
        f"   <code>/num &lt;number&gt;</code>\n"
        f"   Example: <code>/num 9988776655</code>\n\n"
        f"✅ Group members get <b>unlimited</b> searches\n"
        f"with no daily cap — completely free!\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👨‍💻 <b>Developer:</b> MADARA DEFAULTER\n"
        f"🏷️ <b>Brand:</b> MADARA X BRAND"
    )


def txt_protected_block(mobile: str) -> str:
    return bq(
        f"🛡️ <b>Number Protected</b>\n\n"
        f"The number <code>{mobile}</code> has been protected by the owner.\n\n"
        f"This number cannot be searched on this bot.\n\n"
        f"👨‍💻 <b>Developer:</b> MADARA DEFAULTER\n"
        f"🏷️ <b>Brand:</b> MADARA X BRAND"
    )
