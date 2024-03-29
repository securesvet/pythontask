from peewee import SqliteDatabase, PrimaryKeyField, Model, CharField, DateTimeField, ForeignKeyField
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


class Auth(BaseModel):
    """
    В данной таблице хранятся логин и пароль пользователей
    """
    login = CharField(help_text='login', unique=True)
    password = CharField(help_text='hashed password')

    class Meta:
        table_name = 'Auth'


class UsersSeen(BaseModel):
    """
    В данной таблице хранятся usename'ы и ссылки, которые видели юзеры
    """
    username = ForeignKeyField(Auth)
    link = CharField(max_length=64, help_text='link to resource', unique=False)

    class Meta:
        table_name = 'UsersSeen'


class IPVisit(BaseModel):
    """
    Тут хранятся все даты и user-agents в привязке к ip
    """
    user_agent = CharField(help_text='user-agent')
    date_time = DateTimeField(default=datetime.now, help_text='date of visit')
    ip_id = ForeignKeyField(IP)

    class Meta:
        table_name = 'Visits'
