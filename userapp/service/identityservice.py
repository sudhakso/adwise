'''
Created on Nov 23, 2015

@author: sonu
'''
from django.conf import settings
from userapp import Config
from userapp import importutils
from datetime import datetime
from abc import ABCMeta, abstractmethod
from userapp.faults import UserNotAuthorizedException


class IdentityDriver(object):
    '''
    classdocs
    '''
    def __init__(self, *args):
        '''
        Constructor
        '''
        pass

    @abstractmethod
    def do_auth(self, *args):
        pass


class KeystoneDriver(IdentityDriver):
    '''
    classdocs
    '''
    def __init__(self, *args):
        '''
        Constructor
        '''
        pass

    # TBD (Note:Sonu) Validate with keystone
    # end-point
    def do_auth(self, *args):
        raise UserNotAuthorizedException()


class NoopDriver(IdentityDriver):
    '''
    classdocs
    '''
    def __init__(self, *args):
        '''
        Constructor
        '''
        pass


class DriverFactory(object):
    @staticmethod
    def get_driver(typ):
        # TBD (Note:Sonu): fetch all relevant arguments
        # for that type.
        # TBD (Note:Sonu): Create driver singleton for performance
        args = {}
        if typ == 'keystone':
            return KeystoneDriver(*args)
        elif typ == 'noop':
            return NoopDriver(*args)


class IdentityManager(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        param = {
            'default_ini': '%s%s' % (settings.USERAPP_DIR, 'userconfig.ini'),
            'default_value_map': {}
            }

        self.usercfg = Config.config(**param)
        self.auth_strategy = self.usercfg.get_config(
                                        'DEFAULT', 'auth_strategy')
        # Load the auth driver parameters
        self.driver = self._load_driver(typ=self.auth_strategy)

    def _load_driver(self, typ):
        return DriverFactory.get_driver(typ)

    def do_auth(self, header):
        # Initiate an auth request to the driver
        self.driver.do_auth(header)

    def remove_expired_session(self, user_id):
        pass

    def remove_session(self, user_id, session_id):
        pass

    def check_session_active(self, user_id):
        pass
