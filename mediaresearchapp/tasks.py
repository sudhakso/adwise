'''
Created on April 1, 2016

@author: sonu
'''

from __future__ import absolute_import

import datetime
import json
from celery import shared_task
from celery import Task
from mediacontentapp.models import Campaign, OOHMediaSource
from mediaresearchapp.models import SearchQuery, ResearchResult
from celery import Celery
from mediaresearchapp.serializers import ResearchResultSerializer
from rest_framework.renderers import JSONRenderer
from django.core import serializers
from mediacontentapp.serializers import CampaignSerializer
from mediaresearchapp.querymapper import multifield_querymapper
from pyes import ES
from pyes import MatchAllQuery, QueryStringQuery, MultiMatchQuery


class BasicSearchTask(Task):
    ignore_errors = True

    def run(self, *args, **kwargs):
        start = datetime.datetime.now()
        print 'Searching %s ...' % kwargs['raw_strings']
        # Get all campaigns
        queryset = Campaign.objects.all()
        camps = []
        for acamp in queryset:
            camps.append(acamp)
        end = datetime.datetime.now()
        elapsed_time = end - start
        _rr = ResearchResult(campaigns=camps,
                             query_runtime_duration=elapsed_time.total_seconds())
        rr = _rr.save()
        ser = ResearchResultSerializer(rr, many=False)
        _srjson = json.dumps(ser.data)
        return _srjson


class CampaignQuerySearchTask(Task):
    ignore_errors = True
    # TBD (create the end-point through the controller)
    ignore_errors = True
    _es = None

    @property
    def es(self):
        if self._es is None:
            self._es = ES("127.0.0.1:9200")
        return self._es

    def run(self, *args, **kwargs):
        wfields = {"category": 4, "tag": 3, "city": 2, "description": 1}
        start = datetime.datetime.now()
        print 'Searching %s ...' % kwargs['raw_strings']
        # Field ranking
        if 'fields' in kwargs:
            wfields = kwargs['fields']
        qm = multifield_querymapper(wfields)
        q4 = qm.create_query(kwargs['raw_strings'])
        resultset = self.es.search(q4)
        ids = [r['id'] for r in resultset]
        print ids
        camps = Campaign.objects.filter(id__in=set(ids))
        end = datetime.datetime.now()
        elapsed_time = end - start
        _rr = ResearchResult(campaigns=camps,
                             query_runtime_duration=elapsed_time.total_seconds(
                                                            ))
        rr = _rr.save()
        ser = ResearchResultSerializer(rr, many=False)
        _srjson = json.dumps(ser.data, encoding='utf-8')
        print _srjson
        return _srjson


class OOHQuerySearchTask(Task):
    ignore_errors = True
    _es = None

    @property
    def es(self):
        if self._es is None:
            self._es = ES("127.0.0.1:9200")
        return self._es

    def run(self, *args, **kwargs):
        start = datetime.datetime.now()
        print 'Searching %s ...' % kwargs['raw_strings']
        # Field ranking
        qm = multifield_querymapper(kwargs['fields'])
        q4 = qm.create_query(kwargs['raw_strings'])
        resultset = self.es.search(q4)
        ids = [r['id'] for r in resultset]
        print 'Search returned following instances %s' % ids
        oohs = OOHMediaSource.objects.filter(id__in=set(ids))
        end = datetime.datetime.now()
        elapsed_time = end - start
        _rr = ResearchResult(oohs=oohs,
                             query_runtime_duration=elapsed_time.total_seconds(
                                                            ))
        rr = _rr.save()
        ser = ResearchResultSerializer(rr, many=False)
        _srjson = json.dumps(ser.data, encoding='utf-8')
        print _srjson
        return _srjson


@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param


@shared_task
def search_pipeline(raw_strings, fields, values):
    print 'Celery: Search query (%s)' % (raw_strings)
    # TBD(Sonu): Delegate to pyES
    camps = Campaign.objects.all()
    return camps
#     rr = ResearchResult.save(campaigns=camps)
#     return rr
