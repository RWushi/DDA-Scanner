from Config import bot, dp, UserState, DB
from aiogram.types import CallbackQuery

@dp.callback_query_handler(text_startswith='delete_dm:', state=UserState.autoposting)
async def delete_dm(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    command, rest = callback_query.data.split(":", 1)
    post_id, copied_message_id = rest.split("_", 1)

    async with DB() as conn:
        await conn.execute('DELETE FROM default_messages WHERE post_id = $1 AND user_id = $2', int(post_id), user_id)

    await bot.delete_message(chat_id=user_id, message_id=copied_message_id)
    await bot.delete_message(chat_id=user_id, message_id=int(callback_query.message.message_id))

    await bot.send_message(callback_query.from_user.id, f"Шаблон №{post_id} удалён")


@dp.callback_query_handler(text_startswith='delete_mg:', state=UserState.autoposting)
async def delete_mg(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    command, rest = callback_query.data.split(":", 1)
    post_id, message_ids_str = rest.split("_", 1)
    message_ids = list(map(int, message_ids_str.split('_')))

    async with DB() as conn:
        await conn.execute('DELETE FROM media_groups WHERE post_id = $1 AND user_id = $2', int(post_id), user_id)

    for message_id in message_ids:
        await bot.delete_message(chat_id=user_id, message_id=message_id)
    await bot.delete_message(chat_id=user_id, message_id=int(callback_query.message.message_id))

    await bot.send_message(callback_query.from_user.id, f"Шаблон №{post_id} удалён")