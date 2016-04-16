'''
Created on Dec 25, 2015

@author: sonu
'''
import json
from mediacontentapp.models import OOHMediaSource,\
    Campaign, OfferExtension
from mongoengine import signals
from mediacontentapp.tasks import CampaignIndexingTask
from mediacontentapp.serializers import CampaignIndexSerializer
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


# Register all model handlers
signals.post_save.connect(mediasource_handler, OOHMediaSource)
signals.post_save.connect(index_campaign, Campaign)
signals.post_save.connect(index_offer, OfferExtension)
