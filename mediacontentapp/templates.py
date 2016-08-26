'''
Created on Aug 19, 2016

@author: sonu
'''

from jinja2 import Template
import json
from django.conf import settings
from mediacontentapp.sourceserializers import DigitalMediaSourceSerializer
from mediacontentapp.sourceserializers import MediaAggregatorTypeSerializer


class DigitalMediaSourceTemplate():

    def __init__(self):
        self.j2_template = Template(
                            open('%s%s' % (settings.MEDIAAPP_DIR,
                                           'templates/digital_media_source.j2'),
                                 'r').read())

    def create_instance(self, **kwargs):
        # Create the serializer
        ser = DigitalMediaSourceSerializer(data=self.j2_template.render(**kwargs))
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
        ser = MediaAggregatorTypeSerializer(data=_data)
        if ser.is_valid(raise_exception=True):
            return ser.save()

    def update_instance(self, type_instance, **kwargs):
        # Update the instance
        ser = MediaAggregatorTypeSerializer(data=self.j2_template.render(**kwargs),
                                            partial=True)
        if ser.is_valid(raise_exception=True):
            return ser.update(type_instance)
