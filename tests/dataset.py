import os
import unittest

from darts import TimeSeries

from src.data.dataset import Dataset


class DatasetTest(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir('..')

    def test_electricity(self):
        series = Dataset.get('electricity')

        self.assertIsInstance(series, TimeSeries)
        self.assertEqual(len(series), 26_304)

    def test_traffic(self):
        series = Dataset.get('traffic')

        self.assertIsInstance(series, TimeSeries)
        self.assertEqual(len(series), 17_544)

    def test_exchange_rate(self):
        series = Dataset.get('exchange_rate')

        self.assertIsInstance(series, TimeSeries)
        self.assertEqual(len(series), 7_588)


if __name__ == '__main__':
    unittest.main()
