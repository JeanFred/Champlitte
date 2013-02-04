# -*- coding: latin-1 -*-

"""Partnership with the Champlitte museum − main task process."""

import sys
sys.path.append('../MassUploadLibrary')
from Champlitte import ChamplitteMetadataCollection, ChamplitteRecord
from uploadlibrary import PostProcessing


def main(index):
    """Main method."""
    processor = ChamplitteMetadataCollection()
    csv_file = 'DV5_M0354_2003_3.csv'
    processor.retrieve_metadata_from_csv(csv_file)

    mapping = {
        'JOCONDE_DIMS': PostProcessing.process_DIMS,
    }
    processor.post_process_collection(mapping)

    processor.print_metadata_of_record(index)
    #for record in processor.records:
        #print record.get_title()
    #print "\n".join(["%s %s" % x for x in parser.records[0].__dict__.items()])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
