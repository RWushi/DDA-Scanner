from telethon.tl.functions.channels import JoinChannelRequest, GetParticipantRequest
from telethon import errors
from Config import bot, add_bot
import asyncio

async def join_groups(chat_id, links):
    success_count = 0
    failed_count = 0
    already_member_count = 0

    async with add_bot as client:
        me = await client.get_me()
        for link in links:
            try:
                entity = await client.get_entity(link)
                try:
                    participant = await client(GetParticipantRequest(channel=entity, participant=me.id))
                    already_member_count += 1
                except errors.UserNotParticipantError:
                    await client(JoinChannelRequest(entity))
                    success_count += 1
                    await asyncio.sleep(180)

            except Exception as e:
                failed_count += 1
                continue

    try:
        await bot.send_message(chat_id, f"Процесс завершен! Добавлено: {success_count}. Не удалось добавить: {failed_count}. Уже учавствовали: {already_member_count}.")
    except Exception as e:
        pass
