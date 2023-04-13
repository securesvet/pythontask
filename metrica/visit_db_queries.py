from visit_db import *
import re


class Visit:
    def __init__(self, ip_address, user_agent, date_time):
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.date_time = date_time


def create_visit_table():
    """Создаёт бд, если она еще не существует"""
    IP.create_table(fail_silently=True)
    IPVisit.create_table(fail_silently=True)


def add_visit(header: str):
    """
    Функция принимает IP-адрес клиента, затем добавляет его в
    базу данных, выставляя параметры по умолчанию, если клиента
    не было в базе данных, если он там был, то обновляет данные о посещении
    :param header: str
    """
    header_split = header.split('\r\n')
    ip_address = re.search('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', header_split[0]).group()
    user_agent = header_split[4][12:]

    try:
        ip = IP.get(IP.ip_address == ip_address)
        visit = IPVisit(user_agent=user_agent, ip_id=ip.id)
        visit.save()
    except DoesNotExist:
        ip = IP(ip_address=ip_address)
        ip.save()

        ip = ip.get(IP.ip_address == ip_address)
        visit = IPVisit(user_agent=user_agent, ip_id=ip.id)
        visit.save()


def get_all_visits() -> list:
    visits = IPVisit.select()
    list_of_visitors = []
    for line in visits:
        ip_address = IP.get(id=line.ip_id).ip_address
        visitor = Visit(ip_address, line.user_agent, line.date_time)
        list_of_visitors.append(visitor)
    return list_of_visitors


def get_all_visits_by_ip(ip_address: str) -> list:
    """

    """
    list_of_visitors = []
    ip = IP.get(IP.ip_address == ip_address)
    visits = IPVisit.select().where(ip.id == ip.id)
    for line in visits:
        visitor = Visit(ip_address, line.user_agent, line.date_time)
        list_of_visitors.append(visitor)
    return list_of_visitors


def get_all_ip_by_dates(date_time_start: datetime, date_time_end=datetime.now()) \
        -> dict[str, list]:
    """
    Функция принимает две даты начала отсчета и конца
    Возвращает
    :param date_time_start: datatime
    :param date_time_end: datatime
    :return:
    """
    list_of_visitors = []
    date = []
    all_visit = IPVisit.select()
    for visit in all_visit:
        if date_time_start <= visit.date_time <= date_time_end:
            date.append(visit.date_time)
        ip_address = IP.get(IP.id == visit.ip_id)
        visitor = Visit(ip_address, visit.user_agent, visit.date_time)
        list_of_visitors.append(visitor)
    return list_of_visitors


def get_all_visits_by_ip_and_dates(ip_address: str, date_time_start: datetime, date_time_end=datetime.now()) -> list:
    """
    Функция принимает ip_address клиента, две даты (начала и конца отсчета).
    Возвращает
    :param ip_address:
    :param date_time_start:
    :param date_time_end:
    :return:
    """
    list_of_visitors = []
    ip = IP.get(IP.ip_address == ip_address)
    all_visits = IPVisit.select().where(ip.id == ip.id)
    for visit in all_visits:
        if date_time_start <= visit.date_time <= date_time_end:
            visitor = Visit(ip_address, visit.user_agent, visit.date_time)
            list_of_visitors.append(visitor)
    return list_of_visitors


def visit_close_connection():
    """Закрываем подключение к базе данных"""
    db.close()
