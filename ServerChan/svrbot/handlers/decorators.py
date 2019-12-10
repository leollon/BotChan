

class make_handler:

    def __init__(self, handler, command):
        self._handler = handler
        self._command = command

    def __call__(self, func):
        return self._handler(self._command, func)
