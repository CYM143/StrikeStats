import asyncio
from telebot import asyncio_filters

from loader import bot
from database import init_db
from logger import logger
import handlers

async def main():
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    logger.info("Bot add custom filter")
    await init_db()
    logger.info("Bot init database")
    logger.info("Bot started succesful")
    await bot.infinity_polling(timeout=30)

if __name__ == "__main__":
    asyncio.run(main())