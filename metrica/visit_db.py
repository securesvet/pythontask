from peewee import *
from datetime import datetime

db = SqliteDatabase('VISIT.db')


# Добавить ограничения на ip_address, ограничение на уникальность столбика
# help test
# Сохранять не только айпи адрес, но и user-agent
# Нормализация базы данных
class Visit(Model):

    ip_address = CharField(help_text='ip')
    count_visits = IntegerField(default=1)
    last_visit = DateTimeField(default=datetime.now().date())
    today_visit = IntegerField(default=0)

    class Meta:
        database = db
