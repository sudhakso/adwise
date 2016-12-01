'''
Created on April 1, 2016

@author: sonu
'''

from __future__ import absolute_import

import datetime
import json
from celery import shared_task
from celery import Task
from mediacontentapp.models import Campaign, OOHMediaSource,\
 MediaAggregate, Playing
from mediaresearchapp.models import ResearchResult, MediaAggregateResearchResult
from mediaresearchapp.serializers import ResearchResultSerializer,\
 MediaAggregateResearchResultSerializer
from mediaresearchapp.querymapper import multifield_querymapper,\
 querytype_factory
from pyes import ES


class CampaignQuerySearchTask(Task):
    # TBD (create the end-point through the controller)
    ignore_errors = True
    _es = None
    _qf = None

    @property
    def es(self):
        if self._es is None:
            self._es = ES("127.0.0.1:9200", default_indices='campaign')
        return self._es

    @property
    def qf(self):
        if self._qf is None:
            self._qf = querytype_factory()
        return self._qf

    def run(self, *args, **kwargs):
        start = datetime.datetime.now()
        # Field ranking
        if 'fields' in kwargs and kwargs['fields'].keys():
            wfields = kwargs['fields']
        else:
            # default
            wfields = {"category": 4}

        print 'Searching %s ...' % kwargs['raw_strings']
        print 'Fields for query %s ...' % wfields

        qm = self.qf.create_mapper(kwargs['query_type'], wfields)
        q4 = qm.create_query(kwargs['raw_strings'])
        resultset = self.es.search(q4)
        ids = [r['id'] for r in resultset]

        print 'Search returned following campaigns %s ...' % ids

        # Get all campaing objects
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
            self._es = ES("127.0.0.1:9200", default_indices='oohmediasource')
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


class MediaAggregateQuerySearchTask(Task):
    # TBD (create the end-point through the controller)
    ignore_errors = True
    _es = None
    _qf = None

    @property
    def es(self):
        if self._es is None:
            self._es = ES("127.0.0.1:9200", default_indices='mediaaggregate')
        return self._es

    @property
    def qf(self):
        if self._qf is None:
            self._qf = querytype_factory()
        return self._qf

    def run(self, *args, **kwargs):
        start = datetime.datetime.now()
        # Field ranking
        if 'fields' in kwargs and kwargs['fields'].keys():
            wfields = kwargs['fields']
        else:
            # default
            wfields = {"name": 4}

        print 'Searching %s ...' % kwargs['raw_strings']
        print 'Fields for query %s ...' % wfields

        qm = self.qf.create_mapper(kwargs['query_type'], wfields)
        q4 = qm.create_query(kwargs['raw_strings'])
        resultset = self.es.search(q4)
        ids = [r['id'] for r in resultset]

        print 'Search returned following aggregates %s ...' % ids

        # Get all campaing objects
        mas = MediaAggregate.objects.filter(id__in=set(ids))
        end = datetime.datetime.now()
        elapsed_time = end - start
        _rr = ResearchResult(mediaaggregates=mas,
                             query_runtime_duration=elapsed_time.total_seconds(
                                                            ))
        rr = _rr.save()
        ser = ResearchResultSerializer(rr, many=False)
        _srjson = json.dumps(ser.data, encoding='utf-8')
        print _srjson
        return _srjson
#         _rr = MediaAggregateResearchResult(
#                     aggregates=mas,
#                     query_runtime_duration=elapsed_time.total_seconds(
#                                         ))
#         rr = _rr.save()
#         ser = MediaAggregateResearchResultSerializer(rr, many=False)
#         _srjson = json.dumps(ser.data, encoding='utf-8')
#         print _srjson
#         return _srjson


