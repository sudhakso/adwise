'''
Created on Jul 2, 2017

@author: sonu
'''
from jinja2 import Template
import json
import pika
from django.conf import settings
from datetime import date, datetime
from mediacontentapp.sensor.sensordriverbase import SensorDriverBase


class NearbyCampaignTemplate():

    def __init__(self):
        self.j2_template = Template(
                            open('%s%s' % (settings.MEDIAAPP_DIR,
                                           'templates/nearby_request_campaign.j2'),
                                 'r').read())

    def req_body(self, **kwargs):
        # Create the serializer
        _str = str(self.j2_template.render(**kwargs)).encode('utf-8')
        return _str


class NearbyDriver(SensorDriverBase):

#     endpoint = amqp://mrafhtxb:HuPwIQDIAxoC3HQTuyHluZPULpR6uReS@white-mynah-bird.rmq.cloudamqp.com/mrafhtxb
#     exchange_name = nearby-exchange
#     username = mrafhtxb
#     vhost = mrafhtxb

    def __init__(self, endpoint, exchange_name, username, vhost):
        self._endpoint = endpoint
        self.username = username
        self.vhost = vhost
        # Campaign template
        self._template = NearbyCampaignTemplate()


    @property
    def servicedriver_name(self):
        return "nearby"

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
        # get the routing key
        routing_key = venue.venue_name
        routing_response_key = venue.venue_name + "_response"

        data = {"campaignName": campaign.name,
                "beginDate": start_dt.strftime("%m/%d/%Y"),
                "endDate": end_dt.strftime("%m/%d/%Y"),
                "url": tracking_data.short_url,
                "sensors": [sensor],
                "ackQueueName": routing_response_key,
                "venue": venue}

        body = self._template.req_body(**data)
        print "Launching campaign using Nearby routing_key: %s url:%s data:%s" % (
                                                        routing_key,
                                                        self._endpoint,
                                                        body)
        params = pika.URLParameters(self._endpoint)
        params.socket_timeout = 5
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        # send a message
        channel.basic_publish(exchange='', routing_key=routing_key,
                              body=body)
        print " [x] Message sent to consumer"
        connection.close()
        return

    def get_campaign(self):
        pass

    def delete_campaign(self):
        pass

    def get_sensor_details(self, venue_id):
        pass
