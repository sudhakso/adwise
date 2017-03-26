'''
Created on Mar 25, 2017

@author: sonu
'''
from jinja2 import Template
import json
from django.conf import settings
from mongoengine.fields import GeoPointField
from pyes import ES
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from userapp.JSONFormatter import JSONResponse
from datetime import date, datetime
import Config


class ESMapper():
    # Initialize the mapper config
    def __init__(self, config):
        self.mappers = [e.strip() for e in config.get_config(
                                    'indexing', 'mapping').split(',')]

    def get_mapping(self, _type):
        for mapper in self.mappers:
            name = mapper.split(':')[0]
            maptemplate = mapper.split(':')[1]
            if name == _type:
                j2_template = Template(
                        open('%s%s' % (settings.USERAPP_DIR,
                                       'templates/%s' % maptemplate),
                             'r').read())
                _data = json.loads(str(j2_template.render()))
                return _data
        return None


class IndexingService():

    def __init__(self):
        '''
        Constructor
        '''
        param = {
            'default_ini': '%s%s' % (settings.USERAPP_DIR, 'userconfig.ini'),
            'default_value_map': {}
            }

        self.indexcfg = Config.config(**param)
        self.endpoint = self.indexcfg.get_config(
                                        'indexing', 'pyes_endpoint')
        self.indexing_tags = [e.strip() for e in self.indexcfg.get_config(
                                            'indexing', 'index').split(',')]
        self._conn = ES(self.endpoint)
        self._mapper = ESMapper(self.indexcfg)
        # create the indexes
        self.create_indexes(self.indexing_tags)

    @property
    def connection(self):
        return self._conn

    def status(self):
        pass

    def create_indexes(self, tags):
        for index in tags:
            try:
                print "Creating index (%s)..." % (index)
                self.connection.indices.create_index_if_missing(index.lower())
                # Generate the mapping for the index if specified.
                print "Checking mapping types for index (%s)..." % (index)
                mapdata = self._mapper.get_mapping(index)
                if mapdata is not None:
                    print "Creating mapping types for index (%s)..." % (index)
                    self.connection.indices.put_mapping(
                                                'external',
                                                {'properties': mapdata},
                                                [index.lower()])
            except TypeError as te:
                print "Exception creating index (%s). Index exists : (%s)." % (
                                                        index, str(te))
            except Exception as e:
                print "Exception creating index (%s). Critical : (%s)." % (
                                                        index, str(e))
