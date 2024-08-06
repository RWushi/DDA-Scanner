from Config import bot, scan_bot
from Scanbot import scan_id
import asyncio


async def scanning(chat_id1, chat_id2):
    await scan_id(chat_id1, chat_id2)

    asyncio.create_task(start_scanbot())

    await bot.send_message(chat_id=chat_id1, text="Сканирование началось, ждите сообщения")
    await bot.send_message(chat_id=chat_id2, text="Сканирование началось, ждите сообщения")

async def start_scanbot():
    await scan_bot.start()
    await scan_bot.run_until_disconnected()
