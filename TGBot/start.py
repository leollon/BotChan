import logging

from os import environ

from telegram.ext import Updater, CommandHandler


updater = Updater(token=environ.get("tg_bot_token"), use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(
    format='%(asciitime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()
