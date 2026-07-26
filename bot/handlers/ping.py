"""
Handler: /ping command
Shows bot uptime with a banner image in blockquote caption.
"""
import time
import os
from pyrogram import filters
from pyrogram.enums import ParseMode

from client import app
from helpers import bq

# Record start time when module is imported
_START_TIME = time.time()

PING_BANNER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "ping_banner.jpg")


def _fmt_uptime(seconds: float) -> str:
    s = int(seconds)
    days, s    = divmod(s, 86400)
    hours, s   = divmod(s, 3600)
    minutes, s = divmod(s, 60)
    parts = []
    if days:    parts.append(f"{days}d")
    if hours:   parts.append(f"{hours}h")
    if minutes: parts.append(f"{minutes}m")
    parts.append(f"{s}s")
    return " ".join(parts)


@app.on_message(filters.command("ping") & filters.private)
async def cmd_ping(client, msg):
    uptime = _fmt_uptime(time.time() - _START_TIME)
    caption = bq(
        f"🏓 <b>PONG!</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⏱️ <b>Uptime:</b> {uptime}\n"
        f"⚡ <b>Status:</b> Online ✅\n"
        f"🔧 <b>Engine:</b> Kurigram (Python)\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👨‍💻 <b>Developer:</b> MADARA DEFAULTER\n"
        f"🏷️ <b>Brand:</b> MADARA X BRAND"
    )
    await client.send_photo(
        chat_id=msg.chat.id,
        photo=PING_BANNER,
        caption=caption,
        parse_mode=ParseMode.HTML,
    )
