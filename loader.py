import os
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage


load_dotenv()

state_storage = StateMemoryStorage()
bot = AsyncTeleBot(os.getenv("API"), state_storage=state_storage)