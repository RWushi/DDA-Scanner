from Config import bot, dp, UserState, DB
from aiogram.types import Message, CallbackQuery
from Keyboards import schedule_kb
from datetime import datetime

class PostData:
    def __init__(self):
        self.posts = {}

    async def set_post_id(self, chat_id, post_id):
        self.posts[chat_id] = post_id

    async def get_post_id(self, chat_id):
        return self.posts.get(chat_id)

user_post_data = PostData()


async def schedule(chat_id, post_id):
    await bot.send_message(chat_id, text=f"Отправьте дату и время, в которое нужно отправить пост №{post_id}", reply_markup=schedule_kb)
    await user_post_data.set_post_id(chat_id, post_id)


@dp.message_handler(lambda message: message.text == "Посмотреть инструкцию💡", state=UserState.schedule)
async def instruction_schedule(message: Message):
    await bot.send_message(message.chat.id, "Этот пост будет отправлен во все доступные группы по указанному времени. Вам нужно отправить сообщение с датой и временем в формате ДД.ММ.ГГГГ ЧЧ:ММ, например 06.12.2023 09:00. Если пост надо отправить несколько раз, то нужно отправить несколько сообщений с датой")


@dp.message_handler(lambda message: message.text == "Текущее расписание✅", state=UserState.schedule)
async def current_schedule_start(message: Message):
    user_id = message.from_user.id
    post_id = await user_post_data.get_post_id(user_id)
    post_id = int(post_id)

    async with DB() as conn:
        query = "SELECT datetime FROM default_messages WHERE user_id = $1 AND post_id = $2"
        datetimes_records = await conn.fetch(query, user_id, post_id)

        if not datetimes_records:
            query = "SELECT datetime FROM media_groups WHERE user_id = $1 AND post_id = $2"
            datetimes_records = await conn.fetch(query, user_id, post_id)

        datetime_list = []
        for record in datetimes_records:
            if record['datetime'] is not None:
                for dt in record['datetime']:
                    datetime_list.append(dt.strftime("%d.%m.%Y %H:%M"))

        if not datetime_list:
            await bot.send_message(message.chat.id, "Для этого поста публикаций не запланировано")
        else:
            datetime_str = '\n'.join(datetime_list)
            await bot.send_message(message.chat.id, datetime_str)


@dp.callback_query_handler(text_startswith='schedule:', state=[UserState.schedule, UserState.autoposting])
async def schedule_start(callback_query: CallbackQuery):
    await UserState.schedule.set()
    user_id = callback_query.from_user.id
    post_id = callback_query.data.split(":", 1)[1]

    await schedule(user_id, post_id)


@dp.message_handler(state=UserState.schedule)
async def set_schedule(message: Message):
    user_id = message.from_user.id
    time_str = message.text
    post_id = await user_post_data.get_post_id(user_id)
    post_id = int(post_id)

    try:
        scheduled_datetime = datetime.strptime(time_str, '%d.%m.%Y %H:%M')
        current_datetime = datetime.now()

        if scheduled_datetime < current_datetime:
            await bot.send_message(user_id, "Вы ввели прошлое время, введите будущее")
            return
    except ValueError:
        await bot.send_message(user_id, "Время введено неправильно, попробуйте еще раз или вернитесь назад")
        return

    async with DB() as conn:
        updated = await conn.execute(
            "UPDATE default_messages SET datetime = array_append(datetime, $1) WHERE user_id = $2 AND post_id = $3",
            scheduled_datetime, user_id, post_id
        )

        if updated == "UPDATE 0":
            await conn.execute(
                "UPDATE media_groups SET datetime = array_append(datetime, $1) WHERE user_id = $2 AND post_id = $3",
                scheduled_datetime, user_id, post_id
            )

    await bot.send_message(user_id, f"Расписание установлено на {scheduled_datetime.strftime('%d.%m.%Y %H:%M')}")


