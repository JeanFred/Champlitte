# -*- coding: utf-8 -*-

"""Partnership with the Champlitte museum."""
from StringIO import StringIO

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
        url = self.make_url(row.get('Support'), row.get('Cote'))
        return metadata.MetadataRecord(url, row)

    @staticmethod
    def make_url(support, cote):
        base_url = 'http://musees.cg70.fr/wikimedia/2006'
        return "%s/%s/%s_tif/%s.tif" % (base_url, support, support, cote)

def main(args):
    """Main method."""
    collection = ChamplitteMetadataCollection()
#    csv_file = 'DV5_M0354_2006_9.csv'
    csv_file = '2006_7.csv'
    collection.retrieve_metadata_from_csv(csv_file, delimiter=',')

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
            #'JOCONDE_TECH': commonprocessors.map_and_apply_technique(separator=";"),
            'JOCONDE_DIMS': (commonprocessors.process_DIMS, {}),
            'JOCONDE_DOMN': commonprocessors.split_and_keep_as_list(separator=';'),
            'JOCONDE_DESC': commonprocessors.wrap_with_template(template='fr'),
            'JOCONDE_REF': commonprocessors.wrap_within_pattern(pattern='{{online databases|{{Joconde|%s}}}}'),
            'JOCONDE_DACQ': commonprocessors.wrap_within_pattern(pattern='{{ProvenanceEvent|time=%s|type=acquisition|newowner=Musées de la Haute-Saône}}'),
            'JOCONDE_PERI': (commonprocessors.look_for_date, {})

        }
        categories_counter, categories_count_per_file = collection.post_process_collection(mapping_methods)
        # metadata.categorisation_statistics(categories_counter, categories_count_per_file)

    template_name = 'User:Jean-Frédéric/Champlitte/Ingestion'.encode('utf-8')
    front_titlefmt = ""
    #variable_titlefmt = "%(JOCONDE_TITR)s (%(JOCONDE_DENO)s)"
    variable_titlefmt = "%(JOCONDE_DENO)s"
    rear_titlefmt = " - Musées de la Haute-Saône - %(JOCONDE_REF)s"
    reader = iter(collection.records)
    string = StringIO()
    collection.write_metadata_to_xml(string)
    print string.getvalue()
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
