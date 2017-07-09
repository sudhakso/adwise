'''
Created on Nov 23, 2015

@author: sonu
'''
from django.conf import settings
from userapp import Config
from userapp import importutils


class SensorDriverFactory(object):

    def __init__(self):
        self._sensor_driectory = {}

    def driver(self, name):
        return self._sensor_driectory[name]

    def register_driver(self, name, driver, **kwargs):
        provider = importutils.import_object(driver, **kwargs)
        self._sensor_driectory[name] = provider


class SensorManager(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        param = {
            'default_ini': '%s%s' % (settings.MEDIAAPP_DIR, 'mediaconfig.ini'),
            'default_value_map': {}
            }
        self.sensorcfg = Config.config(**param)
        self.factory = SensorDriverFactory()
        sensors = self.sensorcfg.get_config(
                                        'sensor', 'types').split(',')
        for sensor in sensors:
            self.register(ns='sensor.' + sensor.strip(), name=sensor.strip())

    @property
    def sensor_factory(self):
        return self.factory

    def register(self, ns, name):
        args = dict(self.sensorcfg.get_config_list(ns))
        self.factory.register_driver(name, **args)
