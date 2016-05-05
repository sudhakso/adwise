'''
Created on Dec 25, 2015

@author: sonu
'''
import json
from mediacontentapp.models import OOHMediaSource,\
    Campaign, OfferExtension, ImageAd
from mongoengine import signals
from mediacontentapp.tasks import CampaignIndexingTask, OfferIndexingTask,\
    AdIndexingTask
from mediacontentapp.serializers import CampaignIndexSerializer,\
    ImageAdIndexSerializer, OfferIndexSerializer
from mediacontentapp.controller import IndexingService


def mediasource_handler(sender, document, created):
    print "Placeholder for source analytics"


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

# Register all model handlers
signals.post_save.connect(mediasource_handler, OOHMediaSource)
signals.post_save.connect(index_campaign, Campaign)
signals.post_save.connect(index_offer, OfferExtension)
signals.post_save.connect(index_ad, ImageAd)
