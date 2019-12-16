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
    database=environ.get("POSTGRES_DB"),
    user=environ.get("POSTGRES_USER"),
    password=environ.get("POSTGRES_PASSWORD"),
    host=environ.get("POSTGRES_HOST"),
    port=int(environ.get("POSTGRES_PORT"))
)

LOG_FILES_LIST = set("/home/monkey/Desktop/Projects/tools/BotChan/blog.access.log")
TEN_MINUTES = 10 * 60 * 1.0
ONE_DAY = 24 * 3600 * 1.0
SEVEN_DAYS = 7 * ONE_DAY * 1.0
HALF_MONTH = 2 * SEVEN_DAYS * 1.0
THIRTY_DAYS = 30 * ONE_DAY * 1.0
STATUS_CODE_SERACH = re.compile(r"\"{1}[1-5]{1}[0-9]{2}\"{1}").search
REQUEST_SEARCH = re.compile(r"(GET|POST|PUT|DELETE|PATCH|OPTIONS|TRACE|CONNECT){1}[\w\d\s/%\-\.]+").search
DATETIME_SEARCH = re.compile(r"(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})").search  # 09/Dec/2019:11:02:41
REQUEST_TIME_SEARCH = re.compile(r"\"(\d+\.\d{3}\")").search
