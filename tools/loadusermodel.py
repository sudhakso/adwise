'''
Created on Feb 7, 2016

@author: sonu
'''
import os
import sys
from datetime import datetime, timedelta
import json
import requests
import re
from userapp.models import MediaUser
from mediacontentapp.models import *
from mediacontentapp.serializers import PlayingSerializer
# Basic authentication
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from mediacontentapp.sensor.nikaza import NikazaDriver, NikazaCampaignTemplate
from mediacontentapp.sensor.nearby import NearbyCampaignTemplate, NearbyDriver


def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))


def test_nikaza():
        # Test rendering
    start_dt = datetime.now()
    end_dt = datetime.now() + timedelta(1)
    data = {"campaignName": "name",
            "beginDate": start_dt.strftime("%m/%d/%Y"),
            "endDate": end_dt.strftime("%m/%d/%Y"),
            "numDays": (end_dt-start_dt).days if (end_dt-start_dt).days else 1,
            "venueId": "someid",
            "zoneId": "somezoneid",
            "description": "some desc",
            "url": "https://bing.com"}
    template = NikazaCampaignTemplate()
    body = template.req_body(**data)
    print body

    venue = Venue.objects.get(id='5974ba1f1d41c8119bf4205b')
    sensors = venue.sensors
    campaign = Campaign.objects.get(id='57c062231d41c83e549e8af9')
    ct = CampaignTracking.objects.get(campaign=campaign)
    pub_data = {"id": "5974bb1f1d41c8119bf4205d",
                "source_type": "sensor",
                "start_date": "2017-07-23T18:37:21.766000Z",
                "end_date": "2017-07-27T18:37:21.766000Z",
                "creation_date": "2017-07-23T08:40:09.565000Z",
                "deletion_date": "",
                "playing_vendor_attributes": {"status": "success", "message": "Campaign created successfully", "statusCode": "200", "campaignId": "5974bb22cb61eb1059e7c106"}}

    drv = NikazaDriver(endpoint="http://nikaza.io", apikey="somekey", username="somename", password="somepasswd")
    for sensor in sensors:
        drv.publish_campaign(sensor, venue, campaign, ct, json.dumps(pub_data))


def test_nearby():
        # Test rendering
    start_dt = datetime.now()
    end_dt = datetime.now() + timedelta(1)
    sensor_1 = {"id":"someid", "mac_address":"someaddr"}
    venue_1 = {"venue_name": "iimb_phase-1"}
#     sensor_2 = {"id":"someid", "macAddr":"someaddr"}
    data = {"campaignName": "somename",
            "beginDate": start_dt.strftime("%m/%d/%Y"),
            "endDate": end_dt.strftime("%m/%d/%Y"),
            "url": "https://bing.com",
            "sensors": [sensor_1],
            "venue": venue_1}
    template = NearbyCampaignTemplate()
    body = template.req_body(**data)
    print body

    venue = Venue.objects.get(id='596a26911d41c8213e515219')
    sensors = venue.sensors
    campaign = Campaign.objects.get(id='57c062231d41c83e549e8af9')
    ct = CampaignTracking.objects.get(campaign=campaign)
    pub_data = {"start_date" : "2017-07-15T18:37:21.766000Z",
                "end_date" : "2017-09-25T18:37:21.766000Z"}

#     endpoint = amqp://mrafhtxb:HuPwIQDIAxoC3HQTuyHluZPULpR6uReS@white-mynah-bird.rmq.cloudamqp.com/mrafhtxb
#     exchange_name = nearby-exchange
#     username = mrafhtxb
#     vhost = mrafhtxb

    drv = NearbyDriver(endpoint="amqp://mrafhtxb:HuPwIQDIAxoC3HQTuyHluZPULpR6uReS@white-mynah-bird.rmq.cloudamqp.com/mrafhtxb",
                       exchange_name="",
                       username="mrafhtxb", vhost="mrafhtxb")
    for sensor in sensors:
        drv.publish_campaign(sensor, venue, campaign, ct, json.dumps(pub_data))

# Re-creates dJango AUTH users from MediaUser entries.
# dJango Auth model differs in implementation by Mongo DB version
# and may not be directly portable.

if __name__ == '__main__':
    test_nikaza()
#     test_nearby()

    all_users = MediaUser.objects.all()
    print "Found %d users..." % len(all_users)
    for user in all_users:
        print 'Loading user [%s]' % user.username
        try:
            user = User.objects.get(username=user.username)
            if user:
                print 'User already exists, skipping...'
                continue
        except ObjectDoesNotExist:
            print "Creating user with username: %s, email: %s, passowrd: %s" % (user.username, user.email, user.password)
            # User doesn't exist.
#             usr = User.objects.create(username=user.username,
#                                       email=user.email)
#             usr.set_password(usr.password)
#             usr.save()
            print 'Finished adding user %s...' % user.username

