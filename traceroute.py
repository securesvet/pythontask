import select

import os
import argparse
import socket
import struct
import sys
import time
import re
from colorama import Fore, Back, Style

timer = time.time()


# TODO НАПИСАТЬ ТЕСТЫ С МОКАМИ, ТОЧНО, Я ЭТИМ ЗАЙМУСЬ ЗАВТРА, ТЫ МОЖЕШЬ ОСТАЛЬНЫЕ ТУДУШКИ КРОМЕ ПРИНТА ПОДЕЛАТЬ

# TODO ОБРАТИ ВНИМАНИЕ НА ЭТИ СТРОКИ КОДА, НАДЕЮСЬ ТЫ СФЕТЧИШЬ ПРОЕКТ И УВИДИШЬ ЭТО. У меня есть как и у всех
#  нормальных людей VPN. У меня есть программа traceroute на линуксе, которая не работает. Программа. На линуксе.
#  Консольная. Утилита. Не работает. Когда я бля подключаюсь к ебаному VPN. Угадай что? Консольная утилита, блять,
#  работает. Вопрос. Это из России уже никакой интернет не идёт никуда или что это за прикол? Самый большой прикол
#  ещё в том, что мы похоже написали traceroute, которому тоже не нравится то, что подключение идёт из России,
#  потому вопрос почему бля? Есть предположение, что это из-за особенности ICMP пакетов, и где-то я читал про
#  ненадёжность traceroute как утилиты для траблшутинга, так что, епт, возможно все неплохо.
#  Кстати говоря, всё работает почти, осталось только
#  написать функции для принта результатов и на этом всё.

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


def calc_checksum(header: bytes) -> int:
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


def header_to_dict(names: list[str], data: bytes, struct_format: str) -> dict:
    """
    Функция переводит заголовок в словарь
    :param names:
    :param data:
    :param struct_format:
    :return:
    """
    unpacked_data = struct.unpack(struct_format, data)
    return dict(zip(names, unpacked_data))


