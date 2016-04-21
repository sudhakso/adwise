'''
Created on Apr 18, 2016

@author: sonu
'''
from pyes import MultiMatchQuery


class multifield_querymapper():
    boost_constant = "^"

    def __init__(self, weighted_fields):
        self._query_fields = []
        for field in weighted_fields.keys():
            self._query_fields.append("%s%s%s" % (
                                    field, multifield_querymapper.boost_constant,
                                    str(weighted_fields[field])))
        self._type = "multi-field"

    @property
    def type(self):
        return self._type

    @property
    def fields(self):
        return self._query_fields

    def create_query(self, querystring):
        return MultiMatchQuery(fields=self.fields, text=querystring)
