# -*- coding: latin-1 -*-

"""Partnership with the Champlitte museum."""

__authors__ = 'User:Jean-Frédéric'

from uploadlibrary import metadata


class ChamplitteRecord(metadata.MetadataRecord):

    """Represent a record, with its associated metadata."""

    def get_title(self):
        """Return the title for the file."""
        name = self.__dict__.get('JOCONDE_TITR',
                                 self.__dict__.get('JOCONDE_DENO', ""))
        return "%s - %s - CG70" % (name, self.INV)


class ChamplitteMetadataCollection(metadata.MetadataCollection):

    """Processing a collection of Records in various ways."""

    def handle_record(self, row):
        """Handle a record."""

        joconde_field = row.pop('Actimuse::_Export_Global DMF').split('\n')
        joconde = dict(zip(["JOCONDE_%s" % x for x in joconde_field[0::2]],
                            joconde_field[1::2]))
        row.update(joconde)
        return ChamplitteRecord(**row)
