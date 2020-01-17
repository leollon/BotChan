from functools import wraps

import click

from svrbot.conf import settings
from svrbot.handlers.utils import is_file

cache = settings.cache
json = settings.json
log_files_dict = settings.LOG_FILES_DICT


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
        log_files_dict[domain] = log_file
        cache.set('tg_bot_log_files_dict', json.dumps(log_files_dict, indent=4))
        click.echo(log_files_dict)

    set_add(domain, log_file)


@cli.add_command
@click.command()
@click.option("--domain", help="The domain of a log file.[e.g. example.com]")
@click.option("--log_file", help="The absolute path of the access log file.[e.g. /var/log/access.log]")
def remove(domain, log_file):

    @check_aguments(domain, log_file)
    def set_remove(domain, log_file):
        log_files_dict.pop(domain)
        cache.set('tg_bot_log_files_dict', json.dumps(log_files_dict, indent=4))
        click.echo(log_files_dict)

    set_remove(domain, log_file)


@cli.add_command
@click.command()
def list():

    click.echo(json.loads(log_files_dict))


if __name__ == "__main__":
    cli()
