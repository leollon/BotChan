from requests import request

from .conf import settings

Path = settings.Path
json = settings.json
domain_list = settings.LOG_FILES_DICT.keys()
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'


def serialize(data, indent=4):
    if isinstance(data, dict):
        return json.dumps(data, indent=indent)
    try:
        result = json.dumps(json.loads(data), indent=indent)
    except Exception:
        return data
    else:
        return result


def check_domain(context):
    args = context.args
    for val in args:
        if val in domain_list:
            return (val, True)
    return (None, False)


def is_file(file_path):
    return Path(file_path).is_file()


def query_ip(context):
    try:
        ip = context.args[0]
    except IndexError:
        return serialize(data={'status': 'fail', "message": 'no ip to query'})
    else:
        return serialize(request('GET', url='http://ip-api.com/json/' + ip, headers={"User-Agent": user_agent}).text)
