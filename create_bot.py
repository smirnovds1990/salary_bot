import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from motor import motor_asyncio


load_dotenv()

TOKEN = os.getenv('TOKEN')
DATABASE_URI = os.getenv('DATABASE_URI')
bot = Bot(token=TOKEN)
dp = Dispatcher()
client = motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
db = client.sampleDB.sample_collection
