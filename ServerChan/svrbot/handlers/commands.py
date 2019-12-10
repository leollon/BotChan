import psutil
from telegram.ext import CommandHandler

from .. import dispatcher
from .decorators import make_handler


@dispatcher.add_handler
@make_handler(CommandHandler, "resource")
def resource(update, context):
    cpu_percent = psutil.cpu_percent()
    swap_memory = psutil.swap_memory()
    virtual_memory = psutil.virtual_memory()
    mem_total = virtual_memory.total / 2 ** 10
    mem_used = virtual_memory.used / 10 ** 6
    swap_total = swap_memory.total / 10 ** 6
    swap_used = swap_memory.used / 10 ** 6
    sent_text = "CPU: %0.3f%%\nMemory: %0.3fMB / %0.3fMB\nSwap: %0.3fMB / %0.3fMB" % (
        cpu_percent,
        mem_used,
        mem_total,
        swap_used,
        swap_total,
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=sent_text)


@dispatcher.add_handler
@make_handler(CommandHandler, "uptime")
def uptime(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="uptime")


@dispatcher.add_handler
@make_handler(CommandHandler, ["ping", "PING"])
def ping(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="PONG")


@dispatcher.add_handler
@make_handler(CommandHandler, "start")
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


@dispatcher.add_handler
@make_handler(CommandHandler, "last24hours")
def last_24_hours(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="last twenty four hours.")


@dispatcher.add_handler
@make_handler(CommandHandler, "last10mins")
def last_ten_mins(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="last ten minutes.")


@dispatcher.add_handler
@make_handler(CommandHandler, "today")
def today(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="today visited.")
