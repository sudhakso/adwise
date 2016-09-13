'''
Created on Apr 18, 2016

@author: sonu
'''

from pyes import ES
from pyes import MatchAllQuery, QueryStringQuery, MultiMatchQuery
from pyes import RegexTermQuery, TermQuery, FilteredQuery
from pyes.filters import RegexTermFilter
from pyes.filters import *
# from mediaresearchapp.querymapper import multifield_querymapper
# from mediacontentapp.models import Campaign

# test
from mediaresearchapp.tasks import MediaAggregateSQLTask

if __name__ == '__main__':
    es = ES("127.0.0.1:9200", default_indices='mediaaggregate')

# Filters
    filters = [GeoDistanceFilter('location',
                                 [40.0, 9.00],
                                 20, 'arc', 'km')]


#     filters = [TermFilter('message', 'elastic'),
#                GeoDistanceFilter('locations',
#                                  {"lat": 40.0, "lon": 9.00},
#                                  20, 'arc', 'km')
#                ]
    filter = ANDFilter(filters)
    q = FilteredQuery(MatchAllQuery(), filter)
    results = es.search(q)
    for r in results:
        print r
        break


    q4 = RegexTermQuery('city', 'bang.*')
    print q4
    resultset = es.search(q4)
    for r in resultset:
        print r

    query_str = {
                 "query": {
                              "termquery": [
                                            {"fieldname1": "value"},
                                            {"fieldname2": "value"}
                                            ],
                              "geodistancefilter": {
                                                    "field": "locations",
                                                    "fieldvalue": {
                                                                  "lat": 40.0,
                                                                  "lon": 9.00
                                                                  },
                                                    "distance": 20},
                              "optype": "And"
                        }
                }
    query_str2 = {
                 "query": {
                              "geodistancefilter": {
                                                    "field": "locations",
                                                    "fieldvalue": {
                                                                  "lat": 40.0,
                                                                  "lon": 9.00
                                                                  },
                                                    "distance": 20},
                              "termquery": [
                                            {"message": "Trying out Elastic Search, so far so good?"},
                                            ],
                              "optype": "And"
                        }
                }
    query_str3 = {
                 "query": {
                              "termquery": [
                                            {"name": "Inorbit Mall"},
                                            {"city": "Bangalore Bengaluru Pune"}
                                            ],
                              "optype": "And"
                        }
                }
    task = MediaAggregateSQLTask()
    task.run(args=[],
             query=query_str2['query'],
             query_type='structured',
             ignore_failures=True)


# Basic 1
    q2 = MatchAllQuery().search()
    # Displays the ES JSON query.
    print q2

    resultset = es.search(q2)
    for r in resultset:
        print r
        break


# Basic 2
    q1 = QueryStringQuery(query="the joggers park with some")
    print q1
    resultset = es.search(q1)
    for r in resultset:
        print r
        break


# Basic 3
    q3 = MultiMatchQuery(fields=["tag^3", "description"],
                         text="banking ")
    print q3
    resultset = es.search(q3)
    for r in resultset:
        print r

# Basic
#     wfields = {"category": 4, "tag": 3, "description": 1}
#     qm = multifield_querymapper(wfields)
#     q4 = qm.create_query("the joggers park with some")
#     print str(q4)
#     resultset = es.search(q4)
#     ids = [r['id'] for r in resultset]
#     print ids
#     camps = Campaign.objects.filter(id__in=set(ids))
#     print camps



