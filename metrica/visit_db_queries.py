from visit_db import *
from peewee import DoesNotExist

class Visit:
    """
    Сущность посетителя сайта
    """

    def __init__(self, login, ip_address, user_agent, date_time):
        self.login = login
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.date_time = date_time


def create_visit_table():
    """
    Создаёт бд, если она еще не существует
    """
    IP.create_table(fail_silently=True)
    IPVisit.create_table(fail_silently=True)
    # Auth.create_table(fail_silently=True)


def add_visit(ip_address: str, user_agent: str):
    """
    Функция принимает IP-адрес и user_agent, затем добавляет его в
    базу данных.
    :param ip_address: str
    :param user_agent: str
    :param header: str
    """
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
    """
    Функция возвращает список со всеми клиентами
    :return: list
    """
    try:
        visits = IPVisit.select()
        list_of_visitors = []
        for line in visits:
            ip_address = IP.get(id=line.ip_id).ip_address
            visitor = Visit(ip_address, line.user_agent, line.date_time)
            list_of_visitors.append(visitor)
        return list_of_visitors
    except DoesNotExist:
        return []


def get_all_visits_by_ip_and_dates(ip_address=None, date_time_start=datetime(1, 1, 1),
                                   date_time_end=datetime.now()) -> list:
    """
    Функция принимает ip_address клиента, две даты (начала и конца отсчета(конец по дефолту настоящее время)).
    Возвращает список со всеми посещениями клиента в этом промежутке времени

    :param ip_address: str
    :param date_time_start: str
    :param date_time_end: str
    :return: list
    """
    try:
        if date_time_start > date_time_end:
            temp = date_time_end
            date_time_end = date_time_start
            date_time_start = temp

        list_of_visitors = []
        if ip_address:
            ip = IP.get(IP.ip_address == ip_address)
            all_visits = IPVisit.select().where(ip.id == ip.id)
            for visit in all_visits:
                if date_time_start <= visit.date_time <= date_time_end:
                    visitor = Visit(ip_address, visit.user_agent, visit.date_time)
                    list_of_visitors.append(visitor)
        else:
            all_visits = IPVisit.select()
            for visit in all_visits:
                if date_time_start <= visit.date_time <= date_time_end:
                    ip_address = IP.get(IP.id == visit.ip_id).ip_address
                    visitor = Visit(ip_address, visit.user_agent, visit.date_time)
                    list_of_visitors.append(visitor)
        return list_of_visitors
    except DoesNotExist:
        return []


def visit_close_connection():
    """Закрываем подключение к базе данных"""
    db.close()
