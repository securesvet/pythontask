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


def calc_checksum(header):
    # Initialise checksum and overflow
    checksum = 0
    overflow = 0

    # For every word (16-bits)
    for i in range(0, len(header), 2):
        word = header[i] + (header[i + 1] << 8)

        # Add the current word to the checksum
        checksum = checksum + word
        # Separate the overflow
        overflow = checksum >> 16
        # While there is an overflow
        while overflow > 0:
            # Remove the overflow bits
            checksum = checksum & 0xFFFF
            # Add the overflow bits
            checksum = checksum + overflow
            # Calculate the overflow again
            overflow = checksum >> 16

    # There's always a chance that after calculating the checksum
    # across the header, ther is *still* an overflow, so need to
    # check for that
    overflow = checksum >> 16
    while overflow > 0:
        checksum = checksum & 0xFFFF
        checksum = checksum + overflow
        overflow = checksum >> 16

    # Ones-compliment and return
    checksum = ~checksum
    checksum = checksum & 0xFFFF

    return checksum


class Traceroute:
    def __init__(self, destination_host: str, icmp_packets: int, max_hops: int, packet_size: int, timeout: int):
        self.destination_host = destination_host
        self.icmp_packets = icmp_packets
        self.max_hops = max_hops
        self.packet_size = packet_size
        self.timeout = timeout

        self.ttl = 1

        try:
            self.destination_ip = destination_to_ip(self.destination_host)
        except socket.gaierror:
            self.print_host_unknown()

    def print_start_line(self):
        print(f'traceroute to {self.destination_host} ({self.destination_ip}),'
              f' {self.max_hops} hops max, {self.packet_size} byte packets ')

    def print_host_unknown(self):
        print(f'traceroute: unknown host {self.destination_host}')

    def tracer(self):
        try:
            icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('ICMP'))
            icmp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, self.ttl)
        except socket.error:
            print(f'Error: {socket.error}')

    def init_traceroute(self):
        self.print_start_line()


def start_traceroute(destination_host: str, icmp_packets=3, packet_size=52, max_hops=32, timeout=1000):
    traceroute = Traceroute(destination_host, icmp_packets, packet_size, max_hops, timeout)
    traceroute.init_traceroute()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Traceroute',
                                     description='Program for displaying possible paths and measuring transit delays of'
                                                 ' packets',
                                     epilog='coded by Murzin Sviatoslav and Iuriev Artem')
    parser.add_argument('destination_host', type=str)
    parser.add_argument('-m', '--max_hops', required=False, type=int)
    parser.add_argument('-p', '--packet_size', required=False, type=int)
    args = parser.parse_args(sys.argv[1:])
    destination_host = args.destination_host
    max_hops = args.max_hops
    packet_size = args.packet_size
    icmp_packets = 3
    start_traceroute(destination_host)
