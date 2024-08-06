from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import executor
from Config import bot, dp, UserState, add_new_user#, on_startup
from Keyboards import menu_kb
from Scanning import scanning
from ActiveGroups import active_groups

async def menu(chat_id):
    await bot.send_message(chat_id, text="Выберите раздел:", reply_markup=menu_kb)

@dp.message_handler(commands=['start'], state="*")
async def send_menu(message: Message):
    await add_new_user(message.chat.id)
    await UserState.menu.set()
    await menu(message.chat.id)

#Из раздела автопостинга
@dp.message_handler(lambda message: message.text == "Вернуться в меню↩️", state=UserState.autoposting)
async def autoposting_finish(message: Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.menu.set()
    await menu(message.chat.id)

#Из раздела ссылок
@dp.message_handler(lambda message: message.text == "Вернуться в меню↩️", state=UserState.wait_links)
async def wait_links_finish(message: Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.menu.set()
    await menu(message.chat.id)

from Autoposting import autoposting
from WaitLinks import wait_links

@dp.message_handler(lambda message: message.text == "Сканирование🔎", state=UserState.menu)
async def scanning_start(message: Message):
    await bot.send_message(message.chat.id, "Сканирование уже запущено")

@dp.message_handler(lambda message: message.text == "Автопостинг📢", state=UserState.menu)
async def autoposting_start(message: Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.autoposting.set()
    await autoposting(message.chat.id)

@dp.message_handler(lambda message: message.text == "Добавить группы➕", state=UserState.menu)
async def wait_links_start(message: Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await UserState.wait_links.set()
    await wait_links(message.chat.id)

@dp.message_handler(lambda message: message.text == "Список групп📜", state=UserState.menu)
async def ag_start(message: Message):
    await bot.send_message(message.chat.id, "Подождите...")
    await active_groups(message.chat.id)

@dp.message_handler(lambda message: message.text == "О боте📱", state=UserState.menu)
async def about_start(message: Message):
    posibilities = """
    Этот бот подключен к 500 тематическим телеграм группам и в нем можно:
🔎 В постоянном режиме получать новые сообщения из этих групп (приватных и открытых)
📢 Автоматически размещать свои объявления в эти группы
    🖼 Задавать несколько шаблонов объявлений
    🔢 Задавать паттерны шаблонов (в какой последовательности будут поститься шаблоны)
    ⏱ Задавать время постинга
➕ Автоматически вступать в группы, в которые Вы хотите
📜 Получать список актуальных групп
    """
    await bot.send_message(message.chat.id, posibilities)

@dp.message_handler(lambda message: message.text == "🔮Сделано RTools🔮", state=UserState.menu)
async def rtools_star(message: Message):
    button = InlineKeyboardButton("🔮Связаться🔮", url="https://t.me/wuxieten")
    await bot.send_message(
        message.chat.id,
        "Мы предлагаем инновационные и очень точные решения для бизнеса и личной жизни. Сможем сделать сайт, анимацию, бота и прочее на заказ",
        reply_markup=InlineKeyboardMarkup().add(button)
    )

async def on_startup(dp):
    await scanning(5863595924, 1706876076)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
#on_startup=on_startup,