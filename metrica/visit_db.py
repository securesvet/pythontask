from peewee import *
from datetime import datetime

db = SqliteDatabase('VISIT.db')


class Visit(Model):
    ip_address = CharField()
    count_visits = IntegerField(default=1)
    last_visit = DateTimeField(default=datetime.now())
    today_visit = IntegerField()

    class Meta:
        database = db
