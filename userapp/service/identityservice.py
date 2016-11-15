'''
Created on Nov 23, 2015

@author: sonu
'''
from django.conf import settings
from userapp import Config
from abc import abstractmethod
from userapp.faults import UserNotAuthorizedException, UserNotFoundException, UserAlreadyExist

# Basic authentication
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


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
                return True
            else:
                raise UserNotAuthorizedException(
                                "Incorrect login name or password!")
        except DoesNotExist:
            raise UserNotFoundException("User does not exist.")

    @abstractmethod
    def do_create(self, request):
        # Get all Http headers
        import re
        regex = re.compile('^HTTP_')
        head = dict((regex.sub('', header), value) for (header, value)
                    in request.META.items() if header.startswith('HTTP_'))
        user = None
        try:
            user = User.objects.get(username=head['USERNAME'])
            if user:
                raise UserAlreadyExist()
        except ObjectDoesNotExist:
            # User doesn't exist.
            usr = User.objects.create(username=head['USERNAME'],
                                      email=head['EMAIL'])
            usr.set_password(head['PASSWORD'])
            usr.save()
        return user

    @abstractmethod
    def do_update(self, request, username, password):
        # Get all Http headers
        import re
        regex = re.compile('^HTTP_')
        head = dict((regex.sub('', header), value) for (header, value)
                    in request.META.items() if header.startswith('HTTP_'))
        user = None
        try:
            user = User.objects.get(username=head['USERNAME'])
            user.set_password(password)
            user.save()
        except ObjectDoesNotExist:
            pass

        return user

    @abstractmethod
    def remove_expired_session(self, request):
        # Get all Http headers
        import re
        regex = re.compile('^HTTP_')
        head = dict((regex.sub('', header), value) for (header, value)
                    in request.META.items() if header.startswith('HTTP_'))
        try:
            user = User.objects.get(username=head['USERNAME'])
            if user:
                user.delete()
            # Raise exception if user exists.
        except Exception:
            # User doesn't exist.
            pass
        # Always successful
        return True


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

    def do_auth(self, request):
        # Initiate an auth request to the driver
        self.driver.do_auth(request)

    def do_create(self, request):
        # Create session first time
        self.driver.do_create(request)

    def do_update(self, request, username, password):
        # Create session first time
        self.driver.do_update(request, username, password)

    def remove_expired_session(self, request):
        self.driver.remove_expired_session(request)

    def remove_session(self, user_id, session_id):
        pass

    def check_session_active(self, user_id):
        pass
