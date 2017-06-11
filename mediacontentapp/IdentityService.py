'''
Created on Nov 23, 2015

@author: sonu
'''
from django.conf import settings
from userapp import Config
from abc import abstractmethod
from userapp.faults import UserNotAuthorizedException, UserNotFoundException

# Basic authentication
from django.contrib.auth.models import User


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
    def do_auth(self, request):
        pass

    @abstractmethod
    def log_auth(self, request):
        pass

    @abstractmethod
    def do_create(self, request):
        pass

    @abstractmethod
    def remove_expired_session(self, request):
        pass


class KeystoneDriver(IdentityDriver):
    '''
    classdocs
    '''
    def __init__(self, request):
        '''
        Constructor
        '''
        pass

    # TBD (Note:Sonu) Validate with keystone
    # end-point
    def do_auth(self, request):
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

    @abstractmethod
    def do_auth(self, request):
        from django.contrib.auth import login
#         from mongoengine.django.auth import User
        from mongoengine.queryset import DoesNotExist
        from django.contrib import messages
        # Get all Http headers
        import re
        regex = re.compile('^HTTP_')
        head = dict((regex.sub('', header), value) for (header, value)
                    in request.META.items() if header.startswith('HTTP_'))

        try:
            user = User.objects.get(username=head['USERNAME'])
            if user.check_password(head['PASSWORD']):
                user.backend = 'mongoengine.django.auth.MongoEngineBackend'
                print login(request, user)
                return user
            else:
                raise UserNotAuthorizedException(
                                "Incorrect login name or password!")
        except DoesNotExist:
            raise UserNotFoundException("User does not exist.")

    @abstractmethod
    def log_auth(self, request):
        from django.contrib.auth import login
#         from mongoengine.django.auth import User
        from mongoengine.queryset import DoesNotExist
        from django.contrib import messages
        # Get all Http headers
        import re
        regex = re.compile('^HTTP_')
        head = dict((regex.sub('', header), value) for (header, value)
                    in request.META.items() if header.startswith('HTTP_'))

        if 'USERNAME' in head:
            try:
                user = User.objects.get(username=head['USERNAME'])
                return user
            except DoesNotExist:
                return None


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
            'default_ini': '%s%s' % (settings.MEDIAAPP_DIR, 'mediaconfig.ini'),
            'default_value_map': {}
            }

        self.usercfg = Config.config(**param)
        self.auth_strategy = self.usercfg.get_config(
                                        'DEFAULT', 'auth_strategy')
        # Load the auth driver parameters
        self.driver = self._load_driver(typ=self.auth_strategy)

    def _load_driver(self, typ):
        return DriverFactory.get_driver(typ)

    def log_auth(self, request):
        # Initiate an auth request to the driver
        return self.driver.log_auth(request)

    def do_auth(self, request):
        # Initiate an auth request to the driver
        return self.driver.do_auth(request)

    def do_create(self, request):
        # Create session first time
        self.driver.do_create(request)

    def remove_expired_session(self, request):
        self.driver.remove_expired_session(request)

    def remove_session(self, user_id, session_id):
        pass

    def check_session_active(self, user_id):
        pass
