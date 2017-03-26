'''
Created on Dec 25, 2015

@author: sonu
'''
from userapp.models import UserService, Location, MediaUser
from userapp.tasks import fetch_ad, UserIndexingTask
from userapp.serializers import UserSerializer, UserIndexSerializer
import json

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


def index_mediauser(sender, document, created):
    print "Placeholder for indexing user"
    # MediaUser Index task
    if created:
        usr = UserIndexSerializer(document, many=False)
        task = UserIndexingTask()
        rc = task.delay(args=[],
                        instancename=str(document.id),
                        mediauser=json.dumps(usr.data),
                        ignore_failures=False)
        if rc.state == "SUCCESS":
            print "index_mediauser task status: OK."
        else:
            print "index_mediauser task status: Not OK."
    else:
            print "index_mediauser: task status: Unchanged OK."


# Register all model handlers
# TBD: Make it more self organized
signals.post_save.connect(location_handler, Location)
signals.post_save.connect(index_mediauser, MediaUser)
