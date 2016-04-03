'''
Created on April 1, 2016

@author: sonu
'''

from __future__ import absolute_import

from celery import shared_task
from celery import Task
from mediacontentapp.models import Campaign
from mediaresearchapp.models import SearchQuery, ResearchResult
from celery import Celery
from mediaresearchapp.serializers import ResearchResultSerializer
from rest_framework.renderers import JSONRenderer


class BasicSearchTask(Task):
    ignore_errors = True

    def run(self, *args, **kwargs):
        res = ResearchResult()
        print 'Searching %s ...' % kwargs['raw_strings']
        camps = Campaign.objects.all()
        for acamp in camps:
            res.campaigns.append(acamp)
        ser = ResearchResultSerializer(res)
        json = JSONRenderer().render(ser.data)
        return json


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
