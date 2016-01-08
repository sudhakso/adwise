'''
Created on Nov 24, 2015

@author: sonu
'''
from userapp.models import Location, Meter
import json


class LocationDriver(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def handle_service_request(self, key, service_data):
        # Load service data into Json
        req_data = json.loads(service_data)
        if 'point' in req_data:
            loc = Location.objects.create(
                            service_key=key,
                            point=req_data['point'])


class MeteringDriver(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    def handle_service_request(self, key, service_data):
        pass


class CloudmessagingDriver(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    def handle_service_request(self, key, service_data):
        pass
