'''
Created on Dec 25, 2015

@author: sonu
'''
from userapp.models import UserService, Location
from userapp.tasks import fetch_ad
from userapp.serializers import UserSerializer

from mongoengine import signals


def location_handler(sender, document, created):
    print 'Location Created {service_key=%s, point=%s}' % (
                                        document.service_key, document.point)
    # TBD : Can we avoid this lookup?
    # Expect a single Service instance.
    svc = UserService.objects.get(id=document.service_key)
    userdata = UserSerializer(svc.user_ref)
    pointfileds = {"point": document.point}
    # Call the celery task
    # TBD: Error and State checking
    fetch_ad.delay(user=userdata.data, geopoint=pointfileds)

# Register all model handlers
# TBD: Make it more self organized
signals.post_save.connect(location_handler, Location)
