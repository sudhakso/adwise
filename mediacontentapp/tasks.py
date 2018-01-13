'''
Created on April 1, 2016

@author: sonu
'''

from __future__ import absolute_import

import datetime
from json import loads
import json

from celery import Celery
from celery import Task
from celery import shared_task
from django.core import serializers
from mongoengine.errors import DoesNotExist
from rest_framework.renderers import JSONRenderer

from mediacontentapp.controller import IndexingService, URLRedirectService
from mediacontentapp.models import Campaign, OfferExtension, CampaignTracking, \
 Sensor
from mediacontentapp.sensormanager import SensorManager
from mediacontentapp.serializers import CampaignSerializer, \
    CampaignIndexSerializer
from mediaresearchapp.models import SearchQuery, ResearchResult
from mediaresearchapp.serializers import ResearchResultSerializer


# Initialize the service
# indexing_service = IndexingService()
#sensor_manager = SensorManager()
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


class OOHyticsIndexingTask(Task):
    ignore_errors = True
    _es = None

    @property
    def es(self):
        if self._es is None:
            self._es = IndexingService()
        return self._es

    # instancename=, object=
    def run(self, *args, **kwargs):
        print 'Creating index for OOH instance : %s ...' % (
                                kwargs['instancename'])
        if 'many' in kwargs and kwargs['many'] == True:
            data = {'root': kwargs['oohytics']}
        else:
            data = kwargs['oohytics']
        print data
        try:
            self.es.connection.index(
                                data,
                                "oohmediasource",
                                "external")
        except Exception as e:
            print "Failed creating index for ooh  : %s" % (
                                    kwargs['instancename'])
            print "Exception : %s" % str(e)


class CampaignPublishingTask(Task):
    ignore_errors = True
    _sm = None

    @property
    def sm(self):
        if self._sm is None:
            self._sm = SensorManager()
        return self._sm

    def run(self, *args, **kwargs):
        start = datetime.datetime.now()
        # 1 - Check if campaign is enabled for URL
        print 'Checking if campaign publish is required for : %s ...' % (
                                kwargs['pub_content_id'])
        # get the campaign tracking object
        try:
            c = Campaign.objects.get(id=kwargs['pub_content_id'])
            ct = CampaignTracking.objects.get(campaign=c)
            s = Sensor.objects.get(id=kwargs['pub_source_id'])
        except DoesNotExist as e:
            print 'Warning: Enable tracking for the campaign - %s ...' % (
                                    kwargs['pub_content_id'])
            print 'Warning: Campaign not published.'
            print str(e)
            return
        # 2- Check the name of the sensor where this is played
        # 3 - Check if we have the driver that can handle the
        # publishing of the campaign
        try:
            pd = kwargs['pub_detail'] if 'pub_detail' in kwargs.keys() else None
            print 'Extracting publishing details for campaign : %s ...' % (
                                    kwargs['pub_content_id'])
            driver = self.sm.sensor_factory.driver(s.vendor)
            if driver:
                print 'Loaded vendor %s driver to publish content' % s.vendor
                response = driver.publish_campaign(s, s.venue, c, ct, pd)
                # {"campaignId":"59743b49cb61eb1059e7c101",
                # "message":"Campaign created successfully",
                # "status":"success",
                # "statusCode":"200"}
                print 'Published campaign. Response : %s' % response
                return response
            else:
                print 'Loading vendor %s driver encountered error' % s.vendor
        except Exception as e:
            print "Failed publishing campaign : %s" % (
                                    kwargs['pub_content_id'])
            print "Exception : %s" % str(e)


