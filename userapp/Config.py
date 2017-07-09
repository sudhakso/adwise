'''
Created on Apr 25, 2015

@author: sudhakso
'''

import ConfigParser


class config(object):
    '''
    classdocs
    '''
    def __init__(self, default_ini, default_value_map={}):
        '''
        Constructor
        '''
        self._DEFAULT_VALUE_MAP = {}
        self._DEFAULT_VALUE_MAP = default_value_map.copy()
        self.cfg_parser = ConfigParser.SafeConfigParser()

        # Load the configuration from file
        self.cfg_parser.read([default_ini])

    def set_config(self, section, key, value):
        self.cfg_parser.set(section, key, value)

    def get_config(self, ns, key):
        return self.cfg_parser.get(ns, key)

    def get_config_list(self, ns):
        l = [item for item in self.cfg_parser.items(ns) if item[0] not in self.cfg_parser.defaults()]
        return l

