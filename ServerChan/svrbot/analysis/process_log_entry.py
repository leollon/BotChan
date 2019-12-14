from collections import defaultdict

from ..conf import settings
from .models import NginxLogEntry

datetime = getattr(settings, 'datetime')
log_files_list = getattr(settings, "LOG_FILES_LIST")
request_search = getattr(settings, "REQUEST_SEARCH")
status_code_search = getattr(settings, "STATUS_CODE_SERACH")
datetime_search = getattr(settings, "DATETIME_SEARCH")
request_time_search = getattr(settings, "REQUEST_TIME_SEARCH")
log_files_list = getattr(settings, "LOG_FILES_LIST")


class LogEntry(object):

    month_map = {
        "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
        "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
        "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
    }
    data = defaultdict(dict)

    def evalute_line(self, line):
        cdn_ip, real_ip = line.split(' ')[0].replace('"', ''), line.split(' ')[1].replace('"', '')
        cdn_ip, real_ip = (real_ip, cdn_ip) if real_ip == '-' else (cdn_ip, real_ip)
        req = request_search(line)
        if req is None:
            request = 'Unknown'
        else:
            request = req.group(0)
        status_code = status_code_search(line).group(0).replace('"', '')
        request_datetime = datetime_search(line).group(0)
        request_time = request_time_search(line).group(0).replace('"', '')
        return (cdn_ip, real_ip, request, status_code, request_datetime, request_time)

    def get_data_from_logs(self, filename):
        for line in self.open_file(filename):
            method, uri = "Unknown", "Unknown"
            if "HEAD" not in line and "assets/" not in line:
                cdn_ip, real_ip, request, status_code, request_datetime, request_time = self.evalute_line(line)
                request_datetime.replace(request_datetime[3:6], str(self.month_map[request_datetime[3:6]]))
                if request != "Unknown":
                    method, uri = request.split(' ')[0], request.split(' ')[1]
                NginxLogEntry(
                    cdn_ip=cdn_ip, real_ip=real_ip, http_method=method,
                    status_code=status_code, request_time=request_time,
                    uri=uri, request_datetime=request_datetime
                ).save()

    def open_file(self, filename, mode='r'):
        return open(filename, mode=mode)
