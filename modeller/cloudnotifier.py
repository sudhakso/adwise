'''
Created on Jan 21, 2017

@author: sonu
'''
from django.conf import settings
import json
import httplib
from templates import CloudNotifierMessageTemplate


class CloudNotifier():

    def __init__(self):
        self._message_template = CloudNotifierMessageTemplate()

    def notify(self, device_ids, notif_topic, notif_content):
        if device_ids:
            print "Following devices - %s" % device_ids
            connection = httplib.HTTPSConnection(settings.FIREBASE_URL)
            headers = {'Content-type': 'text/plain',
                       'Authorization': settings.FIREBASE_KEY,
                       'project_id': settings.FIREBASE_PROJECT_ID}
            json_notif_data = self._message_template.create_message(topic=notif_topic,
                                                                    content=notif_content,
                                                                    device_ids=device_ids)
            print "Message formatted %s" % json_notif_data
            connection.request('POST', '/fcm/send', json_notif_data, headers)
            response = connection.getresponse()
            print(response.read().decode())
            return response.status


