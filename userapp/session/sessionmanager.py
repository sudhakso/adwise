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

    def prepare_user_service(self, user, service):
        # If the service_name exists for the User, return the service-id
        reg_service = UserService.objects.filter(user_ref=user,
                                                 service_id=service)
        if reg_service:
            # Returns the first element.
            return reg_service[0]
        # Service was not found, so create it.
        reg_session = UserSession.objects.filter(user_ref=user)
        # If session is not known, create it!
        if reg_session:
            session = reg_session[0]
        else:
            session = self.create_session(user)
        # Lookup the service
        kwargs = {
                'user_ref': user,
                'user_session': session,
                'service_id': service,
                'enabled': True,
                'last_report_time': datetime.now(),
                'auto_restart': True
        }
        usersvc = UserService.objects.create(**kwargs)
        # Append the service created into UserSession object for future
        # reference.
        session.services.append(usersvc)
        return usersvc

    def remove_expired_session(self, user_id):
        pass

    def remove_session(self, user_id, session_id):
        pass

    def check_session_active(self, user_id):
        pass
