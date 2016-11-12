'''
Created on Nov 23, 2015

@author: sonu
'''
from django.conf import settings
from userapp import Config
from userapp import importutils
from userapp.models import Service


class ServiceManager(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        param = {
            'default_ini': '%s%s' % (
                        settings.USERAPP_DIR, 'serviceconfig.ini'),
            'default_value_map': {}
            }

        self.svccfg = Config.config(**param)
        self.enabled_services = self.svccfg.get_config(
                                        'DEFAULT',
                                        'enabled_services').split(',')
        # Service instances in DB
        self._servicedirectory = {}
        # Service instances/provider
        self._serviceprovider = {}

        self._loadservices()

    @property
    def servicedirectory(self):
        # DB related
        return self._servicedirectory

    @property
    def serviceprovider(self):
        # Runtime service provider
        return self._serviceprovider

    def get_or_none(self, classmodel, **kwargs):
        try:
            return classmodel.objects.get(**kwargs)
        except classmodel.DoesNotExist:
            return None

    def _loadservices(self):
        for name in self.enabled_services:
            # Get the driver name
            providername = self.svccfg.get_config(name, 'name')
            # Import provider service
            provider = importutils.import_object(providername)

            kwargs = {'service_friendly_name': name,
                      'service_provider': providername,
                      'service_driver': provider.servicedriver_name}
            # Create DB object if it doesn't exist already
            service = self.get_or_none(Service,
                                       service_friendly_name=name)
            if service is None:
                service = Service.objects.create(**kwargs)

            self._serviceprovider[name] = provider
            self._servicedirectory[name] = service

    def handle_service_request(self, svc, reqbody):
        self.serviceprovider[
            svc.service_id.service_friendly_name].handle_service_request(
                                        svc.id,
                                        reqbody)

    def handle_service_get_request(self, svc, reqparam):
        return self.serviceprovider[
            svc.service_id.service_friendly_name].handle_service_get_request(
                                        svc.id,
                                        reqparam)
