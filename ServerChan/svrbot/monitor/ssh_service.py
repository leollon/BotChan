import subprocess

from ..conf import settings

datetime = getattr(settings, "datetime")


class ServerMonitor(object):

    def run_command(self, args) -> str:
        return subprocess.run(args=args, capture_output=True).stdout.decode('utf-8')

    @property
    def hostname(self) -> str:
        return self.run_command(["hostname"])

    @property
    def now(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")

    @property
    def who(self):
        return self.run_command(["who"])

    @property
    def w(self):
        return self.run_command(["w"])

    @property
    def message(self):
        return "{0}{1}{2}{3}".format(self.hostname, self.now, self.who, self.w)


def send_msg_to_bot():
    pass
