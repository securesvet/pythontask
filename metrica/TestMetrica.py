import unittest
from handle import *

filename = 'test_file.txt'


class TestMetrica(unittest.TestCase):
    def test_overall_counts_one(self):
        # 9 + 5 = 14
        self.assertEqual(counting_all_visit(filename), 14)

    def test_unique_counts(self):
        # 2 user agents --> 2 unique visitors
        self.assertEqual(counting_all_unique_visitor(filename), 2)


if __name__ == '__main__':
    unittest.main()
