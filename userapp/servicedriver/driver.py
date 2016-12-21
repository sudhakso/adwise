'''
Created on Nov 24, 2015

@author: sonu
'''
from userapp.models import Location, Meter,\
 Offer, Notification, Event, Cart
from userapp.serializers import LocationSerializer,\
 MeterSerializer, OfferSerializer, NotificationSerializer,\
 EventSerializer, CartSerializer

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
        locser = LocationSerializer(data=req_data)
        if locser.is_valid(raise_exception=True):
            locser.save(service_key=key)

    def handle_service_get_request(self, key, service_data, query_param):
        # Get service data
        # (Note:Sonu) TBD filter query parameters
        locs = Location.objects.filter(service_key=str(key))
        ser = LocationSerializer(locs, many=True)
        return ser


class MeteringDriver(object):
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
        metser = MeterSerializer(data=req_data)
        if metser.is_valid(raise_exception=True):
            metser.save(service_key=key)

    def handle_service_get_request(self, key, service_data, query_param):
        # Get service data
        # (Note:Sonu) TBD filter query parameters
        meters = Meter.objects.filter(service_key=str(key))
        ser = MeterSerializer(meters, many=True)
        return ser


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


class NotificationDriver(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def handle_service_request(self, key, service_data):
        # Load service data into Json
        data = json.loads(service_data)
        notser = NotificationSerializer(data=data)
        if notser.is_valid(raise_exception=True):
            notser.save(service_key=str(key))

    def handle_service_get_request(self, key, query_param):
        # Get service data
        # (Note:Sonu) TBD filter query parameters
        notifs = Notification.objects.filter(service_key=str(key))
        ser = NotificationSerializer(notifs, many=True)
        return ser


class CartDriver(object):
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
        cartser = CartSerializer(data=req_data)
        if cartser.is_valid(raise_exception=True):
            cartser.save(service_key=str(key))

    def handle_service_get_request(self, key, query_param):
        # Get service data
        # (Note:Sonu) TBD filter query parameters
        caelems = Cart.objects.filter(service_key=str(key))
        ser = CartSerializer(caelems, many=True)
        return ser


class OfferDriver(object):
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
        offser = OfferSerializer(data=req_data)
        if offser.is_valid(raise_exception=True):
            offser.save(service_key=str(key))

    def handle_service_get_request(self, key, query_param):
        # Get service data
        # (Note:Sonu) TBD filter query parameters
        offers = Offer.objects.filter(service_key=str(key))
        ser = OfferSerializer(offers, many=True)
        return ser


class EventDriver(object):
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
        evtser = EventSerializer(data=req_data)
        if evtser.is_valid(raise_exception=True):
            evtser.save(service_key=str(key))

    def handle_service_get_request(self, key, query_param):
        # Get service data
        # (Note:Sonu) TBD filter query parameters
        events = Event.objects.filter(service_key=key)
        ser = EventSerializer(events, many=True)
        return ser
