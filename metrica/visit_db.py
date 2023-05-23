from peewee import *
from datetime import datetime

db = SqliteDatabase('VISIT.db')


class BaseModel(Model):
    id = PrimaryKeyField()

    class Meta:
        database = db
        order_by = 'id'


class IP(BaseModel):
    """
    В данной таблице хранятся только IP и ID
    """
    ip_address = CharField(max_length=14, help_text='ip', unique=True)

    class Meta:
        table_name = 'IPs'


class IPVisit(BaseModel):
    """
    Тут хранятся все даты и user-agents в привязке к ip
    """
    user_agent = CharField(help_text='user-agent')
    date_time = DateTimeField(default=datetime.now, help_text='date of visit')
    ip_id = ForeignKeyField(IP)

    class Meta:
        table_name = 'Visits'