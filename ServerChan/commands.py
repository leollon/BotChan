import pickle
from functools import wraps

import click

from svrbot.conf import settings
from svrbot.handlers.utils import is_file

Path = settings.Path
BASE_DIR = Path(__file__).parent.absolute()

DATA_DIR = BASE_DIR / 'svrbot/data'  # host mapped to log file location configuration
DATA_DIR.mkdir(mode=0o755, exist_ok=True)  # idempotent operation

log_file_location = (DATA_DIR / 'log_file_location').as_posix()
Path(log_file_location).touch(mode=0o744)  # idempotent operation


def check_aguments(domain, log_file):
    if not domain or (len(domain.strip('.').split('.')) <= 1):
        raise click.BadParameter("Not specify domain!", param_hint=['--domain'])
    if not log_file or not is_file(log_file):
        raise click.BadParameter("Not specify log file.", param_hint=['--log_file'])

    def decorator(func):
        @wraps(func)
        def wrapped(domain, log_file):
            return func(domain, log_file)
        return wrapped
    return decorator


@click.group()
def cli():
    pass


@cli.add_command
@click.command()
@click.option("--domain", help="The domain of a log file.[e.g. example.com]")
@click.option("--log_file", help="The absolute path of the access log file.[e.g. /var/log/nginx/access.log]")
def add(domain, log_file):

    @check_aguments(domain, log_file)
    def set_add(domain, log_file):
        log_files_dict = {}
        with open(log_file_location, 'wb') as fp:
            log_files_dict[domain] = log_file
            pickle.dump(log_files_dict, fp)
        click.echo(log_files_dict)

    set_add(domain, log_file)


@cli.add_command
@click.command()
@click.option("--domain", help="The domain of a log file.[e.g. example.com]")
@click.option("--log_file", help="The absolute path of the access log file.[e.g. /var/log/access.log]")
def remove(domain, log_file):

    @check_aguments(domain, log_file)
    def set_remove(domain, log_file):
        log_files_dict = {}
        with open(log_file_location, 'rb+') as fp:
            log_files_dict = pickle.load(fp)
            log_files_dict.pop(domain, '')
            pickle.dump(log_files_dict, fp)
        click.echo(log_files_dict)

    set_remove(domain, log_file)


@cli.add_command
@click.command()
def list():

    click.echo(pickle.load(open(log_file_location, 'rb')))


if __name__ == "__main__":
    cli()
