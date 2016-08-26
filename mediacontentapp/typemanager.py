'''
Created on Aug 20, 2016

@author: sonu
'''

from django.conf import settings
from mediacontentapp import Config
from mediacontentapp import importutils
import inspect
from mongoengine.errors import DoesNotExist
from mediacontentapp.models import MediaAggregatorType
from templates import MediaAggregatorTypeTemplate


class MediaTypeManager(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        param = {
            'default_ini': '%s%s' % (
                        settings.MEDIAAPP_DIR, 'mediaconfig.ini'),
            'default_value_map': {}
            }

        self.typecfg = Config.config(**param)
        self.enabled_types = self.typecfg.get_config(
                                        'types',
                                        'type_driver').split(',')
        # Type instances in DB
        self._mediatypesdirectory = {}
        self.factory = MediaAggregatorTypeTemplate()
        self._loadtypedrivers()

    @property
    def mediatypesdirectory(self):
        # DB related
        return self._mediatypesdirectory

    def get_or_none(self, classmodel, **kwargs):
        try:
            return classmodel.objects.get(**kwargs)
        except classmodel.DoesNotExist:
            return None

    def _loadtypedrivers(self):
        for typedriver in self.enabled_types:
            # Import provider service
            provider = importutils.import_module(typedriver)
            types = inspect.getmembers(provider, inspect.isclass)
            print('Loading media aggregator types %s' % types)
            # Create DB object if it doesn't exist already
            for type in types:
                # Lets create a temporary object
                typeobj = getattr(provider, type[0])()
                try:
                    if typeobj.typename:
                        obj = MediaAggregatorType.objects.get(
                                                typename=typeobj.typename)
                        print('Type %s already defined by the driver %s - Type exists'
                              % (type[0], typedriver))
                        continue
                    else:
                        # Skip the type
                        print('Malformed type definition for %s from %s' % (
                                                    type[0], typedriver))
                        continue
                except DoesNotExist as e:
                    # Creates a new type in the DB
                    newtype = self.factory.create_instance(
                                                    typename=typeobj.typename,
                                                    category=typeobj.category,
                                                    typespec={},
                                                    typedesc=typeobj.typedesc)
                    self._mediatypesdirectory[typeobj.typename] = newtype
                except Exception as e:
                    print(e)
