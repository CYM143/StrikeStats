import asyncio
from telebot import asyncio_filters

from loader import bot
from database import init_db
import handlers

async def main():
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    await init_db()
    print("Bot is now online !")
    await bot.infinity_polling(timeout=30)

if __name__ == "__main__":
    asyncio.run(main())