class MediaAggregateSQLTask(Task):
    # TBD (create the end-point through the controller)
    ignore_errors = True
    _es = None
    _qf = None

    @property
    def es(self):
        if self._es is None:
            self._es = ES("127.0.0.1:9200", default_indices='mediaaggregate')
        return self._es

    @property
    def qf(self):
        if self._qf is None:
            self._qf = querytype_factory()
        return self._qf

    def run(self, *args, **kwargs):
        start = datetime.datetime.now()
        # Field ranking
        if 'query' in kwargs:
            print 'Searching %s ...' % kwargs['query']
            qm = self.qf.create_mapper(kwargs['query_type'], None)
            q4 = qm.create_query(kwargs['query'])
            resultset = self.es.search(q4)
            ids = [r['id'] for r in resultset]
            print 'Search returned following aggregates %s ...' % ids
            # Get all campaing objects
            mas = MediaAggregate.objects.filter(id__in=set(ids))
            end = datetime.datetime.now()
            elapsed_time = end - start
            _rr = ResearchResult(mediaaggregates=mas,
                                 query_runtime_duration=elapsed_time.total_seconds(
                                                                ))
            rr = _rr.save()
            ser = ResearchResultSerializer(rr, many=False)
            _srjson = json.dumps(ser.data, encoding='utf-8')
            print _srjson
            return _srjson
        else:
            rr = ResearchResult()
            ser = ResearchResultSerializer(rr, many=False)
            _srjson = json.dumps(ser.data, encoding='utf-8')
            print _srjson
            return _srjson


class CampaignSQLTask(Task):
    # TBD (create the end-point through the controller)
    ignore_errors = True
    _es = None
    _qf = None

    @property
    def es(self):
        if self._es is None:
            # Note: We still search mediaaggregate by location
            # and then lookup relevant campaigns.
            self._es = ES("127.0.0.1:9200", default_indices='mediaaggregate')
        return self._es

    @property
    def qf(self):
        if self._qf is None:
            self._qf = querytype_factory()
        return self._qf

    def run(self, *args, **kwargs):
        start = datetime.datetime.now()
        # Field ranking
        if 'query' in kwargs:
            print 'Searching %s ...' % kwargs['query']
            qm = self.qf.create_mapper(kwargs['query_type'], None)
            q4 = qm.create_query(kwargs['query'])
            resultset = self.es.search(q4)
            ids = [r['id'] for r in resultset]
            print 'Search returned following aggregates %s ...' % ids
            # Get all campaign objects
            mas = MediaAggregate.objects.filter(id__in=set(ids))
            # Collect the campaigns playing in media aggregate
            mediasources = [ms.inhouse_source for ms in mas]
            plays = Playing.objects.filter(
                            primary_media_source__in=set(mediasources))
            print 'Search returned following plays %d ...' % len(plays)
            camps = [play.playing_content for play in plays]
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
        else:
            rr = ResearchResult()
            ser = ResearchResultSerializer(rr, many=False)
            _srjson = json.dumps(ser.data, encoding='utf-8')
            print _srjson
            return _srjson


class OOHMediaSourceSQLTask(Task):
    # TBD (create the end-point through the controller)
    ignore_errors = True
    _es = None
    _qf = None

    @property
    def es(self):
        if self._es is None:
            self._es = ES("127.0.0.1:9200", default_indices='oohmediasource')
        return self._es

    @property
    def qf(self):
        if self._qf is None:
            self._qf = querytype_factory()
        return self._qf

    def run(self, *args, **kwargs):
        start = datetime.datetime.now()
        # Field ranking
        if 'query' in kwargs:
            print 'Searching %s ...' % kwargs['query']
            qm = self.qf.create_mapper(kwargs['query_type'], None)
            q4 = qm.create_query(kwargs['query'])
            resultset = self.es.search(q4)
            ids = [r['id'] for r in resultset]
            print 'Search returned following sources %s ...' % ids
            # Get all campaing objects
            oohs = OOHMediaSource.objects.filter(id__in=set(ids))
            end = datetime.datetime.now()
            elapsed_time = end - start
            _rr = ResearchResult(ooh=oohs,
                                 query_runtime_duration=elapsed_time.total_seconds(
                                                                ))
            rr = _rr.save()
            ser = ResearchResultSerializer(rr, many=False)
            _srjson = json.dumps(ser.data, encoding='utf-8')
            print _srjson
            return _srjson
        else:
            rr = ResearchResult()
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
