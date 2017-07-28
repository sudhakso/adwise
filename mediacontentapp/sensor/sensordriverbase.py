'''
Created on Jul 2, 2017

@author: sonu
'''

from abc import ABCMeta, abstractmethod


class SensorDriverBase(object):
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def servicedriver_name(self):
        return None

    @abstractmethod
    def setup_driver(self):
        pass

    @abstractmethod
    def teardown_driver(self, service_id):
        pass

    @abstractmethod
    def publish_campaign(self, sensor, venue, campaign_data, tracking_data,
                         pub_data):
        pass

    @abstractmethod
    def control_campaign(self, sensor, venue, campaign_data, tracking_data,
                         pub_data, update):
        pass

    @abstractmethod
    def get_campaign(self):
        pass

    @abstractmethod
    def delete_campaign(self):
        pass

    @abstractmethod
    def get_sensor_details(self):
        pass


class NoopDriver(SensorDriverBase):

    @property
    def servicedriver_name(self):
        return "noop"

    def setup_driver(self):
        pass

    def teardown_driver(self, service_id):
        pass

    def publish_campaign(self, sensor, campaign_data, tracking_data):
        pass

    def get_campaign(self):
        pass

    def delete_campaign(self):
        pass

    def get_sensor_details(self):
        pass
