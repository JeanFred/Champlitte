# -*- coding: latin-1 -*-

"""Partnership with the Champlitte museum − handling record."""

__authors__ = 'User:Jean-Frédéric'

import re
import sys
import pickle
from os.path import join
sys.path.append('../pywikipedia')
import wikipedia as pywikibot
import pywikibot.textlib as textlib


class Record:

    """Represent a record, with its associated metadata."""

    def __init__(self, **entries):
        """Constructor.

        Update the object with dictionary passed as argument.

        """
        self.__dict__.update(entries)

    def post_process(self):
        """Post-process the Record.

        For each field of the record,
        call the relevant post-processing method.

        """
        mapping = {
            'JOCONDE_DIMS': self.process_DIMS,
            }
        for field in self.__dict__.keys():
            if field in mapping.keys():
                mapping[field](field)

    def process_DIMS(self, field):
        """Process the Joconde DIMS field.

        Split the field by each dimension
        Build a dictionary with it
        Update the Record dictionary with it

        """
        DIMS = self.__dict__.pop(field, None)
        pattern = '(\w)\.\s?([\d,]*)\s?(\w*)\s?;?\s?'
        splitted = filter(lambda a: a != u'', re.split(pattern, DIMS))
        DIMS_BIS = dict(zip(["_".join([field, x]) for x in splitted[0::3]],
                            [float(x.replace(',', '.')) for x in splitted[1::3]]))
        if len(splitted[2::3]) > 0:
            DIMS_BIS["_".join([field, 'unit'])] = splitted[2::3][0]
        self.__dict__.update(**DIMS_BIS)

    def get_title(self):
        """Return the title for the file."""
        name = self.__dict__.get('JOCONDE_TITR',
                                 self.__dict__.get('JOCONDE_DENO', ""))
        return "%s - %s - CG70" % (name, self.INV)

    def to_template(self, template=u'User:Jean-Frédéric/Champlitte/Ingestion'):
        """Return the Record as a MediaWiki template."""
        return textlib.glue_template_and_params((template,
                                                 self.__dict__))

    def to_disk(self, directory):
        """Write the OAI record on disk in a given repository.

        Serialise the record and name it as the file title,
        do nothing if anything goes wrong
        (we might want to log that)

        """
        fileName = join(directory, self.get_title() + '.dump')
        try:
            with open(fileName, 'w') as f:
                pickle.dump(self, f)
        except Exception, e:
            print "Could not pickle record %s \n %s" % (fileName, e)
