import aiosqlite, os, asyncio
from dotenv import load_dotenv

load_dotenv()
db_name = os.getenv("db_name")

async def init_db() -> None:
    async with aiosqlite.connect(db_name) as db:
        await db.execute('CREATE TABLE IF NOT EXISTS "users" (user_id INTEGER PRIMARY KEY, name TEXT, call TEXT)')
        await db.execute('CREATE TABLE IF NOT EXISTS "games" (number INTEGER, user_id INTEGER, date TEXT, club TEXT, type TEXT, PRIMARY KEY (user_id, number))')
        await db.commit()

async def search_user(user_id: int) -> bool:
    async with aiosqlite.connect(db_name) as db:
        async with db.execute('SELECT 1 FROM "users" WHERE user_id=?', (user_id, )) as cursor:
            row = await cursor.fetchone()
            return row is not None

async def registration_user(user_id: int, user_name: str, user_call: str) -> None:
    async with aiosqlite.connect(db_name) as db:
        await db.execute('INSERT INTO users (user_id, name, call) VALUES (?, ?, ?)', (user_id, user_name, user_call))
        await db.commit()

async def get_user_info(user_id: int) -> tuple:
    async with aiosqlite.connect(db_name) as db:
        async with db.execute('SELECT * FROM users WHERE user_id=?', (user_id, )) as cursor:
            row = await cursor.fetchone()
            return row

async def save_game(user_id: int, game_date: str, club: str, game_type: str) -> None:
    async with aiosqlite.connect(db_name) as db:
        async with db.execute('SELECT MAX(number) FROM games WHERE user_id=?', (user_id, )) as cursor:
            row = await cursor.fetchone()
            next_num = int((row[0]) or 0) + 1

        await db.execute('INSERT INTO games (number, user_id, date, club, type) VALUES (?, ?, ?, ?, ?)', (next_num, user_id, game_date, club, game_type))
        await db.commit()