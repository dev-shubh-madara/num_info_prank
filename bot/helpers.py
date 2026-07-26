"""
MADARA DEFAULTER Prank Bot — Shared helpers
"""
import asyncio
import aiohttp
import logging

from pyrogram import Client
from pyrogram.enums import ParseMode

from config import GROUP_ID, SEARCH_API, SEARCH_KEY

log = logging.getLogger("MadaraBot")


def bq(text: str) -> str:
    """Wrap text in a Telegram blockquote tag."""
    return f"<blockquote>{text}</blockquote>"


async def member_check(client: Client, user_id: int) -> bool:
    try:
        m = await client.get_chat_member(GROUP_ID, user_id)
        return m.status.name not in ("LEFT", "BANNED", "KICKED")
    except Exception:
        return False


async def api_search(mobile: str) -> dict | None:
    url = f"{SEARCH_API}?api_key={SEARCH_KEY}&mobile={mobile}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=12)) as r:
                if r.status != 200:
                    return None
                body = await r.json(content_type=None)
        if body.get("status") != "success":
            return None
        rows = body.get("data") or []
        return rows[0] if rows else None
    except Exception as exc:
        log.warning("API error: %s", exc)
        return None


async def schedule_delete(client: Client, chat_id: int, msg_id: int,
                          phone: str, delay: int = 120) -> None:
    await asyncio.sleep(delay)
    try:
        await client.delete_messages(chat_id, msg_id)
        await client.send_message(
            chat_id,
            bq(f"🗑️ <i>Details for <code>{phone}</code> have been automatically deleted.</i>"),
            parse_mode=ParseMode.HTML,
        )
    except Exception:
        pass
