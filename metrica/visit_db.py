from peewee import *
from datetime import datetime

'''
Реализация базы данных с помощью peewee для записи IP-адресов 
'''

# Создаем подключение к базе данных
db = SqliteDatabase('VISIT.db')


# Определяем модель таблицы
class Visit(Model):
    ip_address = CharField()
    count_visits = IntegerField(default=1)
    last_visit = DateTimeField()
    today_visit = IntegerField()

    class Meta:
        database = db


# Создаем таблицу, если она еще не существует
Visit.create_table(fail_silently=True)

'''
Функция добавляет новую запись в базу данных
'''


def add_visit(ip_address):
    # Ищем запись с таким же IP адресом
    try:
        visit = Visit.get(Visit.ip_address == ip_address)
        visit.count_visits += 1
        visit.today_visit += 1
        visit.last_visit = datetime.now()
        visit.save()
    except Visit.DoesNotExist:
        visit = Visit(ip_address=ip_address, last_visit=datetime.now(), today_visit=1)
        visit.save()


'''
Выводит таблицу из базы данных
'''


def get_table():
    for user in Visit.select():
        print(user.id, user.ip_address, user.count_visits, user.last_visit, user.today_visit)


'''
Возвращает tuple с информацией о визитах сайта 
(привязано к айпи адресу клиента)
'''


def get_count_info_by_ip(ip_address):
    try:
        visit = Visit.get(Visit.ip_address == ip_address)
        return visit.count_visits, visit.today_visit, visit.last_visit
    except Visit.DoesNotExist:
        return 0


# Закрываем подключение к базе данных
db.close()
