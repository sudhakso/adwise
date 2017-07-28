'''
Created on Jul 2, 2017

@author: sonu
'''

from mediacontentapp.sensor.sensordriverbase import SensorDriverBase


class GoogleDriver(SensorDriverBase):

    def __init__(self, endpoint, apikey, clientid):
        pass

    @property
    def servicedriver_name(self):
        return "google"

    def setup_driver(self):
        pass

    def teardown_driver(self, service_id):
        pass

    def publish_campaign(self, sensor, venue, campaign_data, tracking_data,
                         pub_data):
        pass

    def control_campaign(self, sensor, venue, campaign_data, tracking_data,
                        pub_data, update):
        pass

    def get_campaign(self):
        pass

    def delete_campaign(self):
        pass

    def get_sensor_details(self):
        pass
