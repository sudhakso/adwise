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
        return _str


class NikazaDriver(SensorDriverBase):

    # driver = mediacontentapp.sensor.nikaza
    # endpoint = https://nikaza.io/customer_dashboard
    # apikey = b2a7f8f3-ef34-4e17-a2f7-db102523e5dc
    # username = series5
    # password = series5076

    def __init__(self, endpoint, apikey, username, password):
        self.headers = {"Content-type": "application/json",
                        "APIKey": apikey,
                        "User-Agent": "series5"
                        }
        self._endpoint = endpoint
        # APIs supported
        self.CREATE_CAMPAIGN = "create_campaign"
        self.GET_BEACON_PLACEMENT = "get_beacon_placement"
        self.UPDATE_CAMPAIGN_STATUS = 'update_campaign_status'
        self.UPDATE_CAMPAIGN = 'update_campaign'

        # Campaign template
        self._template = NikazaCampaignTemplate()

    @property
    def servicedriver_name(self):
        return "nikaza"

    def setup_driver(self):
        pass

    def teardown_driver(self, service_id):
        pass

    def get_venue_details(self, venuename):
        data = {"venueName": venuename}
        datastr = str(data)
        api_endpoint = self._endpoint + self.GET_BEACON_PLACEMENT
        print "HTTP header : %s" % (self.headers)
        datastr = datastr.replace("\'","\"").replace("u\"","\"").replace("u\'","\'")
        print "Get sensor details using Nikaza url:%s data:%s" % (
                                                        api_endpoint, datastr)
        response = requests.post(url=api_endpoint,
                                 headers=self.headers,
                                 data=datastr)
        venuedetail = json.loads(response.text)
        # If successful
        venueId = ""
        numSensors = 0
        sensors = []
        if venuedetail['status'] == 'success':
            venues = venuedetail['venues']
            for venue in venues:
                if venue['venueName'] == venuename:
                    venueId = venue['venueId']
                    numSensors = venue['noOfDevices']
                    break
            if numSensors:
                zones = venuedetail['zones']
                for sensor in zones:
                    sensorname = sensor['zone']
                    sensorId = sensor['zoneId']
                    sensors.append((sensorname, sensorId))
        return (venueId, sensors)

    def publish_campaign(self,
                         sensor,
                         venue,
                         campaign,
                         tracking_data,
                         pub_data):
        from dateutil.parser import parse
        playing_data = json.loads(pub_data)
        start_dt = parse(playing_data['start_date'])
        end_dt = parse(playing_data['end_date'])
        # venueId and ZoneId must be filled in the driver.
        # This need not be auto-filled and needs to be removed
        # from the model.
        venueId, sensors = self.get_venue_details(venue.venue_name)
        if venueId is None:
            rcvars = {"message": "No matching venue registered. VenueId returned is None for %s " % (venue.name),
                      "code": "500"}
            rcvarstr = json.dumps(rcvars)
            print "Matching Venue not found : %s" % (rcvarstr)
            return rcvarstr

        if not sensors:
            rcvars = {"message": "No sensors were registered for venue %s " % (venue.name),
                      "code": "500"}
            rcvarstr = json.dumps(rcvars)
            print "Empty sensors : %s" % (rcvarstr)

        # Grab the sensor to program by name.
        sensorId = None
        for zone in sensors:
            name = zone[0]
            if name.lower() == sensor.name.lower():
                sensorId = zone[1]
                break
        if sensorId is None:
            rcvars = {"message": "No valid sensors were found by name %s under venue %s " % (
                                                                                sensor.name, venue.name),
                      "code": "500"}
            rcvarstr = json.dumps(rcvars)
            print "Sensor not found : %s" % (rcvarstr)

        data = {"campaignName": campaign.name,
                "beginDate": start_dt.strftime("%m/%d/%Y"),
                "endDate": end_dt.strftime("%m/%d/%Y"),
                "numDays": (end_dt-start_dt).days if (end_dt-start_dt).days else 1,
                "venueId": venueId,
                "zoneId": sensorId,
                "description": campaign.description,
                "url": tracking_data.short_url}

        api_endpoint = self._endpoint + self.CREATE_CAMPAIGN
        body = self._template.req_body(**data)
        print "HTTP header : %s" % (self.headers)
        print "Launching campaign using Nikaza url:%s data:%s" % (
                                                        api_endpoint, body)
        response = requests.post(url=api_endpoint,
                                 headers=self.headers,
                                 data=body)
        return response.text

    def control_campaign(self, sensor, venue, campaign_data, tracking_data,
                         pub_data, update):
        playing_data = json.loads(pub_data)
        control = update
        # campaigns:[]
        # campaignStatus: "run"

        # check the playing data for vendor campaign id
        if playing_data['playing_vendor_attributes']:
            vendor_attrib = playing_data['playing_vendor_attributes']
            nikaza_campaign_id = vendor_attrib['campaignId']
            print "Nikaza driver attributes for the campaign %s" % vendor_attrib
            print "Updating campaign status to %s for %s" % (
                                            update, nikaza_campaign_id)
            body = {
                # remove unicode prefixes, Nikaza doesnt understand them
                "campaigns": [nikaza_campaign_id],
                "campaignStatus": "run" if control == 'resume' else "pause"
            }
            body_str = json.dumps(body).replace("u\"","\"").replace("u\'","\'")
            api_endpoint = self._endpoint + self.UPDATE_CAMPAIGN_STATUS
            print "HTTP header : %s" % (self.headers)
            print "Controlling campaign using Nikaza url:%s data:%s" % (
                                                            api_endpoint, body_str)
            response = requests.post(url=api_endpoint,
                                     headers=self.headers,
                                     data=body_str)
            return response.text

    def get_campaign(self):
        pass

    def delete_campaign(self):
        pass

    def update_campaign(self):
        pass

    def get_sensor_details(self, venue_id):
        pass
