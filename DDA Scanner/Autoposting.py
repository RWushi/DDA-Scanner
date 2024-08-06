from aiogram import types
from Config import dp, bot, UserState, DB
from aiogram.types import Message, ContentType, InputMediaPhoto
from ReceivePost import mg_check
from ManagePost import show_post
from Keyboards import autoposting_kb


async def autoposting(chat_id):
    await bot.send_message(chat_id, text="Отправьте пост или несколько постов (максимум 10)", reply_markup=autoposting_kb)

#Из раздела расписания
@dp.message_handler(lambda message: message.text == "Назад⏪", state=UserState.schedule)
async def schedule_finish(message: Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.autoposting.set()
    await autoposting(message.chat.id)

import Schedule

@dp.message_handler(lambda message: message.text == "Посмотреть пример💡", state=UserState.autoposting)
async def example(message: types.Message):
    user_id = message.from_user.id
    async with DB() as conn:
        example_photos = await conn.fetch('SELECT text, file_ids FROM post_example')
    for example_photo in example_photos:
        text = example_photo['text']
        file_ids = example_photo['file_ids']

        media = [InputMediaPhoto(file_id) for file_id in file_ids]
        media[0].caption = text

        await bot.send_media_group(chat_id=user_id, media=media)


@dp.message_handler(lambda message: message.text == "Управление шаблонами⚙️", state=UserState.autoposting)
async def manage_template(message: Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await show_post(message)


@dp.message_handler(content_types=ContentType.ANY, state=UserState.autoposting)
async def receive_template(message: Message):
    await mg_check(message)
