'''
Created on April 1, 2016

@author: sonu
'''

from __future__ import absolute_import

import datetime
import json
from celery import shared_task
from celery import Task
from mediacontentapp.models import Campaign, OfferExtension
from mediaresearchapp.models import SearchQuery, ResearchResult
from celery import Celery
from mediaresearchapp.serializers import ResearchResultSerializer
from rest_framework.renderers import JSONRenderer
from django.core import serializers
from mediacontentapp.serializers import CampaignSerializer,\
    CampaignIndexSerializer
from mediacontentapp.controller import IndexingService

# Initialize the service
# indexing_service = IndexingService()


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


class OfferIndexingTask(Task):
    ignore_errors = True

    # instancename=, object=
    def run(self, *args, **kwargs):
        start = datetime.datetime.now()
        print 'Creating index for offer : %s ...' % (
                                kwargs['instancename'])
        obj = kwargs['offer']
        if isinstance(obj, OfferExtension):
            # Create index
            pass


class CampaignIndexingTask(Task):
    ignore_errors = True
    _es = None

    @property
    def es(self):
        if self._es is None:
            self._es = IndexingService()
        return self._es

    # instancename=, object=
    def run(self, *args, **kwargs):
        start = datetime.datetime.now()
        print 'Creating index for campaign : %s ...' % (
                                kwargs['instancename'])
        if 'many' in kwargs and kwargs['many'] == True:
            data = {'root': kwargs['campaign']}
        else:
            data = kwargs['campaign']
        print data
        try:
            self.es.connection.index(
                                data,
                                "campaign",
                                "external")
        except Exception as e:
            print "Failed creating index for campaign : %s" % (
                                    kwargs['instancename'])
            print "Exception : %s" % str(e)


@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param
