from telethon import TelegramClient
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.dispatcher.filters.state import State, StatesGroup
from States import PostgresStateStorage
import asyncpg

async def on_startup(dp):
    await bot.set_my_commands([
        BotCommand("start", "Запустить бота")
    ])
#heroku
# DATABASE_CONFIG = {
#     'host': 'ec2-107-22-101-0.compute-1.amazonaws.com',
#     'database': 'd4b75m92odhd5r',
#     'user': 'qddmpqnjnjtntp',
#     'password': '9483a873f26ab8fc04d1c0f3585bd222b58ca4777cda8ecd4fbec733028140c5',
#     'port': '5432',
#     'ssl': 'require'
# }

#gcloud
DATABASE_CONFIG = {
    'host': '34.146.128.18',
    'database': 'postgres',
    'user': 'postgres',
    'password': 's4kUp3Nc1rCl3s&',
    'port': '5432'
}

async def add_new_user(user_id):
    conn = await create_connection()

    await conn.execute('''
        INSERT INTO user_settings (user_id) 
        VALUES ($1) ON CONFLICT (user_id) DO NOTHING
    ''', user_id)

    await conn.close()

api_id = "29699799"
api_hash = "2a66f255418ff322d2750d346ab9f111"
bot_token = "6574243823:AAGYzYFSDjIpXvmk2J8jh5qIkjROGB4CH6M"
#bot_token = "6319819956:AAHoObcErD2bZ_Fg8n68dx8jF0YsMKftkhk"

scan_bot = TelegramClient('scan_bot', api_id, api_hash)
ag_bot = TelegramClient('ag_bot', api_id, api_hash)
add_bot = TelegramClient('add_bot', api_id, api_hash)

bot = Bot(token=bot_token)
storage = PostgresStateStorage(**DATABASE_CONFIG)
dp = Dispatcher(bot, storage=storage)

async def create_connection():
    return await asyncpg.connect(**DATABASE_CONFIG)

class DB:
    async def __aenter__(self):
        self.conn = await create_connection()
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()


class UserState(StatesGroup):
    menu = State()
    autoposting = State()
    wait_links = State()
    schedule = State()

storage_id= -1002037895749

from gcloud.aio.storage import Storage
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Google Cloud Storage APIs.json"

async def gcs(file_path):
    async with Storage() as storage_client:
        bucket_name = "dda-scanner"
        blob_name = "post_images/" + file_path.split('/')[-1]
        await storage_client.upload(bucket_name, blob_name, file_path)
        url = f"https://storage.googleapis.com/{bucket_name}/{blob_name}"
        return url
