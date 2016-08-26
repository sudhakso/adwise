'''
Created on Apr 18, 2016

@author: sonu
'''
from pyes import TermQuery
from pyes import MultiMatchQuery
import sys
from pyes.query import RegexTermQuery


class querytype_factory():
    def __init__(self):
        '''
        Constructor
        '''
        self._current_ = sys.modules[__name__]

    # Factory can create mappers that are in this module.
    # TBD (Note: Sonu) Extend this to other module mappers.
    def create_mapper(self, mappertype, args):
        class_ = getattr(self._current_, '%s_%s' % (
                                            mappertype, 'querymapper'))
        return class_(args)


class multifield_querymapper():
    boost_constant = "^"

    def __init__(self, weighted_fields):
        self._query_fields = []
        for field in weighted_fields.keys():
            self._query_fields.append("%s%s%s" % (
                                field, multifield_querymapper.boost_constant,
                                str(weighted_fields[field])))
        self._type = "multifield"

    @property
    def type(self):
        return self._type

    @property
    def fields(self):
        return self._query_fields

    def create_query(self, querystring):
        return MultiMatchQuery(fields=self.fields, text=querystring)


class regexp_querymapper():
    boost_constant = "^"

    def __init__(self, field):
        self._query_field = field
        self._type = "regexpquery"

    @property
    def type(self):
        return self._type

    @property
    def field(self):
        return self._query_field

    def create_query(self, querystring):
        # One field allowed. Rest are ignored.
        field_name = self.field.keys()[0]
        boost_value = self.field[field_name]

        return RegexTermQuery(field_name,
                              querystring,
                              boost_value)
