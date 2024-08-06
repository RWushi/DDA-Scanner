from Config import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def send_message(chat_id1, chat_id2, chat_title, message_text, warning_message, sender_link, message_link):
    Buttons = InlineKeyboardMarkup(row_width=2)
    text = chat_title + "\n\n" + message_text + warning_message
    if sender_link:
        Buttons.add(InlineKeyboardButton("Отправитель👤", url=sender_link))
    Buttons.add(InlineKeyboardButton("Сообщение✉️", url=message_link))
    await bot.send_message(chat_id=chat_id1, text=text, parse_mode="HTML", reply_markup=Buttons)
    await bot.send_message(chat_id=chat_id2, text=text, parse_mode="HTML", reply_markup=Buttons)

#Второй чат айди это костыль, так не пойдет, в идеале все аргументы должны передаваться через вызов функции по хендлеру сканирования
