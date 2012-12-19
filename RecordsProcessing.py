# -*- coding: latin-1 -*-

"""Partnership with the Champlitte museum − handling metadata collection."""

__authors__ = 'User:Jean-Frédéric'

import sys
import codecs
import csv
import UnicodeCSV
from Record import Record


class RecordsProcessing:

    """Processing a collection of Records in various ways."""

    def __init__(self):
        self.records = []

    def retrieve_metadata_from_csv(self, csv_file):
        """Retrieve metadata from the given CSV file."""
        file_handler = codecs.open(csv_file, 'r', 'utf-8')
        csvReader = UnicodeCSV.unicode_csv_dictreader(file_handler,
                                                      delimiter=',')
        try:
            for row in csvReader:
                joconde_field = row.pop('Actimuse::_Export_Global DMF').split('\n')
                joconde = dict(zip(["JOCONDE_%s" % x for x in joconde_field[0::2]],
                                    joconde_field[1::2]))
                row.update(joconde)
                record = Record(**row)
                record.post_process()
                self.records.append(record)
        except csv.Error, e:
            sys.exit('file %s, line %d: %s' % (self.csv_file,
                                               csvReader.line_num, e))

    def print_metadata_of_record(self, index):
        """Print the metadata of the record.

        Print the result of get_title and of to_template.

        """
        print self.records[index].get_title()
        print self.records[index].to_template()
