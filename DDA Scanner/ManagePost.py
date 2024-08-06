from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from Config import bot, DB, storage_id
import DeletePost

async def show_post(message):
    user_id = message.from_user.id

    async with DB() as conn:
        default_messages = await conn.fetch('SELECT post_id, message_id FROM default_messages WHERE user_id = $1', user_id)
        media_groups = await conn.fetch('SELECT post_id, text, file_ids FROM media_groups WHERE user_id = $1', user_id)

    if not default_messages and not media_groups:
        await message.answer("У вас нет активных шаблонов")
        return

    for default_message in default_messages:
        post_id = default_message['post_id']
        storage_message_id = default_message['message_id']

        copied_message = await bot.copy_message(chat_id=user_id, from_chat_id=storage_id, message_id=storage_message_id)
        copied_message_id = copied_message.message_id

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Удалить шаблон❌", callback_data=f"delete_dm:{post_id}_{copied_message_id}"))
        markup.add(InlineKeyboardButton("Расписание шаблона⏱", callback_data=f"schedule:{post_id}"))

        await message.answer(f"Шаблон №{post_id} выше", reply_markup=markup)

    for media_group in media_groups:
        post_id = media_group['post_id']
        text = media_group['text']
        file_ids = media_group['file_ids']

        media = [InputMediaPhoto(file_id) for file_id in file_ids]

        if text:
            media[0].caption = text

        sent_messages = await bot.send_media_group(chat_id=user_id, media=media)
        message_ids = [msg.message_id for msg in sent_messages]

        markup = InlineKeyboardMarkup()
        message_ids_str = '_'.join(map(str, message_ids))
        markup.add(InlineKeyboardButton("Удалить шаблон❌", callback_data=f"delete_mg:{post_id}_{message_ids_str}"))
        markup.add(InlineKeyboardButton("Расписание шаблона⏱", callback_data=f"schedule:{post_id}"))

        await message.answer(f"Шаблон №{post_id} выше", reply_markup=markup)
