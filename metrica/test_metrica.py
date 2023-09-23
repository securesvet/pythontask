from visit_db_queries import *
import unittest
from unittest.mock import patch
from visit_db import *


class TestVisit(unittest.TestCase):
    def setUp(self):
        self.db = SqliteDatabase(':memory:')
        self.db.bind([IP, IPVisit], bind_refs=False, bind_backrefs=False)
        self.db.connect()
        self.db.create_tables([IP, IPVisit])

    def tearDown(self):
        self.db.drop_tables([IP, IPVisit])
        self.db.close()

    def test_create_visit_table(self):
        create_visit_table()
        self.assertTrue(IP.table_exists())
        self.assertTrue(IPVisit.table_exists())

    def test_add_visit(self):
        add_visit('192.168.0.1',
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3')
        self.assertEqual(IP.select().count(), 1)
        self.assertEqual(IPVisit.select().count(), 1)

    def test_add_visit_existing_ip(self):
        IP.create(ip_address='192.168.0.1')
        add_visit('192.168.0.1',
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3')
        self.assertEqual(IP.select().count(), 1)
        self.assertEqual(IPVisit.select().count(), 1)

    def test_get_all_visits(self):
        IP.create(ip_address='192.168.0.1')
        IPVisit.create(ip_id=1,
                       user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                  ' Chrome/58.0.3029.110 Safari/537.3',
                       date_time=datetime.now())
        visits = get_all_visits()
        self.assertEqual(len(visits), 1)
        self.assertIsInstance(visits[0], Visit)

    def test_get_all_visits_by_ip_and_dates(self):
        IP.create(ip_address='192.168.0.1')
        IPVisit.create(ip_id=1,
                       user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/58.0.3029.110 Safari/537.3',
                       date_time=datetime.now())
        visits = get_all_visits_by_ip_and_dates('192.168.0.1', datetime.now().replace(hour=0, minute=0, second=0),
                                                datetime.now().replace(hour=23, minute=59, second=59))
        self.assertEqual(len(visits), 1)
        self.assertIsInstance(visits[0], Visit)

    @patch('visit_db.db.close')
    def test_visit_close_connection(self, mock_close):
        visit_close_connection()
        mock_close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
