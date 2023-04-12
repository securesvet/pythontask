from visit_db import *
import re


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
    date_of_visit = datetime.now()

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


def get_all_ip() -> list:
    """
    Функция выводит вообще все ip
    :return: list c ip
    """
    ips = []
    for ip in IP.select():
        ips.append(ip.ip_address)

    return ips


def get_all_visits_by_ip(ip_address: str) -> list:
    """
    Функция принимает ip_address клиента
    Возвращает список дат его по ip
    :param ip_address:
    :return: list с datatime
    """
    dates = []
    ip = IP.get(IP.ip_address == ip_address)
    all_dates = IPVisit.select().where(ip.id == ip.id)
    for date in all_dates:
        dates.append(date.data_time)
    return dates


def get_all_ip_by_dates(data_time_start: datetime, data_time_end:  datetime) -> dict[str, list]:
    """
    Функция принимает две даты начала отсчета и конца
    Возвращает словарь где ключ ip клиента, а значение list с временем посещения клиента в заданном промежутке времени
    :param data_time_start: datatime
    :param data_time_end: datatime
    :return: {str(ip):[datatime]}
    """
    ips_and_date = {}
    date = []
    all_visit = IPVisit.select()
    for visit in all_visit:
        if data_time_start <= visit.data_time <= data_time_end:
            date.append(visit.data_time)
        ip = IP.get(IP.id == visit.ip_id)
        ips_and_date[ip.ip_address] = date

    return ips_and_date


def get_all_ip_by_date(data_time_start: datetime) -> dict[str, list]:
    """
    Функция принимает две даты начала отсчета.
    Возвращает словарь где ключ ip клиента, а значение list с временем посещения клиента в промежутке от заданной даты до настоящего времени (формат datatime)
    :param data_time_start: datatime
    :return: {str(ip):[datatime]}
    """
    ips_and_date = {}
    date = []
    all_visit = IPVisit.select()
    for visit in all_visit:
        if data_time_start <= visit.data_time:
            date.append(visit.data_time)
        ip = IP.get(IP.id == visit.ip_id)
        ips_and_date[ip.ip_address] = date

    return ips_and_date


def visit_close_connection():
    """Закрываем подключение к базе данных"""
    db.close()
