import os
import argparse
import socket
import time
import re

timer = time.time()


def is_valid_ip(host: str) -> bool:
    """
    Функция возвращает значение True, если переданный хост валидный,
    и возвращает False, если нет
    :param host:
    :return:
    """
    # Паттерн для айпи адреса
    pattern = r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][' \
              r'0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return bool(re.match(pattern, host))


def destination_to_ip(destination: str) -> str:
    """
    Функция кастует переданный хост к IP-адресу
    :param destination:
    :return:
    """
    if is_valid_ip(destination):
        return destination
    return socket.gethostbyname(destination)


if __name__ == '__main__':
    #print(destination_to_ip('www.mursvet.ru'))
    pass
