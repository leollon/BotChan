import os
from collections import defaultdict
from typing import Counter

from ..conf import settings
from .models import NginxLogEntry

json = getattr(settings, "json")
datetime = getattr(settings, "datetime")
dt_strptime = datetime.strptime
log_files_dict = getattr(settings, "LOG_FILES_DICT")
request_search = getattr(settings, "REQUEST_SEARCH")
status_code_search = getattr(settings, "STATUS_CODE_SERACH")
datetime_search = getattr(settings, "DATETIME_SEARCH")
request_time_search = getattr(settings, "REQUEST_TIME_SEARCH")

ten_mins = getattr(settings, "TEN_MINUTES")
one_day = getattr(settings, "ONE_DAY")
seven_days = getattr(settings, "SEVEN_DAYS")
HALF_MONTH = getattr(settings, "HALF_MONTH")
thirty_days = getattr(settings, "THIRTY_DAYS")


class LogEntry(object):

    month_map = {
        "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
        "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
        "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
    }
    data = defaultdict(dict)

    def evaluate_line(self, line):
        cdn_ip, real_ip = line.split(' ')[0].replace('"', ''), line.split(' ')[1].replace('"', '')
        if real_ip == '-':
            cdn_ip, real_ip = real_ip, cdn_ip
        req = request_search(line)
        if req is None:
            request = 'Unknown'
        else:
            request = req.group(0)
        status_code = status_code_search(line).group(0).replace('"', '')
        request_datetime = datetime_search(line).group(0)
        request_time = request_time_search(line).group(0).replace('"', '')
        return (cdn_ip, real_ip, request, status_code, request_datetime, request_time)

    def get_data_from_logs(self, filename, start_datetime='', datetime_range=ten_mins):
        last_access_datetime_timestamp = None
        for line in self.reverse_open_file(filename):
            method, uri = "Unknown", "Unknown"
            if "HEAD" not in line and "assets/" not in line:
                cdn_ip, real_ip, request, status_code, request_datetime, request_time = self.evaluate_line(line)
                request_datetime = request_datetime.replace(
                    request_datetime[3:6],
                    str(self.month_map[request_datetime[3:6]])
                )
                current_request_datetime_timestamp = dt_strptime(request_datetime, "%d/%m/%Y:%H:%M:%S").timestamp()
                if last_access_datetime_timestamp is None:
                    last_access_datetime_timestamp = dt_strptime(request_datetime, "%d/%m/%Y:%H:%M:%S").timestamp()
                if request != "Unknown":
                    method, uri = request.split(' ')[0], request.split(' ')[1]
                # self.save_log_entry_to_db(
                #     cdn_ip=cdn_ip, real_ip=real_ip, http_method=method,
                #     status_code=status_code, request_time=request_time,
                #     uri=uri, request_datetime=request_datetime
                # )
                if start_datetime and dt_strptime(request_datetime, "%d/%m/%Y:%H:%M:%S").date() < start_datetime.date():
                    break
                if (last_access_datetime_timestamp - current_request_datetime_timestamp) > datetime_range:
                    break
                uri = self.data.setdefault(uri, {})
                uri.setdefault("real_ips", []).append(real_ip)
                if cdn_ip != "-":
                    uri.setdefault("cdn_ips", []).append(cdn_ip)
                if cdn_ip == "-":
                    not_cdn = uri.setdefault("not_cdn", {})
                    not_cdn.setdefault("methods", []).append(method)
                    not_cdn.setdefault("real_ips", []).append(real_ip)
                if status_code.startswith('4'):
                    self.data.setdefault("4xx", []).append(status_code)
                if status_code.startswith('3'):
                    self.data.setdefault("3xx", []).append(status_code)
                if status_code.startswith('2'):
                    self.data.setdefault("2xx", []).append(status_code)
        return self.data

    def open_file(self, filename, mode='r'):
        return open(filename, mode=mode)

    def reverse_open_file(self, filename, buff_size=8192):
        with open(filename, 'r') as fp:
            segment = None
            offset = 0
            fp.seek(0, os.SEEK_END)
            file_size = remaining_size = fp.tell()
            while remaining_size > 0:
                offset = min(file_size, offset + buff_size)
                fp.seek(file_size - offset)
                buffer = fp.read(min(remaining_size, buff_size))
                remaining_size -= buff_size
                lines = buffer.split('\n')
                # the first line of the buffer is probably not a complete line
                # so we'll save it and append it to the last line of the next
                # buffer we read
                if segment is not None:
                    # if the previous chunk starts right from the beginning
                    # of line do not connect the segment to the last line of
                    # new chunk instead, yield the segment first
                    if buffer[-1] != '\n':
                        lines[-1] += segment
                    else:
                        yield segment
                segment = lines[0]
                for index in range(len(lines) - 1, 0, -1):
                    if len(lines[index]):
                        yield lines[index]
            # Don't yield None if the file was empty
            if segment is not None:
                yield segment

    def save_log_entry_to_db(self, cdn_ip, real_ip, http_method, status_code, request_time, uri, request_datetime):
        NginxLogEntry(
            cdn_ip=cdn_ip, real_ip=real_ip, http_method=http_method,
            status_code=status_code, request_time=request_time,
            uri=uri, request_datetime=request_datetime
        ).save()


class AnalyseLogs(LogEntry):

    def start_analyse(self, domain, start_datetime='', datetime_range=ten_mins):
        self.get_data_from_logs(
            start_datetime=start_datetime,
            filename=log_files_dict[domain],
            datetime_range=datetime_range
        )
        twoxx = len(self.data.pop('2xx', []))
        threexx = len(self.data.pop('3xx', []))
        fourxx = len(self.data.pop('4xx', []))
        visited_ips = Counter()
        not_through_cdn = Counter()
        for key in self.data.keys():
            visited_ips.update(Counter(self.data.get(key).get("real_ips")))
            not_through_cdn.update(Counter(self.data.get(key, '').get("not_cdn", {}).get("real_ips", [])))
        visited_ips = json.dumps(dict(visited_ips.most_common(10)), indent=4)
        not_through_cdn = json.dumps(dict(not_through_cdn.most_common(1)), indent=4)
        result = "2xx: {0}\n\n3xx: {1}\n\n4xx: {2}\n\nvisited_ips: {3}\n\nnot_through_cdn: {4}\n\n".format(
            twoxx, threexx, fourxx, visited_ips, not_through_cdn
        )
        self.data.clear()
        return result
