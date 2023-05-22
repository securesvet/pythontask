import time
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from traceroute import Traceroute, is_valid_ip, destination_to_ip, start_traceroute, calc_checksum, header_to_dict
import socket


class TestFunctions(unittest.TestCase):

    def test_is_valid_ip(self):
        self.assertTrue(is_valid_ip("192.168.0.1"))
        self.assertTrue(is_valid_ip("10.0.0.1"))
        self.assertTrue(is_valid_ip("172.16.0.1"))
        self.assertFalse(is_valid_ip("256.0.0.1"))
        self.assertFalse(is_valid_ip("192.168.0"))
        self.assertFalse(is_valid_ip("192.168.0.1.2"))
        self.assertFalse(is_valid_ip("a192.168.0.1"))

    def test_destination_to_ip(self):
        self.assertEqual(destination_to_ip("www.mursvet.ru"), "80.87.110.79")
        self.assertEqual(destination_to_ip("192.168.0.1"), "192.168.0.1")
        self.assertEqual(destination_to_ip("10.0.0.1"), "10.0.0.1")

    def test_header_to_dict(self):
        header = b'\x45\x00\x00\x28\xbe\xef\x40\x00\x40\x01\x2c\x8e\x7f\x00\x00\x01\x7f\x00\x00\x01'
        icmp_keys = ['type', 'code', 'checksum', 'identifier', 'sequence number']
        ICMP_STRUCT_FORMAT = '!BBHHH'
        expected_output = 0
        icmp_header = header_to_dict(icmp_keys, header[:8], ICMP_STRUCT_FORMAT)
        actual_output = icmp_header['code']
        self.assertEqual(actual_output, expected_output)

    def test_calc_checksum(self):
        header = b'\x45\x00\x00\x28\xbe\xef\x40\x00\x40\x01\x2c\x8e\x7f\x00\x00\x01\x7f\x00\x00\x01'
        expected_output = 0x5551
        actual_output = calc_checksum(header)

        self.assertEqual(actual_output, expected_output)

    def test_print_start_line_with_destination_ip(self):
        traceroute = Traceroute('www.example.com', 3, 30, 52, 1000)
        expected_output = "traceroute to www.example.com (93.184.216.34), 30 hops max, 52 byte packets \n"
        with patch('sys.stdout', new=StringIO()) as fake_output:
            traceroute.print_start_line()
            self.assertEqual(fake_output.getvalue(), expected_output)

    def test_print_start_line_without_destination_ip(self):
        traceroute = Traceroute('invalid.host', 3, 30, 52, 1000)
        expected_output = "traceroute to invalid.host, 30 hops max, 52 byte packets \n"
        with patch('sys.stdout', new=StringIO()) as fake_output:
            traceroute.print_start_line()
            self.assertEqual(fake_output.getvalue(), expected_output)

    def test_print_host_unknown(self):
        traceroute = Traceroute('invalid.host', 3, 30, 52, 1000)
        expected_output = "\x1b[31mtraceroute: unknown host invalid.host\n"
        with patch('sys.stdout', new=StringIO()) as fake_output:
            traceroute.print_host_unknown()
            self.assertEqual(fake_output.getvalue(), expected_output)

    def test_print_timeout(self):
        traceroute = Traceroute('www.example.com', 3, 30, 52, 1000)
        expected_output = '* '
        with patch('sys.stdout', new=StringIO()) as fake_output:
            traceroute.print_timeout()
            self.assertEqual(fake_output.getvalue(), expected_output)

    def test_print_timeout_with_first_seq(self):
        traceroute = Traceroute('www.example.com', 3, 30, 52, 1000)
        traceroute.seq = 1
        traceroute.ttl = 123456789
        expected_output = '123456789 * '
        with patch('sys.stdout', new=StringIO()) as fake_output:
            traceroute.print_timeout()
            self.assertEqual(fake_output.getvalue(), expected_output)

    def test_print_timeout_when_seq_equals_aop(self):
        traceroute = Traceroute('www.example.com', 3, 30, 52, 1000)
        traceroute.seq = 3
        traceroute.ttl = 123456789
        expected_output = '* \n'
        with patch('sys.stdout', new=StringIO()) as fake_output:
            traceroute.print_timeout()
            self.assertEqual(fake_output.getvalue(), expected_output)

    def test_print_trace(self):
        traceroute = Traceroute('www.example.com', 3, 30, 52, 1000)
        traceroute.previous_sender_hostname = 'previous.example.com'
        expected_output = '1 1572390803.dhcp.nefnet.dk (93.184.199.146) 10.0 ms\n'
        ip_header = {
            'Source_IP': 1572390802
        }
        with patch('sys.stdout', new=StringIO()) as fake_output:
            traceroute.print_trace(10.0, ip_header)
            self.assertEqual(fake_output.getvalue(), expected_output)

    def test_print_trace_with_exception(self):
        traceroute = Traceroute('www.example.com', 3, 30, 52, 1000)
        traceroute.previous_sender_hostname = 'previous.example.com'
        expected_output = '1 1572390803.dhcp.nefnet.dk (93.184.199.146) 10.0 ms\n'
        ip_header = {
            'Source_IP': 1572390802
        }
        with patch('sys.stdout', new=StringIO()) as fake_output:
            with self.assertRaises(socket.error):
                traceroute.print_trace(10.0, ip_header)

                raise socket.error("Socket err")
            self.assertEqual(fake_output.getvalue(), expected_output)

    def test_start_traceroute(self):
        traceroute = Traceroute('www.example.com', 3, 30, 52, 1000)
        icmp_header = {
            'type': 0
        }
        with patch('traceroute.Traceroute.start_traceroute', return_value=icmp_header):
            traceroute.start_traceroute()
            self.assertEqual(traceroute.ttl, 1)

    def setUp(self):
        self.traceroute = Traceroute('127.0.0.1', 3, 30, 52, 1000)

    def test_send_icmp_echo_localhost(self):
        expected_result = time.time() + 1
        with patch('socket.socket') as mock_socket:
            with patch('time.perf_counter', return_value=expected_result):
                result = self.traceroute.send_icmp_echo(mock_socket)
                self.assertLess(result, expected_result)

    def test_send_icmp_echo_invalid(self):
        traceroute = Traceroute('256.256.36.1', 3, 30, 52, 1000)
        with patch('socket.socket') as mock_socket:
            mock_socket.sendto = None
            result = traceroute.send_icmp_echo(mock_socket)
            self.assertEquals(result, None)

    def test_traceroute_with_valid_destination(self):
        destination = '127.0.0.1'
        expected_output = 'traceroute to 127.0.0.1 (127.0.0.1), 30 hops max, 52 byte packets\n' \
                          '1 localhost (127.0.0.1) <10 ms'
        with patch('sys.stdout', new=StringIO()) as fake_output:
            with self.assertRaises(SystemExit) as cm:
                start_traceroute(destination)
                self.assertEqual(fake_output.getvalue(), expected_output)
            self.assertEqual(cm.exception.code, None)

    def test_get_icmp_header_exit(self):
        with self.assertRaises(SystemExit) as cm:
            self.traceroute.get_icmp_header()
        self.assertEqual(cm.exception.code, None)

    @patch('socket.socket')
    def test_get_icmp_header(self, mock_socket):
        mock_icmp_socket = mock_socket.return_value
        mock_icmp_socket.recvfrom.return_value = (b'', ('', 0))

        traceroute = Traceroute(self.traceroute.destination_host, self.traceroute.amount_of_packets,
                                self.traceroute.max_hops, self.traceroute.packet_size, self.traceroute.timeout)
        icmp_header = traceroute.get_icmp_header()

        mock_icmp_socket.sendto.assert_called_once()
        mock_icmp_socket.close.assert_called_once()

        self.assertIsNone(icmp_header)

    def test_traceroute(self):
        with self.assertRaises(SystemExit) as cm:
            self.traceroute.traceroute()
        self.assertEqual(cm.exception.code, None)

    def test_traceroute_with_invalid_destination(self):
        destination = 'invalid.host'
        expected_output = "\x1b[31mtraceroute: unknown host invalid.host\n"
        with patch('sys.stdout', new=StringIO()) as fake_output:
            start_traceroute(destination)
            self.assertEqual(fake_output.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()
