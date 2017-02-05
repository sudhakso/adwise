'''
Created on Jan 21, 2017

@author: sonu
'''
from __future__ import absolute_import

from celery import Task
from modeller.classifierclient import Classifier
from modeller.cloudnotifier import CloudNotifier
from mediacontentapp.models import Amenity, NearBy
import json
from mediacontentapp.sourceserializers import MediaSourceSerializer
from userapp.models import MediaUser
from userapp.serializers import UserDevicePrefSerializer


class ClassifierTask(Task):
    ignore_errors = True
    _clsifier = None

    @property
    def classifier(self):
        if self._clsifier is None:
            self._clsifier = Classifier()
        return self._clsifier

    def run(self, message):
        print 'Classifying %s ...' % message
        category = self.classifier.classify(message)

        print 'Classifier classified %s into category %s ...' % (
                                                    message, category)
        return category


class FindOOHFiltered(Task):
    # category = sports|bank etc..
    # filters =
    #    [
    #     {"type": "costfilter", "condition": "maximum", "value": "100000"},
    #     {"type": "dgfilter", "condition": "target", "value": "parents"}
    #    ]
    ignore_errors = True

    def run(self, category, filters):
        # TBD :  filters to be implemented!
        print 'FindOOHFiltered %s (%s)...' % (category, filters)
        amenities = Amenity.objects.filter(type=category)
        nearbys = NearBy.objects.filter(amenity__in=amenities)
        sources_relevant = [nearby.media_source for nearby in nearbys]
        ser_sources = MediaSourceSerializer(sources_relevant,
                                            many=True)
        _srjson = json.dumps(ser_sources.data, encoding='utf-8')
        return _srjson


class UserSelectorTask(Task):
    ignore_errors = True

    # TBD(Note:Sonu) It returns all the Users at the moment,
    # Need to build selectors
    def run(self, selector):
        print 'Selecting users for the following %s ...' % selector
        # return all users
        devices = []
        for user in MediaUser.objects.all():
            devices.extend(user.device_pref)
        devs = UserDevicePrefSerializer(devices, many=True)
        _srjson = json.dumps(devs.data, encoding='utf-8')
        return _srjson


class CloudNotifierTask(Task):
    ignore_errors = True
    _cloud_notifier = None

    @property
    def cloud_notifier(self):
        if self._cloud_notifier is None:
            self._cloud_notifier = CloudNotifier()
        return self._cloud_notifier

    def run(self, devices, notif_topic, notif_content):
        print 'Sending %s notifications %s to %s ...' % (notif_topic,
                                                         notif_content,
                                                         devices)
        # return all users
        print 'Sending %s notifications %s to %s ...' % (
                                                    notif_topic,
                                                    notif_content,
                                                    devices)
        deviceidjson = json.loads(devices)
        registered_ids = []
        for device in deviceidjson:
            if 'device_info' in device:
                devinfo = device['device_info']
                if 'device_id' in devinfo:
                    registered_ids.append(devinfo['device_id'])
        return self.cloud_notifier.notify(registered_ids,
                                          notif_topic,
                                          notif_content)
