# -*- coding: utf-8 -*-

"""Partnership with the Champlitte museum."""

__authors__ = 'User:Jean-Frédéric'

import sys
from uploadlibrary import metadata
import uploadlibrary.PostProcessing as commonprocessors
from uploadlibrary.UploadBot import DataIngestionBot, UploadBotArgumentParser

reload(sys)
sys.setdefaultencoding('utf-8')


class ChamplitteMetadataCollection(metadata.MetadataCollection):
    """Processing a collection of Records in various ways."""

    def handle_record(self, row):
        """Handle a record."""

        joconde_field = row.pop('Actimuse::_Export_Global DMF').split('\n')
        joconde = dict(zip(["JOCONDE_%s" % x for x in joconde_field[0::2]],
                           joconde_field[1::2]))
        row.update(joconde)
        return metadata.MetadataRecord(".jpg", row)


def main(args):
    """Main method."""
    collection = ChamplitteMetadataCollection()
    csv_file = 'DV5_M0354_2003_3.csv'
    collection.retrieve_metadata_from_csv(csv_file)

    alignment_template = 'User:Jean-Frédéric/AlignmentRow'.encode('utf-8')

    if args.prepare_alignment:
        for key, value in collection.count_metadata_values().items():
            collection.write_dict_as_wiki(value, key, 'wiki',
                                          alignment_template)

    if args.post_process:
        mapping_fields = []
        mapper = commonprocessors.retrieve_metadata_alignments(mapping_fields,
                                                               alignment_template)

        mapping_methods = {
            'JOCONDE_TECH': commonprocessors.map_and_apply_technique(separator=";"),
            'JOCONDE_DIMS': (commonprocessors.process_DIMS, {}),
        }
        categories_counter, categories_count_per_file = collection.post_process_collection(mapping_methods)
        # metadata.categorisation_statistics(categories_counter, categories_count_per_file)

    template_name = 'User:Jean-Frédéric/Champlitte/Ingestion'.encode('utf-8')
    front_titlefmt = ""
    #variable_titlefmt = "%(JOCONDE_TITR)s (%(JOCONDE_DENO)s)"
    variable_titlefmt = "%(JOCONDE_DENO)s"
    rear_titlefmt = " - Musées de la Haute-Saône - %(Actimuse::_REF Export)s"
    reader = iter(collection.records)
    uploadBot = DataIngestionBot(reader=reader,
                                 front_titlefmt=front_titlefmt,
                                 rear_titlefmt=rear_titlefmt,
                                 variable_titlefmt=variable_titlefmt,
                                 pagefmt=template_name,
                                 subst=False,
                                 verifyDescription=True)
    if args.upload:
        uploadBot.doSingle()
    elif args.dry_run:
        uploadBot.dry_run()


if __name__ == "__main__":
    parser = UploadBotArgumentParser()
    arguments = parser.parse_args()
    if not any(arguments.__dict__.values()):
        parser.print_help()
    else:
        main(arguments)
