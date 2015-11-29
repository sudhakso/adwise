'''
Created on Nov 23, 2015

@author: sonu
'''
from django.conf import settings
from userapp import Config
from userapp.models import MediaUser, UserSession,\
 UserService
from userapp.faults import UserNotFoundException,\
 UserSessionNotFoundException, UserNotAuthorizedException
from userapp import importutils
from userapp.service import servicemanager
from datetime import datetime


class SessionManager(object):
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
        self.user_enabled_services = self.usercfg.get_config(
                                        'DEFAULT', 'services').split(',')
        # TBD (Note:Sonu)
        # Re-factor - containment not appropriate.
        self.servicemanager = servicemanager.ServiceManager()

    def create_session(self, user_id, raise_exception=True):
        # Get the user
        if user_id is None:
            if raise_exception:
                raise UserNotFoundException
            return
        # Create the session
        usersess = UserSession.objects.create(user_ref=user_id)
        return usersess

    def prepare_service(self, user_id, sess_id, service_name,
                        args, raise_exception=True):
        # If session is not known
        if sess_id is None:
            sess_id = self.create_session(user_id)

        # Lookup the service
        if service_name in self.user_enabled_services:
            kwargs = {
                    'user_ref': user_id,
                    'user_session': sess_id,
                    'service_id': self.servicemanager.servicedirectory[
                                        service_name],
                    'enabled': True,
                    'last_report_time': datetime.now(),
                    'auto_restart': True
                    }
            usersvc = UserService.objects.create(**kwargs)
        return usersvc

    def remove_expired_session(self, user_id):
        pass

    def remove_session(self, user_id, session_id):
        pass

    def check_session_active(self, user_id):
        pass
