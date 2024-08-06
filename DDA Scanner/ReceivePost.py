from Config import bot, create_connection, storage_id
import asyncpg


async def mg_check(message):
    user_id = message.from_user.id
    conn = await create_connection()

    if message.media_group_id:
        media_group_id = int(message.media_group_id)
        try:
            new_post_id = await get_post_id(user_id, conn)
            await conn.execute(
                "INSERT INTO media_groups (media_id, user_id, post_id) VALUES ($1, $2, $3)",
                media_group_id, user_id, new_post_id
            )
            await create_mg(message, new_post_id, conn)
        except asyncpg.UniqueViolationError:
            existing_post_id = await conn.fetchval(
                "SELECT post_id FROM media_groups WHERE user_id = $1 AND media_id = $2",
                user_id, media_group_id
            )
            await add_to_mg(message, existing_post_id, conn)

    else:
        new_post_id = await get_post_id(user_id, conn)
        if new_post_id is not None:
            await receive_dm(message, new_post_id, conn)
        else:
            await message.answer("Вы достигли лимита, удалите 1 из существующих шаблонов и повторите попытку")

    await conn.close()


async def get_post_id(user_id, conn):
    records_default = await conn.fetch('SELECT post_id FROM default_messages WHERE user_id = $1', user_id)
    records_media = await conn.fetch('SELECT post_id FROM media_groups WHERE user_id = $1', user_id)
    existing_ids = [record['post_id'] for record in records_default] + [record['post_id'] for record in records_media]

    for i in range(1, 11):
        if i not in existing_ids:
            return i
    return None


async def receive_dm(message, post_id, conn):
    user_id = message.from_user.id
    text = message.caption if message.caption else None
    copied_message = await bot.copy_message(chat_id=storage_id, from_chat_id=message.chat.id, message_id=message.message_id)
    storage_message_id = copied_message.message_id
    await conn.execute("INSERT INTO default_messages (user_id, post_id, message_id, text) VALUES ($1, $2, $3, $4)", user_id, post_id, storage_message_id, text)
    await conn.close()
    await message.answer("Шаблон принят")


async def add_to_mg(message, post_id, conn):
    user_id = message.from_user.id

    file_id = message.photo[-1].file_id
    await bot.send_photo(chat_id=storage_id, photo=file_id)

    await conn.execute(
        "UPDATE media_groups SET file_ids = array_append(file_ids, $1) WHERE user_id = $2 AND post_id = $3",
        file_id, user_id, post_id
    )

    await conn.close()
    await message.answer("Медиа группа пополнена")


async def create_mg(message, new_post_id, conn):
    user_id = message.from_user.id

    text = message.caption if message.caption else None
    file_id = message.photo[-1].file_id
    await bot.send_photo(chat_id=storage_id, photo=file_id)

    await conn.execute(
        "UPDATE media_groups SET text = $3, file_ids = $4 WHERE user_id = $1 AND post_id = $2",
        user_id, new_post_id, text, [file_id]
    )

    await conn.close()
    await message.answer("Медиа группа создана")
