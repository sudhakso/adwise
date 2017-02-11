'''
Created on Jan 21, 2017

@author: sonu
'''
from django.conf import settings
import json
import httplib
from templates import CloudNotifierMessageTemplate, \
 CloudNotifierDataMessageTemplate


class CloudNotifier():

    def __init__(self):
        self._notification_template = CloudNotifierMessageTemplate()
        self._data_template = CloudNotifierDataMessageTemplate()

    def notify(self, device_ids, notif_topic, notif_type, notif_content):
        if device_ids:
            print "Following devices will be notified - %s" % device_ids
            connection = httplib.HTTPSConnection(settings.FIREBASE_URL)
            headers = {'Content-type': 'application/json',
                       'Authorization': settings.FIREBASE_KEY,
                       'Project-ID': settings.FIREBASE_PROJECT_ID}
            if notif_type == 'notification':
                json_notif_data = self._notification_template.create_message(topic=notif_topic,
                                                                             content=notif_content,
                                                                             device_ids=device_ids)
            else:
                json_notif_data = self._data_template.create_message(topic=notif_topic,
                                                                     content=notif_content,
                                                                     device_ids=device_ids)
            print "Message header %s" % headers
            print "Message formatted %s" % json_notif_data
            connection.request('POST', '/fcm/send', json_notif_data, headers)
            response = connection.getresponse()
            print(response.read().decode())
            return response.status
