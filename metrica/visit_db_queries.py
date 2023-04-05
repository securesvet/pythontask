from visit_db import *


def create_visit_table():
    """Создаёт таблицу Visit, если она еще не существует"""
    Visit.create_table(fail_silently=True)


def add_visit(ip_address: str):
    """
    Функция принимает IP-адрес клиента, затем добавляет его в
    базу данных, выставляя параметры по умолчанию, если клиента
    не было в базе данных, если он там был, то обновляет данные о посещении
    :param ip_address:
    """
    try:
        visit = Visit.get(Visit.ip_address == ip_address)
        visit.count_visits += 1
        if visit.last_visit.date() == datetime.now().date():
            visit.today_visit += 1
        else:
            visit.today_visit = 1
        visit.last_visit = datetime.now()
        visit.save()
    except Visit.DoesNotExist:
        visit = Visit(ip_address=ip_address, last_visit=datetime.now().date(), today_visit=1)
        visit.save()


def get_table():
    """
    Функция, не принимающая аргументов, выводит таблицу из Visit.db в консоль
    """
    for user in Visit.select():
        print(user.id, user.ip_address, user.count_visits, user.last_visit, user.today_visit)


def get_counts_overall() -> int:
    """
    Функция не принимет аргументов, запрашивает данные из VISIT.db и суммирует поля count_visits,
    возвращает сумму всех посещений от всех клиентов
    :return:
    """
    count_overall = 0
    for user in Visit.select():
        count_overall += user.count_visits
    return count_overall


def get_unique_visits() -> int:
    """
    Функция возвращает количество уникальных посещений, выводя количество строк в таблице
    :return:
    """
    return Visit.select().count()


def get_today_overall_visits() -> int:
    """
    Функция возвращает количество всех посещений за сегодняшний день
    :return:
    """
    count_today_overall = 0
    for client in Visit.select():
        if client.last_visit.date() == datetime.now().date():
            count_today_overall += client.today_visit
        else:
            client.today_visit = 0
        client.save()
    return count_today_overall


def get_today_unique_visits() -> int:
    """
    Функция возвращает уникальных посетителей за сегодняшний день
    :return:
    """
    count_of_unique_visits_today = 0
    for client in Visit.select():
        if client.last_visit.date() == datetime.now().date():
            count_of_unique_visits_today += 1
    return count_of_unique_visits_today


def visit_close_connection():
    """Закрываем подключение к базе данных"""
    db.close()
