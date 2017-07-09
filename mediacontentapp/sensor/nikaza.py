'''
Created on Jul 2, 2017

@author: sonu
'''
import httplib
from jinja2 import Template
import requests
import json
from django.conf import settings
from mediacontentapp.sensor.sensordriverbase import SensorDriverBase
from datetime import date, datetime


class NikazaCampaignTemplate():

    def __init__(self):
        self.j2_template = Template(
                            open('%s%s' % (settings.MEDIAAPP_DIR,
                                           'templates/nikaza_request_campaign.j2'),
                                 'r').read())

    def req_body(self, **kwargs):
        # Create the serializer
        _str = str(self.j2_template.render(**kwargs)).encode('utf-8')
#         _str = _str.replace("\'","\"").replace("u\"","\"").replace("u\'","\'")
        print _str
        _data = json.loads(_str)
        print _data
        return _data


class NikazaDriver(SensorDriverBase):

    # driver = mediacontentapp.sensor.nikaza
    # endpoint = https://nikaza.io/customer_dashboard
    # apikey = b2a7f8f3-ef34-4e17-a2f7-db102523e5dc
    # username = series5
    # password = series5076

    def __init__(self, endpoint, apikey, username, password):
        self.headers = {"Content-type": "application/json",
                        "APIKey": apikey,
                        "Accept": "text/plain",
                        }
        self._endpoint = endpoint
        # APIs supported
        self.CREATE_CAMPAIGN = "create_campaign"
        self.GET_BEACON_PLACEMENT = "get_beacon_placement"
        self.UPDATE_CAMPAIGN_STATUS = 'update_campaign_status'
        self.UPDATE_CAMPAIGN = 'update_campaign'
        # Constant zoneId
        self.ZONE_ID = "series5-001"

        # Campaign template
        self._template = NikazaCampaignTemplate()

    @property
    def servicedriver_name(self):
        return "nikaza"

    def setup_driver(self):
        pass

    def teardown_driver(self, service_id):
        pass

    def publish_campaign(self,
                         sensor,
                         venue,
                         campaign,
                         tracking_data,
                         pub_data):
        playing_data = json.loads(pub_data)
        start_dt = datetime.strptime(playing_data['start_date'],
                                     "%Y-%m-%dT%H:%M:%S.%fZ")
        end_dt = datetime.strptime(playing_data['end_date'],
                                   "%Y-%m-%dT%H:%M:%S.%fZ")
        data = {"campaignName": campaign.name,
                "beginDate": start_dt.strftime("%m/%d/%Y"),
                "endDate": end_dt.strftime("%m/%d/%Y"),
                "venueId": venue.venue_name if venue is not None else 'default',
                "zoneId": self.ZONE_ID,
                "description": campaign.description,
                "url": tracking_data.short_url}

        api_endpoint = self._endpoint + self.CREATE_CAMPAIGN
        body = self._template.req_body(**data)
        print "Launching campaign using Nikaza url:%s data:%s" % (
                                                        api_endpoint, body)
        response = requests.post(url=api_endpoint,
                                 headers=self.headers,
                                 data=body)
#       print "Campaign result response:%s" % (response.text)
        return response.text

    def get_campaign(self):
        pass

    def delete_campaign(self):
        pass

    def get_sensor_details(self, venue_id):
        pass
