from visit_db import *


def create_visit_table():
    """Создаём таблицу Visit, если она еще не существует"""
    Visit.create_table(fail_silently=True)


def add_visit(ip_address: str):
    """
    Функция принимает IP-адрес клиента, затем добавляет его в
    базу данных, выставляя параметры по умолчанию, если клиента
    не было в базе данных, если он там был, то обновляет данные о посещении
    :param ip_address:
    :return:
    """
    try:
        visit = Visit.get(Visit.ip_address == ip_address)
        visit.count_visits += 1
        visit.today_visit += 1
        visit.last_visit = datetime.now().date()
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


def get_count_info_by_ip(ip_address: str) -> tuple[int, int, int]:
    """
    Функция принимает IP-адрес (str), возвращает tuple с информацией о визитах сайта
    :param ip_address:
    :return:
    """
    try:
        visit = Visit.get(Visit.ip_address == ip_address)
        return visit.count_visits, visit.today_visit, visit.last_visit
    except Visit.DoesNotExist:
        return 0, 0, 0


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
