import unittest
import datetime
from unittest.mock import Mock, patch

from scraper import scrap

class TestDownloadDiario(unittest.TestCase):
    def test_get_current_date(self):
        time1 = 1727635460.2906659
        expected_r1 = "29-09-2024"
       
        datetime_mock = Mock(wraps=datetime.datetime)
        datetime_mock.now.return_value = datetime.datetime.fromtimestamp(time1)
        with patch('datetime.datetime', new=datetime_mock):
            r = scrap.get_current_date()
            self.assertEqual(expected_r1, r)
        