
from ..conf import settings

datetime = getattr(settings, 'datetime')
log_files_list = getattr(settings, "LOG_FILES_LIST")
http_method_regexp = getattr(settings, "HTTP_METHODS")
http_status_code_regexp = getattr(settings, "HTTP_STATUS_CODE")


class LogEntry(object):

    def get_data_from_logs(self):
        pass
    pass


class LogDataStructure(object):

    pass