class CampaignControlTask(Task):
    ignore_errors = True
    _sm = None

    @property
    def sm(self):
        if self._sm is None:
            self._sm = SensorManager()
        return self._sm

    def run(self, *args, **kwargs):
        start = datetime.datetime.now()
        # 1 - Check if campaign is enabled for URL
        print 'Checking if campaign update is required for : %s ...' % (
                                kwargs['pub_content_id'])
        # get the campaign tracking object
        try:
            c = Campaign.objects.get(id=kwargs['pub_content_id'])
            ct = CampaignTracking.objects.get(campaign=c)
            s = Sensor.objects.get(id=kwargs['pub_source_id'])
        except DoesNotExist as e:
            print 'Warning: Enable tracking for the campaign - %s ...' % (
                                    kwargs['pub_content_id'])
            print 'Warning: Campaign not updated.'
            print str(e)
            return
        # 2- Check the name of the sensor where this is played
        # 3 - Check if we have the driver that can handle the
        # publishing of the campaign
        try:
            pd = kwargs['pub_detail'] if 'pub_detail' in kwargs.keys() else None
            update = kwargs['update']
            driver = self.sm.sensor_factory.driver(s.vendor)
            if driver:
                print 'Loaded vendor %s driver to control content' % s.vendor
                response = driver.control_campaign(s, s.venue, c, ct, pd, update)
                print 'Updated campaign. Response : %s' % response
                return response
            else:
                print 'Loading vendor %s driver encountered error' % s.vendor
        except Exception as e:
            print "Failed publishing campaign : %s" % (
                                    kwargs['pub_content_id'])
            print "Exception : %s" % str(e)


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


class MediaAggregateIndexingTask(Task):
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
        print 'Creating index for mediaaggregate : %s ...' % (
                                kwargs['instancename'])
        if 'many' in kwargs and kwargs['many'] == True:
            data = {'root': kwargs['mediaaggregate']}
        else:
            data = kwargs['mediaaggregate']
        print data
        try:
            self.es.connection.index(
                                data,
                                "mediaaggregate",
                                "external")
        except Exception as e:
            print "Failed creating index for mediaaggregate : %s" % (
                                    kwargs['instancename'])
            print "Exception : %s" % str(e)


class OfferIndexingTask(Task):
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
        print 'Creating index for offer : %s ...' % (
                                kwargs['instancename'])
        if 'many' in kwargs and kwargs['many'] == True:
            data = {'root': kwargs['offer']}
        else:
            data = kwargs['offer']
        print data
        try:
            self.es.connection.index(
                                data,
                                "offer",
                                "external")
        except Exception as e:
            print "Failed creating index for offer : %s" % (
                                    kwargs['instancename'])
            print "Exception : %s" % str(e)


class AdIndexingTask(Task):
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
        print 'Creating index for Ad : %s ...' % (
                                kwargs['instancename'])
        if 'many' in kwargs and kwargs['many'] == True:
            data = {'root': kwargs['ad']}
        else:
            data = kwargs['ad']
        print data
        try:
            self.es.connection.index(
                                data,
                                "ad",
                                "external")
        except Exception as e:
            print "Failed creating index for ad : %s" % (
                                    kwargs['instancename'])
            print "Exception : %s" % str(e)


class OOHMediaSourceIndexingTask(Task):
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
        print 'Creating index for oohmediasource : %s ...' % (
                                kwargs['instancename'])
        if 'many' in kwargs and kwargs['many'] == True:
            data = {'root': kwargs['oohmediasource']}
        else:
            data = kwargs['oohmediasource']
        print data
        try:
            self.es.connection.index(
                                data,
                                "oohmediasource",
                                "external")
        except Exception as e:
            print "Failed creating index for oohmediasource : %s" % (
                                    kwargs['instancename'])
            print "Exception : %s" % str(e)


class CampaignRedirectRuleSetupTask(Task):
    ignore_errors = True
    _rulebroker = None

    @property
    def rulebroker(self):
        if self._rulebroker is None:
            self._rulebroker = URLRedirectService()
        return self._rulebroker

    # instancename=, object=
    def run(self, *args, **kwargs):
        start = datetime.datetime.now()
        print 'Setting up 302 redirect rules for campaign tracking Id : %s ...' % (
                                kwargs['instancename'])
        data = loads(kwargs['campaigntracker'])
        print data
        try:
            tracks = CampaignTracking.objects.filter(id=data['id'])
            # Find the campaign id
            if len(tracks):
                source = tracks[0].campaign.id
                target = tracks[0].campaign.home_url
                # Add the URLs to redirect server
                res = self.rulebroker.addRule(source, target)
                if res:
                    print "Successfully created redirect rule for campaign : %s" % (
                                        source)
                    print "Applying rule to the server..."
                    self.rulebroker.SIGUSR1()
                    return "SUCCESS"
        except Exception as e:
            print "Failed creating redirect rule for campaign tracking: %s" % (
                                    kwargs['instancename'])
            print "Exception : %s" % str(e)
            return "FAILED"

@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param
