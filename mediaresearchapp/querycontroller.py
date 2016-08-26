'''
Created on May 14, 2016

@author: sonu
'''
import inspect
from django.conf import settings
from mediaresearchapp import Config


class querytype_controller():
    def __init__(self):
        '''
        Constructor
        '''
        param = {
            'default_ini': [
                        '%s%s' % (settings.SEARCHAPP_DIR, 'researchconfig.ini')
            ],
            'default_value_map': {}
            }
        self.module_ = __import__('mediaresearchapp')
        self.tasks_ = getattr(self.module_, 'tasks')
        self._query_typemaps = {}
        self.querycfg = Config.config(**param)
        self._query_types = [e.strip() for e in self.querycfg.get_config(
                                            'typemaps', 'types').split(',')]
        for e in self._query_types:
            _type, driver = e.split(':')
            self._query_typemaps[_type] = driver

    def create_task(self, type):
        # TBD (Note:Sonu) Load once
        class_ = getattr(self.tasks_, self._query_typemaps[type])
        return class_()
