'''
Created on Aug 19, 2016

@author: sonu
'''

from jinja2 import Template
import json
from django.conf import settings
from mediacontentapp.sourceserializers import DigitalMediaSourceSerializer,\
    AmenitySerializer
from mediacontentapp.sourceserializers import MediaAggregateTypeSerializer


class AmenityTemplate():

    def __init__(self):
        self.j2_template = Template(
                            open('%s%s' % (settings.MEDIAAPP_DIR,
                                           'templates/amenity.j2'),
                                 'r').read())

    def create_instance(self, **kwargs):
        # Create the serializer
        _str = str(self.j2_template.render(**kwargs)).encode('utf-8')
        _str = _str.replace("\'","\"").replace("u\"","\"").replace("u\'","\'")
        _data = json.loads(_str)
        print _data
        ser = AmenitySerializer(data=_data)
        if ser.is_valid(raise_exception=True):
            return ser.save()

    def update_instance(self, media_instance, **kwargs):
        # Update the instance
        ser = AmenitySerializer(data=self.j2_template.render(**kwargs),
                                partial=True)
        if ser.is_valid(raise_exception=True):
            return ser.update(media_instance)


class DigitalMediaSourceTemplate():

    def __init__(self):
        self.j2_template = Template(
                            open('%s%s' % (settings.MEDIAAPP_DIR,
                                           'templates/digital_media_source.j2'),
                                 'r').read())

    def create_instance(self, **kwargs):
        # Create the serializer
        _data = json.loads(str(self.j2_template.render(**kwargs)))
        ser = DigitalMediaSourceSerializer(data=_data)
        if ser.is_valid(raise_exception=True):
            return ser.save()

    def update_instance(self, media_instance, **kwargs):
        # Update the instance
        ser = DigitalMediaSourceSerializer(data=self.j2_template.render(**kwargs),
                                           partial=True)
        if ser.is_valid(raise_exception=True):
            return ser.update(media_instance)


class MediaAggregatorTypeTemplate():

    def __init__(self):
        self.j2_template = Template(
                            open('%s%s' % (settings.MEDIAAPP_DIR,
                                           'templates/media_aggregator_type.j2'),
                                 'r').read())

    def create_instance(self, **kwargs):
        # Create the serializer
        _data = json.loads(str(self.j2_template.render(**kwargs)))
        ser = MediaAggregateTypeSerializer(data=_data)
        if ser.is_valid(raise_exception=True):
            return ser.save()

    def update_instance(self, type_instance, **kwargs):
        # Update the instance
        ser = MediaAggregateTypeSerializer(data=self.j2_template.render(**kwargs),
                                            partial=True)
        if ser.is_valid(raise_exception=True):
            return ser.update(type_instance)
