import unittest

# Path hack.
import sys, os

sys.path.insert(0, os.path.abspath(".."))

import src.timestamp_finder


class DateTextToFilename(unittest.TestCase):
    def test_valid_date_text(self):
        result = src.timestamp_finder.date_text_to_filename("2013:12:01 13:23:12")
        self.assertIsNotNone(result)

    def test_empty_date_text(self):
        result = src.timestamp_finder.date_text_to_filename(": :    :    :")
        self.assertIsNone(result)


class GetTimestamp(unittest.TestCase):
    def test_exif_version_0220(self):
        result = src.timestamp_finder.get_timestamp("tests/test_data/0220.jpg")
        self.assertEqual(result, "20070802_123020")

    def test_exif_version_0221(self):
        result = src.timestamp_finder.get_timestamp("tests/test_data/0221.jpg")
        self.assertEqual(result, "20150704_172516")

    def test_invalid_file(self):
        result = src.timestamp_finder.get_timestamp("tests/test_data/foo.jpg")
        self.assertIsNone(result)
