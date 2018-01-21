'''
Created on Dec 25, 2015

@author: sonu
'''
import json

from mongoengine import signals

from mediacontentapp.controller import IndexingService
from mediacontentapp.models import OOHAnalyticalAttributes, \
    Campaign, OfferExtension, ImageAd, MediaAggregate, OOHMediaSource, \
    Playing, CampaignTracking
from mediacontentapp.serializers import CampaignIndexSerializer, \
    ImageAdIndexSerializer, OfferIndexSerializer, \
    MediaAggregateIndexSerializer, CampaignTrackingSerializer
from mediacontentapp.sourceserializers import OOHAnalyticalAttributesSerializer, \
 OOHMediaSourceIndexSerializer
from mediacontentapp.tasks import CampaignIndexingTask, OfferIndexingTask, \
    AdIndexingTask, OOHyticsIndexingTask, MediaAggregateIndexingTask, \
    OOHMediaSourceIndexingTask, CampaignRedirectRuleSetupTask


def index_oohanalytics(sender, document, created):
    print "Placeholder for source analytics"
    # Campaign Index task
    if created:
        oohytics = OOHAnalyticalAttributesSerializer(document, many=False)
        task = OOHyticsIndexingTask()
        rc = task.delay(args=[],
                        instancename=str(document.source_ref.id),
                        oohytics=json.dumps(oohytics.data),
                        ignore_failures=True)
        if rc.state == "SUCCESS":
            print "index_oohanalytics task status: OK."
        else:
            print "index_oohanalytics task status: Not OK."
    else:
            print "index_oohanalytics: task status: Unchanged OK."


def index_campaign(sender, document, created):
    print "Placeholder for indexing campaigns"
    # Campaign Index task
    if created:
        cs = CampaignIndexSerializer(document, many=False)
        task = CampaignIndexingTask()
        rc = task.delay(args=[],
                        instancename=str(document.id),
                        campaign=json.dumps(cs.data),
                        ignore_failures=True)
        if rc.state == "SUCCESS":
            print "index_campaign task status: OK."
        else:
            print "index_campaign task status: Not OK."
    else:
            print "index_campaign: task status: Unchanged OK."


def index_offer(sender, document, created):
    print "Placeholder for indexing offers"
    # Offer Index task
    if created:
        of = OfferIndexSerializer(document, many=False)
        task = OfferIndexingTask()
        rc = task.delay(args=[],
                        instancename=str(document.id),
                        offer=json.dumps(of.data),
                        ignore_failures=True)
        if rc.state == "SUCCESS":
            print "index_offer task status: OK."
        else:
            print "index_offer task status: Not OK."
    else:
            print "index_offer: task status: Unchanged OK."


def index_ad(sender, document, created):
    print "Placeholder for indexing ads"
    # Ad Index task
    if created:
        ad = ImageAdIndexSerializer(document, many=False)
        task = AdIndexingTask()
        rc = task.delay(args=[],
                        instancename=str(document.id),
                        ad=json.dumps(ad.data),
                        ignore_failures=True)
        if rc.state == "SUCCESS":
            print "index_ad task status: OK."
        else:
            print "index_ad task status: Not OK."
    else:
            print "index_ad: task status: Unchanged OK."


def index_mediaaggregate(sender, document, created):
    print "Placeholder for indexing amenity/mediaaggregate"
    # MediaAggregate Index task
    if created:
        ma = MediaAggregateIndexSerializer(document, many=False)
        task = MediaAggregateIndexingTask()
        rc = task.delay(args=[],
                        instancename=str(document.id),
                        mediaaggregate=json.dumps(ma.data),
                        ignore_failures=False)
        if rc.state == "SUCCESS":
            print "index_mediaaggregate task status: OK."
        else:
            print "index_mediaaggregate task status: Not OK."
    else:
            print "index_mediaaggregate: task status: Unchanged OK."


def index_oohmediasource(sender, document, created):
    print "Placeholder for indexing amenity/oohmediasource"
    # OOHMediaSource Index task
    if created:
        ooh = OOHMediaSourceIndexSerializer(document, many=False)
        task = OOHMediaSourceIndexingTask()
        rc = task.delay(args=[],
                        instancename=str(document.id),
                        oohmediasource=json.dumps(ooh.data),
                        ignore_failures=False)
        if rc.state == "SUCCESS":
            print "index_oohmediasource task status: OK."
        else:
            print "index_oohmediasource task status: Not OK."
    else:
            print "index_oohmediasource: task status: Unchanged OK."


def set_302redirect_rules(sender, document, created):
    print "Placeholder for setting 302 redirect rules in nginx"
    # 302 redirect
    ctser = CampaignTrackingSerializer(document, many=False)
    task = CampaignRedirectRuleSetupTask()
    rc = task.delay(args=[],
                    instancename=str(document.id),
                    campaigntracker=json.dumps(ctser.data),
                    ignore_failures=False)
    if rc.state == "SUCCESS":
        print "redirect rule for %s task status: OK." % str(document.id)
    else:
        print "redirect rule for %s task status: Not OK." % str(document.id)


# Register all model handlers
signals.post_save.connect(index_oohanalytics, OOHAnalyticalAttributes)
signals.post_save.connect(index_campaign, Campaign)
signals.post_save.connect(index_offer, OfferExtension)
signals.post_save.connect(index_ad, ImageAd)
signals.post_save.connect(index_mediaaggregate, MediaAggregate)
signals.post_save.connect(index_oohmediasource, OOHMediaSource)
signals.post_save.connect(set_302redirect_rules, CampaignTracking)

