from functools import wraps

from ..conf import settings

allowed_id = int(getattr(settings, "chat_id", 0))


class make_handler:

    def __init__(self, handler, command):
        self._handler = handler
        self._command = command

    def __call__(self, func):
        return self._handler(self._command, func)


def auth(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        if update.effective_chat.id != allowed_id:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Not Allowed.")
            return
        return func(update, context)
    return wrapped
