'''
Created on Dec 30, 2015

@author: sonu
'''

from __future__ import absolute_import

from celery import shared_task
from mediacontentapp.models import ImageAd

import datetime
import json
from celery import Task
from rest_framework.renderers import JSONRenderer
from userapp.controller import IndexingService


@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param


@shared_task
def fetch_ad(user, geopoint):
    print 'Fetching ad for the user {%s} at location (%s)' % (
                                user['username'], geopoint['point'])
    # TBD: Actual work pending.
    # Step1 : Search for the Ad by location
    # Step2 : Deliver it via a driver (django-instapush)
    # TBD: Testing in progress
    ads = ImageAd.objects(
                ad_location_tag__near=geopoint['point'])
    print ads
    pass


class UserIndexingTask(Task):
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
        print 'Creating index for User : %s ...' % (
                                kwargs['instancename'])
        if 'many' in kwargs and kwargs['many'] == True:
            data = {'root': kwargs['mediauser']}
        else:
            data = kwargs['mediauser']
        print data
        try:
            self.es.connection.index(
                                data,
                                "mediauser",
                                "external")
        except Exception as e:
            print "Failed creating index for mediauser : %s" % (
                                    kwargs['instancename'])
            print "Exception : %s" % str(e)

