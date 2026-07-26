"""
Shared Pyrogram / Kurigram client instance.
Import `app` from here in every handler file so decorators register correctly.
"""
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "madara_session",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)
