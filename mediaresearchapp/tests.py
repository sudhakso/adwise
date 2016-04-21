'''
Created on Apr 18, 2016

@author: sonu
'''

from pyes import ES
from pyes import MatchAllQuery, QueryStringQuery, MultiMatchQuery
from mediaresearchapp.querymapper import multifield_querymapper
from mediacontentapp.models import Campaign


if __name__ == '__main__':
    es = ES("127.0.0.1:9200")

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
                         text="joggers airfare")
    print q3
    resultset = es.search(q3)
    for r in resultset:
        print r

# Basic
    wfields = {"category": 4, "tag": 3, "description": 1}
    qm = multifield_querymapper(wfields)
    q4 = qm.create_query("the joggers park with some")
    print q4
    resultset = es.search(q4)
    ids = [r['id'] for r in resultset]
    print ids
    camps = Campaign.objects.filter(id__in=set(ids))
    print camps



