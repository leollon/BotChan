from functools import wraps

import click

from svrbot.conf import settings

json = getattr(settings, "json")
cache_db = getattr(settings, "cache_db")


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
@click.option("--domain", help="The domain of a log file.[e.g. example.com]")
@click.option("--log_file", help="The absolute path of the access log file.[e.g. /var/log/nginx/access.log]")
def add(domain, log_file):

    @check_aguments(domain, log_file)
    def set_add(domain, log_file):
        log_files_dict = json.loads(cache_db.get("log_files") or "{}")
        log_files_dict[domain] = log_file
        cache_db.set("log_files", json.dumps(log_files_dict))
        click.echo(cache_db.get("log_files"))

    set_add(domain, log_file)


@cli.add_command
@click.command()
@click.option("--domain", default="", help="The domain of a log file.[e.g. example.com]")
@click.option("--log_file", default="", help="The absolute path of the access log file.[e.g. /var/log/access.log]")
def remove(domain, log_file):

    @check_aguments(domain, log_file)
    def set_remove(domain, log_file):
        log_files_dict = json.loads(cache_db.get("log_files") or "{}")
        log_files_dict.pop(domain, '')
        cache_db.set("log_files", json.dumps(log_files_dict))
        click.echo(cache_db.get("log_files"))

    set_remove(domain, log_file)


@cli.add_command
@click.command()
def list():

    click.echo(cache_db.get("log_files"))


if __name__ == "__main__":
    cli()
