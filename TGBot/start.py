import logging
from os import environ

from telegram.ext import CommandHandler, Updater

from bot.command_handlers import (last_24_hours, last_ten_mins, ping, resource,
                                  start, today, uptime)

updater = Updater(token=environ.get("tg_bot_token"), use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(
    format='%(asciitime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

start_handler = CommandHandler('start', start)
today_handler = CommandHandler('today', today)
ping_handler = CommandHandler(['ping', 'PING'], ping)
resource_handler = CommandHandler('resource', resource)
uptime_handler = CommandHandler(['uptime', 'Uptime'], uptime)
last10mins_handler = CommandHandler('last10mins', last_ten_mins)
last_24_hours_handler = CommandHandler('last24hours', last_24_hours)
dispatcher.add_handler(start_handler)
updater.start_polling()
