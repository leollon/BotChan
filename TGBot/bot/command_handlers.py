

def resource(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="system resource")


def uptime(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="uptime")


def ping(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="PONG")


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def last_24_hours(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="last twenty four hours.")


def last_ten_mins(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="last ten minutes.")


def today(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="today visited.")
