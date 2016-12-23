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

    @abstractmethod
    def handle_service_get_request(self, key, req_param):
        return self.driver.handle_service_get_request(key,
                                                      req_param)


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
        print 'Handling userlocationservice request...(%s)' % service_data
        super(UserLocationService, self).handle_service_request(key, service_data)

    def handle_service_get_request(self, key, req_param):
        print 'Handling userlocationservice request...'
        return super(UserLocationService, self).handle_service_get_request(
                                                            key,
                                                            req_param)


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

    def handle_service_get_request(self, key, req_param):
        print 'Handling UserMeteringService request...'
        return super(UserMeteringService, self).handle_service_get_request(
                                                            key,
                                                            req_param)


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

    def handle_service_get_request(self, key, req_param):
        print 'Handling CloudMessagingService request...'
        return super(CloudMessagingService, self).handle_service_get_request(
                                                            key,
                                                            req_param)


class NotificationService(BaseService):

    def setup_service(self):
        print 'Setting up NotificationService...'
        super(NotificationService, self).setup_service()

    @property
    def servicedriver_name(self):
        return 'userapp.servicedriver.driver.NotificationDriver'

    def update_service(self, service_id):
        print 'Updating NotificationService...'
        super(NotificationService, self).update_service(service_id)

    def teardown_service(self, service_id):
        print 'Tearing down NotificationService...'
        super(NotificationService, self).teardown_service(service_id)

    def handle_service_request(self, key, service_data):
        print 'Handling NotificationService request...'
        super(NotificationService, self).handle_service_request(
                                                key, service_data)

    def handle_service_get_request(self, key, req_param):
        print 'Handling NotificationService request...'
        return super(NotificationService, self).handle_service_get_request(
                                                            key,
                                                            req_param)


class EventService(BaseService):

    def setup_service(self):
        print 'Setting up EventService...'
        super(EventService, self).setup_service()

    @property
    def servicedriver_name(self):
        return 'userapp.servicedriver.driver.EventDriver'

    def update_service(self, service_id):
        print 'Updating EventService...'
        super(EventService, self).update_service(service_id)

    def teardown_service(self, service_id):
        print 'Tearing down EventService...'
        super(EventService, self).teardown_service(service_id)

    def handle_service_request(self, key, service_data):
        print 'Handling EventService request...'
        super(EventService, self).handle_service_request(
                                                key, service_data)

    def handle_service_get_request(self, key, req_param):
        print 'Handling EventService request...'
        return super(EventService, self).handle_service_get_request(
                                                            key,
                                                            req_param)


class CartService(BaseService):

    def setup_service(self):
        print 'Setting up CartService...'
        super(CartService, self).setup_service()

    @property
    def servicedriver_name(self):
        return 'userapp.servicedriver.driver.CartDriver'

    def update_service(self, service_id):
        print 'Updating CartService...'
        super(CartService, self).update_service(service_id)

    def teardown_service(self, service_id):
        print 'Tearing down CartService...'
        super(CartService, self).teardown_service(service_id)

    def handle_service_request(self, key, service_data):
        print 'Handling CartService request...'
        super(CartService, self).handle_service_request(
                                                key, service_data)

    def handle_service_get_request(self, key, req_param):
        print 'Handling CartService request...'
        return super(CartService, self).handle_service_get_request(
                                                            key,
                                                            req_param)


class OfferService(BaseService):

    def setup_service(self):
        print 'Setting up OfferService...'
        super(OfferService, self).setup_service()

    @property
    def servicedriver_name(self):
        return 'userapp.servicedriver.driver.OfferDriver'

    def update_service(self, service_id):
        print 'Updating OfferService...'
        super(OfferService, self).update_service(service_id)

    def teardown_service(self, service_id):
        print 'Tearing down OfferService...'
        super(OfferService, self).teardown_service(service_id)

    def handle_service_request(self, key, service_data):
        print 'Handling OfferService request...'
        super(OfferService, self).handle_service_request(
                                                key, service_data)

    def handle_service_get_request(self, key, req_param):
        print 'Handling OfferService request...(%s)'
        return super(OfferService, self).handle_service_get_request(
                                                            key,
                                                            req_param)


class MyFavouriteService(BaseService):

    def setup_service(self):
        print 'Setting up MyFavouriteService...'
        super(MyFavouriteService, self).setup_service()

    @property
    def servicedriver_name(self):
        return 'userapp.servicedriver.driver.FavouriteDriver'

    def update_service(self, service_id):
        print 'Updating MyFavouriteService...'
        super(MyFavouriteService, self).update_service(service_id)

    def teardown_service(self, service_id):
        print 'Tearing down MyFavouriteService...'
        super(MyFavouriteService, self).teardown_service(service_id)

    def handle_service_request(self, key, service_data):
        print 'Handling MyFavouriteService request...'
        super(MyFavouriteService, self).handle_service_request(
                                                key, service_data)

    def handle_service_get_request(self, key, req_param):
        print 'Handling MyFavouriteService request...(%s)'
        return super(MyFavouriteService, self).handle_service_get_request(
                                                            key,
                                                            req_param)
