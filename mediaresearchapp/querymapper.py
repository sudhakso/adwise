'''
Created on Apr 18, 2016

@author: sonu
'''
from pyes import TermQuery
from pyes import MultiMatchQuery
import sys
from pyes.query import RegexTermQuery, FilteredQuery,\
 MatchAllQuery
from pyes.filters import *


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


class structured_querymapper():

    def __init__(self, dummy):
        self._type = "structured"
        self._filters = []
        self._filtertype = None
        self._query_field = []

    @property
    def type(self):
        return self._type

    @property
    def field(self):
        return self._query_field

    def create_query(self, sql):
        # query  filter. Rest are ignored.
        if "termquery" in sql.keys():
            # Create Term filter
            terms = sql['termquery']
            for term in terms:
                self._query_field.append(term.keys()[0])
                _tf = TermFilter(term.keys()[0], term[term.keys()[0]])
                self._filters.append(_tf)
        if "geodistancefilter" in sql.keys():
            # Prepare distance filter
            geoterm = sql['geodistancefilter']
            geofieldname = geoterm['field']
            geofieldvalue = geoterm['fieldvalue']
            _gf = GeoDistanceFilter(geofieldname,
                                    geofieldvalue,
                                    geoterm['distance'],
                                    'arc', 'km')
            self._filters.append(_gf)
            self._query_field.append(geofieldname)
        if "optype" in sql.keys():
            # Condition filters
            if sql['optype'].lower() == 'and':
                self._filtertype = ANDFilter(self._filters)
            if sql['optype'].lower() == 'or':
                self._filtertype = ORFilter(self._filters)
        else:
            self._filtertype = ANDFilter(self._filters)
        return FilteredQuery(MatchAllQuery(), self._filtertype)
