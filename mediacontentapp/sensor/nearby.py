'''
Created on Jul 2, 2017

@author: sonu
'''
from mediacontentapp.sensor.sensordriverbase import SensorDriverBase


class NearbyDriver(SensorDriverBase):

    @property
    def servicedriver_name(self):
        return "nearby"

    def setup_driver(self):
        pass

    def teardown_driver(self, service_id):
        pass

    def publish_campaign(self, sensor, venue, campaign_data, tracking_data,
                         pub_data):
        pass

    def get_campaign(self):
        pass

    def delete_campaign(self):
        pass

    def get_sensor_details(self):
        pass
