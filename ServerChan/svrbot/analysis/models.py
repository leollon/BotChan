from peewee import (BooleanField, DateTimeField, FixedCharField, FloatField,
                    Model, TextField)

from ..conf import settings

psql_db = getattr(settings, "psql_db")
datetime = getattr(settings, "datetime")


class BaseModel(Model):
    """A base model that will use Postgresql database"""
    class Meat:
        database = psql_db


class NginxLogEntry(BaseModel):
    http_method = FixedCharField(max_length=8)
    real_ip = TextField()
    cdn_ip = BooleanField(default=True)
    status_code = FixedCharField(max_length=6)
    request_time = FloatField()
    uri = TextField()
    request_datetime = DateTimeField()

    class Meta:
        table_name = 'nginx_log_entry'


psql_db.create_tables([NginxLogEntry, ])
