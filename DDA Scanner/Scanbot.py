from Config import scan_bot
from telethon import events
from Filter import message_filter
from Sending import send_message
from Repeat import add_hash, hash_filter

async def scan_id(chat_id1, chat_id2):
    @scan_bot.on(events.NewMessage)
    async def handler(event):

        if event.is_group and message_filter(event.message.text):
            chat = await event.get_chat()
            sender = await event.get_sender()

            message_text = event.message.text

            if await hash_filter(sender.id, message_text):
                await add_hash(sender.id, message_text)
            else:
                return

            chat_title = chat.title

            if sender.username:
                sender_link = f"https://t.me/{sender.username}"
                warning_message = ""
            else:
                sender_link = None
                warning_message = "\n\n" + "<strong>Внимание:</strong> у отправителя нет юзернейма"

            if chat.username:
                message_link = f"https://t.me/{chat.username}/{event.message.id}"
            else:
                message_link = f"https://t.me/c/{chat.id}/{event.message.id}"

            await send_message(chat_id1, chat_id2, chat_title, message_text, warning_message, sender_link, message_link)