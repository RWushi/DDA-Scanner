from aiogram.types import Message
from Config import dp, bot, UserState
from Keyboards import wait_links_kb
from JoinGroups import join_groups
import re, asyncio

async def wait_links(chat_id):
    await bot.send_message(chat_id, text = "Отправьте список групп, в которые нужно вступить", reply_markup = wait_links_kb)

@dp.message_handler(lambda message: message.text == "Посмотреть инструкцию💡", state=UserState.wait_links)
async def wait_links_start(message: Message):
    instruction = """
    Вам нужно отправить сообщение с ссылками на группы в формате:
https://t.me/group1
https://t.me/group2
https://t.me/group3
https://t.me/group4
...
    """
    await bot.send_message(message.chat.id, instruction)

@dp.message_handler(lambda message: message.text.startswith("https://t.me/"), state=UserState.wait_links)
async def handle_groups_links(message: Message):
    links = re.findall(r'https://t\.me/\S+', message.text)
    num = len(links)

    if num == 0:
        await bot.send_message(message.from_user.id, "Ссылки введены неправильно, попробуйте еще раз или вернитесь назад")
        return

    time = num * 3

    asyncio.create_task(join_groups(message.chat.id, links))
    await bot.send_message(message.from_user.id, f"Процесс начался. Максимальное время выполнения: {time} минут(ы|а)")