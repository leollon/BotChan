import re
from datetime import datetime  # noqa: F401
from math import floor  # noqa: F401
from os import environ
from pathlib import Path
from typing import Type  # noqa: F401

import redis

try:
    import ujson as json
except ImportError:
    import json  # noqa: F401

PROC_DIR = Path("/proc")
BASE_DIR = Path(__file__).parent.parent
REQUEST_KWARGS = {
    'proxy_url': 'socks5://127.0.0.1:1080',
    'urllib3_proxy_kwargs': {
        'timeout': 5.0
    }
}

cache = redis.Redis(host=environ.get("REDIS_HOST"), port=int(environ.get("REDIS_PORT")), db=1, encoding='utf-8')

try:
    json.loads(cache.get('tg_bot_log_files_dict'))
except TypeError:
    cache.set('tg_bot_log_files_dict', '{}')
finally:
    LOG_FILES_DICT = json.loads(cache.get('tg_bot_log_files_dict'))


TEN_MINUTES = 10 * 60 * 1.0
ONE_DAY = 24 * 3600 * 1.0
SEVEN_DAYS = 7 * ONE_DAY
HALF_MONTH = 2 * SEVEN_DAYS
THIRTY_DAYS = 30 * ONE_DAY
STATUS_CODE_SERACH = re.compile(r"\s([1-5]{1}[0-9]{2})\s").search
REQUEST_SEARCH = re.compile(r'(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS|CONNECT{1})\s([^"]+)\s').search
DATETIME_SEARCH = re.compile(r"(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})").search  # 09/Dec/2019:11:02:41
REQUEST_TIME_SEARCH = re.compile(r"\s(\d+\.\d{3})$").search
HTTP_REFERER_SEARCH = re.compile(r'"(https?:\/{2}[\w\d\%\.\-\/_]+|\-)').search

CHAT_ID = environ.get("CHAT_ID")
