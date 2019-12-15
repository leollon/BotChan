from peewee import DateTimeField, FixedCharField, FloatField, Model, TextField

from ..conf import settings

psql_db = getattr(settings, "psql_db")
datetime = getattr(settings, "datetime")


class NginxLogEntry(Model):
    http_method = FixedCharField(max_length=8)
    real_ip = TextField()
    cdn_ip = TextField()
    status_code = FixedCharField(max_length=6)
    request_time = FloatField()
    uri = TextField()
    request_datetime = DateTimeField()

    class Meta:
        database = psql_db
        table_name = 'nginx_log_entry'


psql_db.create_tables([NginxLogEntry, ])
