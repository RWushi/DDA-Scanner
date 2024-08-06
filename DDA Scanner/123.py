from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram import Bot, Filters

TOKEN = '6574243823:AAGYzYFSDjIpXvmk2J8jh5qIkjROGB4CH6M'

def start(update, context):
    update.message.reply_text('Привет! Отправь мне фото.')

def handle_photo(update, context):
    photo_file = update.message.photo[-1].file_id
    update.message.reply_text(f'File ID вашего фото: {photo_file}')

def main():
    bot = Bot(TOKEN)
    updater = Updater(bot=bot, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
