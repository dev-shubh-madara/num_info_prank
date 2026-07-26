"""
MADARA DEFAULTER Prank Bot — Database layer
All async functions use aiosqlite; init_db() is sync (called before app.run()).
"""
import sqlite3
import aiosqlite
from datetime import date

from config import DB_PATH, DAILY_FREE, OWNER_ID


# ══════════════════════════════════════════════════════════════════════════════
#  INIT  (synchronous — called once before event loop starts)
# ══════════════════════════════════════════════════════════════════════════════

def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id         INTEGER PRIMARY KEY,
                username        TEXT,
                first_name      TEXT,
                referred_by     INTEGER DEFAULT NULL,
                bonus_searches  INTEGER DEFAULT 0,
                joined_at       TEXT    DEFAULT (date('now'))
            );

            CREATE TABLE IF NOT EXISTS daily_usage (
                user_id     INTEGER,
                usage_date  TEXT,
                count       INTEGER DEFAULT 0,
                PRIMARY KEY (user_id, usage_date)
            );

            CREATE TABLE IF NOT EXISTS referrals (
                referred_id  INTEGER PRIMARY KEY,
                referrer_id  INTEGER,
                created_at   TEXT DEFAULT (date('now'))
            );

            CREATE TABLE IF NOT EXISTS protected_numbers (
                number      TEXT PRIMARY KEY,
                added_at    TEXT DEFAULT (date('now'))
            );
        """)


# ══════════════════════════════════════════════════════════════════════════════
#  USER HELPERS
# ══════════════════════════════════════════════════════════════════════════════

async def upsert_user(user_id: int, username: str | None, first_name: str) -> dict:
    today = date.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?,?,?)",
            (user_id, username, first_name),
        )
        await db.commit()
        async with db.execute(
            "SELECT * FROM users WHERE user_id=?", (user_id,)
        ) as cur:
            user = dict(await cur.fetchone())
        async with db.execute(
            "SELECT count FROM daily_usage WHERE user_id=? AND usage_date=?",
            (user_id, today),
        ) as cur:
            row = await cur.fetchone()
            user["daily_used"] = row[0] if row else 0
    return user


async def credit_referrer(referrer_id: int, referred_id: int) -> bool:
    """Returns True if first-time referral was credited."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT 1 FROM referrals WHERE referred_id=?", (referred_id,)
        ) as cur:
            if await cur.fetchone():
                return False
        await db.execute(
            "INSERT INTO referrals (referred_id, referrer_id) VALUES (?,?)",
            (referred_id, referrer_id),
        )
        await db.execute(
            "UPDATE users SET bonus_searches = bonus_searches + 1 WHERE user_id=?",
            (referrer_id,),
        )
        await db.commit()
    return True


async def referral_count(user_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT COUNT(*) FROM referrals WHERE referrer_id=?", (user_id,)
        ) as cur:
            row = await cur.fetchone()
            return row[0] if row else 0


async def spend_search(user_id: int, daily_used: int) -> None:
    today = date.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT INTO daily_usage (user_id, usage_date, count) VALUES (?,?,1)
               ON CONFLICT(user_id, usage_date) DO UPDATE SET count = count + 1""",
            (user_id, today),
        )
        if daily_used >= DAILY_FREE:          # burning a bonus slot
            await db.execute(
                "UPDATE users SET bonus_searches = MAX(0, bonus_searches - 1) WHERE user_id=?",
                (user_id,),
            )
        await db.commit()


def has_searches(user: dict) -> bool:
    """Owner always has unlimited searches."""
    if user["user_id"] == OWNER_ID:
        return True
    return user["daily_used"] < DAILY_FREE or user["bonus_searches"] > 0


def remaining(user: dict) -> int:
    """Returns remaining searches for today (∞ for owner)."""
    if user["user_id"] == OWNER_ID:
        return 9999
    free_left  = max(0, DAILY_FREE - user["daily_used"])
    bonus_used = max(0, user["daily_used"] - DAILY_FREE)
    bonus_left = max(0, user["bonus_searches"] - bonus_used)
    return free_left + bonus_left


# ══════════════════════════════════════════════════════════════════════════════
#  PROTECTED NUMBERS
# ══════════════════════════════════════════════════════════════════════════════

async def is_protected(number: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT 1 FROM protected_numbers WHERE number=?", (number,)
        ) as cur:
            return await cur.fetchone() is not None


async def protect_number(number: str) -> bool:
    """Add a number to the protected list. Returns False if already protected."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT 1 FROM protected_numbers WHERE number=?", (number,)
        ) as cur:
            if await cur.fetchone():
                return False
        await db.execute(
            "INSERT INTO protected_numbers (number) VALUES (?)", (number,)
        )
        await db.commit()
    return True


async def unprotect_number(number: str) -> bool:
    """Remove a number from the protected list. Returns False if not found."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT 1 FROM protected_numbers WHERE number=?", (number,)
        ) as cur:
            if not await cur.fetchone():
                return False
        await db.execute(
            "DELETE FROM protected_numbers WHERE number=?", (number,)
        )
        await db.commit()
    return True


async def list_protected() -> list[str]:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT number FROM protected_numbers ORDER BY added_at DESC"
        ) as cur:
            rows = await cur.fetchall()
            return [r[0] for r in rows]
