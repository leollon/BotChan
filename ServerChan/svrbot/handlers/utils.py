
from ..conf import settings

Path = getattr(settings, "Path")
domain_list = getattr(settings, "LOG_FILES_DICT").keys()


def check_domain(context):
    args = context.args
    for val in args:
        if val in domain_list:
            return (val, True)
    return (None, False)


def is_file(file_path):
    return Path(file_path).is_file()
