# -*- coding: latin-1 -*-

"""Partnership with the Champlitte museum − main task process."""

import sys
from RecordsProcessing import RecordsProcessing


def main(index):
    """Main method."""
    processor = RecordsProcessing()
    csv_file = 'DV5_M0354_2003_3.csv'
    processor.retrieve_metadata_from_csv(csv_file)
    #processor.print_metadata_of_record(index)
    #for record in processor.records:
        #print record.get_title()
    #print "\n".join(["%s %s" % x for x in parser.records[0].__dict__.items()])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