class Traceroute:
    """
    Класс Traceroute реализует работу консольной утилиты
    """

    def __init__(self, destination_host: str, amount_of_packets: int, max_hops: int, packet_size: int, timeout: int):
        self.destination_host = destination_host
        self.amount_of_packets = amount_of_packets
        self.max_hops = max_hops
        self.packet_size = packet_size
        self.timeout = timeout
        self.previous_sender_hostname = ''
        self.__MIN_SLEEP = 1000
        self.id = os.getpid() & 0xffff
        self.seq = 0
        self.__ICMP_ECHO_REQUEST = 8
        self.__icmp_keys = ['type', 'code', 'checksum', 'identifier', 'sequence number']
        self.__ip_keys = ['VersionIHL', 'Type_of_Service', 'Total_Length', 'Identification', 'Flags_FragOffset', 'TTL',
                          'Protocol', 'Header_Checksum', 'Source_IP', 'Destination_IP']
        self.__IP_STRUCT_FORMAT = '!BBHHHBBHII'
        self.__ICMP_STRUCT_FORMAT = '!BBHHH'
        self.ttl = 1

        try:
            self.destination_ip = destination_to_ip(self.destination_host)
        except socket.gaierror:
            self.destination_ip = None

    def print_start_line(self) -> None:
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

    def print_host_unknown(self) -> None:
        """
        Вывод утилиты в случае, если был передан неверный destination
        :return:
        """
        print(Fore.RED + f'traceroute: unknown host {self.destination_host}')

    # TODO понять и доделать случай таймаута.
    def print_timeout(self) -> None:
        """
        Функция для вывода случая, когда нет ответа на запрос и проходит timeout.
        :return:
        """
        print(f'{self.ttl} * ', end='')
        if self.seq == self.amount_of_packets:
            print()

    # TODO Допи'сать сам вывод консольной утилиты
    def print_trace(self, delay: float, ip_header: dict) -> None:
        """
        Вывод пути для хоста
        :param delay:
        :param ip_header:
        :return:
        """
        ip_address = socket.inet_ntoa(struct.pack('!I', ip_header['Source_IP']))
        try:
            sender_hostname = socket.gethostbyaddr(ip_address)[0]
        except socket.error:
            sender_hostname = ip_address

        # Проверка на то, что мы не ходим по одному и тому же хосту
        if self.previous_sender_hostname != sender_hostname:
            if self.ttl < self.max_hops:
                print(f'{self.ttl} {sender_hostname} {ip_address} {delay}ms')

            self.previous_sender_hostname = sender_hostname

    def start_traceroute(self) -> None:
        """
        В этой функции описана основная логика работы traceroute'а
        Таким образом, идёт цикл, пока TimeToLive не превысит максимального значения
        :return:
        """
        icmp_header = None
        while self.ttl <= self.max_hops:
            self.seq = 0

            for i in range(self.amount_of_packets):
                icmp_header = self.tracer()

            self.ttl += 1

            if icmp_header is not None:
                if icmp_header['type'] == 0:
                    break

    def tracer(self) -> dict | None:
        """
        Функция возвращает icmp_header, в этой функции идёт создание сокета
        :return:
        """
        try:
            icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
            icmp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, self.ttl)
        except socket.error:
            print(Fore.RED + f'Error: {socket.error}')
            print(Fore.YELLOW + 'WARNING: You must run traceroute as root in order to send ICMP messages')

            sys.exit()

        self.seq += 1

        sent_time = self.send_icmp_echo(icmp_socket)

        if sent_time is None:
            return

        receive_time, icmp_header, ip_header = self.receive_icmp_reply(icmp_socket)

        icmp_socket.close()
        if receive_time:
            delay = (receive_time - sent_time) * 1000.0
            self.print_trace(delay, ip_header)

        return icmp_header

    # TODO Придумать более осознанное название для данной функции, так как непонятно, почему называется
    #  send_icmp_echo, когда на деле эта функция возвращает время (в мс) и может логичней будет придумать что-то
    #  вроде get_icmp_echo или другое
    def send_icmp_echo(self, icmp_socket: socket) -> float | None:
        """
        Функция, отправляющая icmp_echo запрос, на выходе получаем время, за которое прошло это дело.
        :param icmp_socket:
        :return:
        """
        header = struct.pack(self.__ICMP_STRUCT_FORMAT, self.__ICMP_ECHO_REQUEST, 0, 0, self.id, self.seq)
        start_value = 65
        payload = []
        for i in range(start_value, start_value + self.packet_size):
            payload.append(i & 0xff)

        data = bytes(payload)

        checksum = calc_checksum(header + data)
        header = struct.pack(self.__ICMP_STRUCT_FORMAT, self.__ICMP_ECHO_REQUEST, 0, checksum, self.id, self.seq)

        packet = header + data

        send_time = timer

        try:
            icmp_socket.sendto(packet, (self.destination_host, 1))
        except socket.error as err:
            print(f'Socket error: {err}')
            icmp_socket.close()
            return

        return send_time

    # --------------------

    # TODO здесь тоже предложение или изменить название функции, или разделить эту функцию на две, чтобы был понятен
    #  смысл, а то я уже начинаю путаться, что у нас делает каждая из этих функций
    def receive_icmp_reply(self, icmp_socket: socket) -> (float, dict, dict):
        """
        Функция принимает на вход сокет и на выходе выдаёт три параметра:
        Время получения пакета, ICMP-header и IP-header
        :param icmp_socket:
        :return:
        """
        timeout = self.timeout / 1000

        reads, send, excepts = select.select([icmp_socket], [], [], timeout)

        receive_time = timer

        if not reads:  # timeout
            self.print_timeout()
            return None, None, None

        packet_data, address = icmp_socket.recvfrom(2048)

        icmp_header = header_to_dict(self.__icmp_keys, packet_data[20:28], self.__ICMP_STRUCT_FORMAT)

        ip_header = header_to_dict(self.__ip_keys, packet_data[:20], self.__IP_STRUCT_FORMAT)

        return receive_time, icmp_header, ip_header

    # ------------

    # TODO По сути, можно здесь оставить эту функцию единственной public, так как это единственная функция,
    #  которую мы вызываем в этом проекте в main'e, предложение отрефакторить это слегка.
    def traceroute(self) -> None:
        """
        Функция для вызова консольной утилиты traceroute.
        :return:
        """
        if self.destination_ip:
            self.print_start_line()
            try:
                self.start_traceroute()
            except KeyboardInterrupt:
                print('The program has been stopped by Ctrl+C')
                sys.exit()
        else:
            self.print_host_unknown()


def start_traceroute(destination: str, amount_of_packets=3, max_hops=30, packet_size=52, timeout=1000) -> None:
    traceroute = Traceroute(destination, amount_of_packets, max_hops, packet_size, timeout)
    traceroute.traceroute()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Traceroute',
        description='Program for displaying possible paths and measuring transit delays of packets',
        epilog='coded by Murzin Sviatoslav and Iuriev Artem')
    parser.add_argument('destination_host', type=str)
    parser.add_argument('-m', '--max-hops', required=False, type=int, default=3)
    parser.add_argument('-s', '--packet-size', required=False, type=int, default=52)
    parser.add_argument('-a', '--packet-amount', required=False, type=int, default=3)
    parser.add_argument('-t', '--timeout', required=False, type=int, default=1000)
    # args = parser.parse_args(sys.argv[1:])
    args = parser.parse_args(['www.mursvet.ru'])
    destination_host = args.destination_host
    max_hops = args.max_hops
    packet_size = args.packet_size
    icmp_packets = 3
    start_traceroute(destination_host)
