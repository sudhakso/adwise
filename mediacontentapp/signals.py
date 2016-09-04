'''
Created on Dec 25, 2015

@author: sonu
'''
import json
from mediacontentapp.models import OOHAnalyticalAttributes,\
    Campaign, OfferExtension, ImageAd, MediaAggregate
from mongoengine import signals
from mediacontentapp.tasks import CampaignIndexingTask, OfferIndexingTask,\
    AdIndexingTask, OOHyticsIndexingTask, MediaAggregateIndexingTask
from mediacontentapp.serializers import CampaignIndexSerializer,\
    ImageAdIndexSerializer, OfferIndexSerializer,\
    MediaAggregateIndexSerializer
from mediacontentapp.controller import IndexingService
from mediacontentapp.sourceserializers import OOHAnalyticalAttributesSerializer


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

# Register all model handlers
signals.post_save.connect(index_oohanalytics, OOHAnalyticalAttributes)
signals.post_save.connect(index_campaign, Campaign)
signals.post_save.connect(index_offer, OfferExtension)
signals.post_save.connect(index_ad, ImageAd)
signals.post_save.connect(index_mediaaggregate, MediaAggregate)
