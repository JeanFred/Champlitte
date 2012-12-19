#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Unit tests."""

import unittest
import pickle
from os.path import join, dirname
from Record import Record


class TestRecord(unittest.TestCase):

    """Testing methods from Record."""

    @classmethod
    def setUpClass(cls):
        """Retrieve the record from disk by deserialiazation."""
        record_files = ['personnage_militaire_-_1951.3.16_-_CG70.dump']
        func = lambda x: pickle.load(open(join(dirname(__file__), 'data', x)))
        cls.records = map(func, record_files)
        values = {'INV': 'inv', 'JOCONDE_TITR': 'joconde_titr'}
        dummy_record = Record(**values)
        cls.records.append(dummy_record)

    def test_init(self):
        """Test __init__."""
        values = {'A': 'a'}
        record = Record(**values)
        self.assertEqual(record.__dict__, values)

    def test_get_title(self):
        """Test get_title."""
        expected_result = ['personnage militaire - 1951.3.16 (a) - CG70',
                           'joconde_titr - inv - CG70']
        self.assertListEqual(expected_result,
                             map(Record.get_title, self.records))

    def test_to_template(self):
        """Test to_template."""
        expected_result = u'{{Dummy\n|INV=inv\n|JOCONDE_TITR=joconde_titr\n}}'
        self.assertEqual(expected_result,
                         self.records[-1].to_template(template='Dummy'))


if __name__ == "__main__":
    unittest.main()
