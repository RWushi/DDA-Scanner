from Config import bot
from GetList import get_list

async def active_groups(chat_id):
    file_path, chats_count = await get_list()
    await bot.send_message(chat_id, f"Сохранено {chats_count} групп. Отправляется файл...")
    with open(file_path, 'rb') as file:
        await bot.send_document(chat_id, file)