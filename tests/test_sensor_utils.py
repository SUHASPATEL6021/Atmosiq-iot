import unittest
from io import StringIO
from sensor_utils import load_readings

class SensorTests(unittest.TestCase):
    def test_valid_csv(self):
        df = load_readings(StringIO("timestamp,temperature_c,humidity_pct\n2026-11-18,25,50\n"))
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["temperature_c"], 25)
    def test_missing_column(self):
        with self.assertRaises(ValueError):
            load_readings(StringIO("timestamp,temperature_c\n2026-11-18,25\n"))
    def test_invalid_readings(self):
        with self.assertRaises(ValueError):
            load_readings(StringIO("timestamp,temperature_c,humidity_pct\ninvalid,999,500\n"))
    def test_bad_csv(self):
        with self.assertRaises(ValueError):
            load_readings(StringIO(""))
    def test_mixed_readings(self):
        df = load_readings(StringIO("timestamp,temperature_c,humidity_pct\n2026-11-18,25,50\n2026-11-19,25,150\n"))
        self.assertEqual(len(df), 1)

if __name__ == "__main__":
    unittest.main()
