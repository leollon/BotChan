import re
from datetime import datetime  # noqa: F401
from math import floor  # noqa: F401
from os import environ
from pathlib import Path  # noqa: F401

from peewee import PostgresqlDatabase

PROC_DIR = "/proc"
REQUEST_KWARGS = {
    'proxy_url': 'socks5://127.0.0.1:1080'
}

psql_db = PostgresqlDatabase(
    database=environ.get("PG_USER_DB"),
    user=environ.get("PG_USER"),
    passpard=environ.get("PG_USER_PASSWORD"),
    host=environ.get("POSTGRES_HOST"),
    port=int(environ.get("POSTGRES_PORT"))
)

HTTP_METHODS = re.compile(r"(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS|TRACE|CONNECT)+")
HTTP_STATUS_CODE = re.compile(r"\"{1}[1-5]{1}[0-9]{2}\"{1}")
