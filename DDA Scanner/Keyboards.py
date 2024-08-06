from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сканирование🔎"), KeyboardButton(text="Автопостинг📢")],
        [KeyboardButton(text="Добавить группы➕"), KeyboardButton(text="Список групп📜")],
        [KeyboardButton(text="О боте📱")],
        [KeyboardButton(text="🔮Сделано RTools🔮")]
    ],
    resize_keyboard=True
)

wait_links_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Посмотреть инструкцию💡")],
        [KeyboardButton(text="Вернуться в меню↩️")]
    ],
    resize_keyboard=True
)

autoposting_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Посмотреть пример💡")],
        [KeyboardButton(text="Управление шаблонами⚙️")],
        [KeyboardButton(text="Вернуться в меню↩️")]
    ],
    resize_keyboard=True
)

schedule_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Посмотреть инструкцию💡")],
        [KeyboardButton(text="Текущее расписание✅")],
        [KeyboardButton(text="Назад⏪")]
    ],
    resize_keyboard=True
)
