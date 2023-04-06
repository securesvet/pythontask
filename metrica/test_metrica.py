import unittest
from datetime import timedelta
from unittest.mock import MagicMock, patch
from visit_db_queries import *


class TestVisitDB(unittest.TestCase):

    @patch('visit_db.Visit.create_table')
    def test_create_visit_table(self, mock_create_table):
        create_visit_table()
        mock_create_table.assert_called_once()

    def test_add_visit(self):
        ip_address = "localhost"
        with patch('visit_db.Visit.get',
                   return_value=MagicMock(count_visits=0, last_visit=datetime.now(), today_visit=0)) as mock_get:
            add_visit(ip_address)
            mock_get.assert_called_once_with(Visit.ip_address == ip_address)

    def test_get_table(self):
        with patch('builtins.print') as mock_print:
            get_table()
            mock_print.assert_called()

    def test_get_counts_overall(self):
        with patch('visit_db.Visit.select',
                   return_value=[MagicMock(count_visits=1), MagicMock(count_visits=2)]) as mock_select:
            count_overall = get_counts_overall()
            mock_select.assert_called_once()
            self.assertEqual(count_overall, 3)

    def test_get_today_overall_visits(self):
        with patch('visit_db.Visit.select', return_value=[MagicMock(last_visit=datetime.now(), today_visit=2),
                                                          MagicMock(last_visit=datetime.now(),
                                                                    today_visit=1)]) as mock_select:
            count_today_overall = get_today_overall_visits()
            mock_select.assert_called_once()
            self.assertEqual(count_today_overall, 3)

    def test_get_today_unique_visits(self):
        with patch('visit_db.Visit.select', return_value=[MagicMock(last_visit=datetime.now()),
                                                          MagicMock(last_visit=datetime.now()), MagicMock(
                last_visit=datetime.now() - timedelta(days=1))]) as mock_select:
            count_of_unique_visits_today = get_today_unique_visits()
            mock_select.assert_called_once()
            self.assertEqual(count_of_unique_visits_today, 2)

    @patch('visit_db.db.close')
    def test_visit_close_connection(self, mock_close):
        visit_close_connection()
        mock_close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
