import os
import argparse
import socket
import sys
import time
import re

timer = time.time()


def is_valid_ip(ip_address: str) -> bool:
    """
    Функция возвращает значение True, если переданный хост валидный,
    и возвращает False, если нет
    :param ip_address:
    :return:
    """
    # Паттерн для айпи адреса
    pattern = r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][' \
              r'0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return bool(re.match(pattern, ip_address))


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
    parser = argparse.ArgumentParser(prog='Traceroute',
                                     description='Program for displaying possible paths and measuring transit delays of'
                                                 ' packets',
                                     epilog='coded by Murzin Sviatoslav and Iuriev Artem')
    parser.add_argument('destination_host')
    args = parser.parse_args(sys.argv[1:])
    destination_host = args.destination_host
    print(destination_to_ip(destination_host))
