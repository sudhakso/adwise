'''
Created on April 1, 2016

@author: sonu
'''

from __future__ import absolute_import

import datetime
import json
from celery import shared_task
from celery import Task
from mediacontentapp.models import Campaign
from mediaresearchapp.models import SearchQuery, ResearchResult
from celery import Celery
from mediaresearchapp.serializers import ResearchResultSerializer
from rest_framework.renderers import JSONRenderer
from django.core import serializers
from mediacontentapp.serializers import CampaignSerializer


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
