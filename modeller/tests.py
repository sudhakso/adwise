from django.test import TestCase
from modeller import cloudnotifier
from userapp.models import MediaUser
from userapp.serializers import UserDevicePrefSerializer
import json
# Create your tests here.


def main():
    devices = []
    for user in MediaUser.objects.all():
        devices.extend(user.device_pref)
    devs = UserDevicePrefSerializer(devices, many=True)
    _srjson = json.dumps(devs.data, encoding='utf-8')

    notif_topic = 'marketing'
    notif_content = '{"somecontent":"someconente"}'
    print 'Sending %s notifications %s to %s ...' % (notif_topic, notif_content, _srjson)
    # return all users

    deviceidjson = json.loads(_srjson)
    registered_ids = []
    for device in deviceidjson:
        if 'device_info' in device:
            devinfo = device['device_info']
            if 'device_id' in devinfo:
                registered_ids.append(devinfo['device_id'])
    print registered_ids
    return cloudnotifier.CloudNotifier().notify(registered_ids,
                                                notif_topic,
                                                notif_content)



if __name__ == '__main__':
    main()

