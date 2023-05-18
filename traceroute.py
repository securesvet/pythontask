import os
import argparse
import socket
import struct
import sys
import time
import re
from colorama import Fore, Back, Style

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


def calc_checksum(header):
    """
    Функция, проверяющая checksum для подтверждения пакета
    :param header:
    :return:
    """
    checksum = 0
    overflow = 0

    # Для каждого слова (16-бит)
    for i in range(0, len(header), 2):
        word = header[i] + (header[i + 1] << 8)

        # Добавить текущее слово в checksum
        checksum = checksum + word
        overflow = checksum >> 16
        while overflow > 0:
            # Удаляем битики пока есть оверфлоу
            checksum = checksum & 0xFFFF
            checksum = checksum + overflow
            # Вновь считаем overflow
            overflow = checksum >> 16

    # Ещё раз проверим на оверфлоу
    overflow = checksum >> 16
    while overflow > 0:
        checksum = checksum & 0xFFFF
        checksum = checksum + overflow
        overflow = checksum >> 16

    return ~checksum & 0xFFFF


class Traceroute:
    """
    Класс Traceroute реализует работу консольной утилиты
    """

    def __init__(self, destination_host: str, count_of_packets: int, max_hops: int, packet_size: int, timeout: int):
        self.destination_host = destination_host
        self.count_of_packets = count_of_packets
        self.max_hops = max_hops
        self.packet_size = packet_size
        self.timeout = timeout
        self.previous_sender_hostname = ''
        self.MIN_SLEEP = 1000
        self.ICMP_ECHO_REQUEST = 8

        self.ttl = 1

        try:
            self.destination_ip = destination_to_ip(self.destination_host)
        except socket.gaierror:
            self.destination_ip = None

    def print_start_line(self):
        """
        Функция выводит самую первую строку команды Traceroute, пример:
        traceroute to www.mursvet.ru (80.87.110.79), 52 hops max, 32 byte packets
        :return:
        """
        if self.destination_ip:
            print(f'traceroute to {self.destination_host} ({self.destination_ip}),'
                  f' {self.max_hops} hops max, {self.packet_size} byte packets ')
        else:
            print(f'traceroute to {self.destination_host}, {self.max_hops} hops max, {self.packet_size} byte packets ')

    def print_host_unknown(self):
        """
        Вывод утилиты в случае, если был передан неверный destination
        :return:
        """
        print(Fore.RED + f'traceroute: unknown host {self.destination_host}')

    def get_icmp_packet(self):
        """
        Функция чтения ICMP-пакета (вариант для Unix-систем)
        :return:
        """
        pass

    def print_trace(self, delay, ip_header):
        """
        Вывод пути для хоста
        :param delay:
        :param ip_header:
        :return:
        """
        ip_address = socket.inet_ntoa(struct.pack('!I', ip_header['Source_IP']))
        try:
            sender_hostname = socket.gethostbyname(ip_address)[0]
        except socket.error:
            sender_hostname = ip_address

        # Проверка на то, что мы не ходим по одному и тому же хосту
        if self.previous_sender_hostname != sender_hostname:
            # По дефолту TTL до десяти
            if self.ttl < 10:
                print(f'{self.ttl} ')

    def start_traceroute(self):
        icmp_header = None
        while self.ttl <= self.max_hops:
            pass

    def tracer(self):
        try:
            icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
            icmp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, self.ttl)
        except socket.error:
            print(Fore.RED + f'Error: {socket.error}')
            print(Fore.YELLOW + 'WARNING: You must run traceroute as root in order to send ICMP messages')

    def traceroute(self):
        if self.destination_ip:
            self.print_start_line()
            # self.tracer()
        else:
            self.print_host_unknown()


def start_traceroute(destination_host: str, icmp_packets=3, packet_size=52, max_hops=32, timeout=1000):
    traceroute = Traceroute(destination_host, icmp_packets, packet_size, max_hops, timeout)
    traceroute.traceroute()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Traceroute',
        description='Program for displaying possible paths and measuring transit delays of packets',
        epilog='coded by Murzin Sviatoslav and Iuriev Artem')
    parser.add_argument('destination_host', type=str, default='www.mursvet.ru')
    parser.add_argument('-m', '--max-hops', required=False, type=int)
    parser.add_argument('-p', '--packet-size', required=False, type=int)
    # args = parser.parse_args(sys.argv[1:])
    args = parser.parse_args(['www.mursvet.ru'])
    destination_host = args.destination_host
    max_hops = args.max_hops
    packet_size = args.packet_size
    icmp_packets = 3
    start_traceroute(destination_host)
