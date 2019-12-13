from functools import wraps

import click

from svrbot.conf import settings

log_files_list = getattr(settings, 'LOG_FILES_LIST')


def check_aguments(domain, log_file):
    if len(domain.strip('.').split('.')) <= 1:
        raise click.BadParameter("Not specify domain!", param_hint=['--domain'])
    if not log_file:
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
@click.option("--domain", default="", help="The domain of a log file.[e.g. example.com]")
@click.option("--log_file", default="", help="The absolute path of the access log file.[e.g. /var/log/access.log]")
def add(domain, log_file):

    @check_aguments(domain, log_file)
    def set_add(domain, log_file):
        log_file = " - ".join([domain, log_file])
        log_files_list.add(log_file)
        click.echo(log_files_list)

    set_add(domain, log_file)


@cli.add_command
@click.command()
@click.option("--domain", default="", help="The domain of a log file.[e.g. example.com]")
@click.option("--log_file", default="", help="The absolute path of the access log file.[e.g. /var/log/access.log]")
def remove(domain, log_file):

    @check_aguments(domain, log_file)
    def set_remove(domain, log_file):
        log_file = " - ".join([domain, log_file])
        log_files_list.remove(log_file)
        click.echo(log_files_list)

    set_remove(domain, log_file)


@cli.add_command
@click.command()
def list():
    click.echo(log_files_list)


if __name__ == "__main__":
    cli()
