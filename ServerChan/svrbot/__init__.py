from os import environ

from telegram.ext import Updater

updater = Updater(token=environ.get("tg_bot_token"), use_context=True)
dispatcher = updater.dispatcher

from .handlers.commands import (last_24_hours,  # noqa: F401, E402, isort:skip
                                last_ten_mins, ping, resource, start, today,
                                uptime, load)
