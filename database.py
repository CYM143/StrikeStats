import aiosqlite, os, asyncio
from dotenv import load_dotenv

load_dotenv()
db_name = os.getenv("db_name")

async def init_db() -> None:
    async with aiosqlite.connect(db_name) as db:
        await db.execute('CREATE TABLE IF NOT EXISTS "users" (user_id INTEGER PRIMARY KEY, name TEXT, call TEXT)')
        await db.execute('CREATE TABLE IF NOT EXISTS "games" (user_id INTEGER, date TEXT, club TEXT, type TEXT)')
        await db.execute('CREATE TABLE IF NOT EXISTS "msg_ids" (user_id INTEGER, message_id INTEGER)')
        await db.commit()

async def search_user(user_id: int) -> bool:
    async with aiosqlite.connect(db_name) as db:
        async with db.execute('SELECT 1 FROM "users" WHERE user_id=?', (user_id, )) as cursor:
            row = await cursor.fetchone()
            return row if row is not None else False

async def registration_user(user_id: int, user_name: str, user_call: str) -> None:
    async with aiosqlite.connect(db_name) as db:
        await db.execute('INSERT INTO users (user_id, name, call) VALUES (?, ?, ?)', (user_id, user_name, user_call))
        await db.commit()

async def change_name_user(user_id: int, new_name: str) -> None:
    async with aiosqlite.connect(db_name) as db:
        await db.execute('UPDATE users SET name = ? WHERE user_id = ?', (new_name, user_id))
        await db.commit()

async def change_call_user(user_id: int, new_call: str) -> None:
    async with aiosqlite.connect(db_name) as db:
        await db.execute('UPDATE users SET call = ? WHERE user_id = ?', (new_call, user_id))
        await db.commit()

async def get_user_info(user_id: int) -> tuple:
    async with aiosqlite.connect(db_name) as db:
        async with db.execute('SELECT * FROM users WHERE user_id=?', (user_id, )) as cursor:
            row = await cursor.fetchone()
            return row

async def save_game(user_id: int, game_date: str, club: str, game_type: str) -> None:
    async with aiosqlite.connect(db_name) as db:
        await db.execute('INSERT INTO games (user_id, date, club, type) VALUES (?, ?, ?, ?)', (user_id, game_date, club, game_type))
        await db.commit()

async def get_user_games(user_id: int) -> tuple:
    async with aiosqlite.connect(db_name) as db:
        async with db.execute('SELECT * FROM games WHERE user_id = ?', (user_id, )) as cursor:
            row = await cursor.fetchall()
            return list(row)

async def save_user_message_id(user_id: int, msg_id: int):
    async with aiosqlite.connect(db_name) as db:
        await db.execute("INSERT INTO msg_ids (user_id, message_id) VALUES (?, ?)", (user_id, msg_id))
        await db.commit()

async def load_user_message_id(user_id: int) -> int:
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT message_id FROM msg_ids WHERE user_id = ?", (user_id, )) as cursor:
            raw = await cursor.fetchone()
            return raw[0]

async def remove_user_message_id(user_id: int):
    async with aiosqlite.connect(db_name) as db:
        await db.execute("DELETE FROM msg_ids WHERE user_id = ?", (user_id, ))
        await db.commit()