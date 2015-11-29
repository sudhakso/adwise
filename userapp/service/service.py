'''
Created on Nov 24, 2015

@author: sonu
'''
from abc import ABCMeta, abstractmethod
from userapp.importutils import import_object


class BaseService(object):
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta

    def __init__(self):
        '''
        Constructor
        '''
        self.driver = None
        self.setup_service()

    @property
    @abstractmethod
    def servicedriver_name(self):
        return None

    @abstractmethod
    def setup_service(self):
        if self.servicedriver_name is not None:
            self.driver = import_object(self.servicedriver_name)

    @abstractmethod
    def update_service(self, service_id):
        pass

    @abstractmethod
    def teardown_service(self, service_id):
        pass

    @abstractmethod
    def handle_service_request(self, key, service_data):
        return self.driver.handle_service_request(key, service_data)


class UserLocationService(BaseService):

    def setup_service(self):
        print 'Setting up userlocationservice...'
        super(UserLocationService, self).setup_service()

    @property
    def servicedriver_name(self):
        return 'userapp.servicedriver.driver.LocationDriver'

    def update_service(self, service_id):
        print 'Updating userlocationservice...'
        super(UserLocationService, self).update_service(service_id)

    def teardown_service(self, service_id):
        print 'Tearing down userlocationservice...'
        super(UserLocationService, self).teardown_service(service_id)

    def handle_service_request(self, key, service_data):
        print 'Handling userlocationservice request...'
        super(UserLocationService, self).handle_service_request(key, service_data)


class UserMeteringService(BaseService):

    def setup_service(self):
        print 'Setting up usermeteringservice...'
        super(UserMeteringService, self).setup_service()

    @property
    def servicedriver_name(self):
        return 'userapp.servicedriver.driver.MeteringDriver'

    def update_service(self, service_id):
        print 'Updating UserMeteringService...'
        super(UserMeteringService, self).update_service(service_id)

    def teardown_service(self, service_id):
        print 'Tearing down UserMeteringService...'
        super(UserMeteringService, self).teardown_service(service_id)

    def handle_service_request(self, key, service_data):
        print 'Handling UserMeteringService request...'
        super(UserMeteringService, self).handle_service_request(key, service_data)


class CloudMessagingService(BaseService):

    def setup_service(self):
        print 'Setting up CloudMessagingService...'
        super(CloudMessagingService, self).setup_service()

    @property
    def servicedriver_name(self):
        return 'userapp.servicedriver.driver.CloudmessagingDriver'

    def update_service(self, service_id):
        print 'Updating CloudMessagingService...'
        super(CloudMessagingService, self).update_service(service_id)

    def teardown_service(self, service_id):
        print 'Tearing down CloudMessagingService...'
        super(CloudMessagingService, self).teardown_service(service_id)

    def handle_service_request(self, key, service_data):
        print 'Handling CloudMessagingService request...'
        super(CloudMessagingService, self).handle_service_request(
                                                key, service_data)
