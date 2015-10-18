from userapp.models import MediaUser, PreferenceSubCategory, UserDevicePref
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MediaUser
        fields = ('username', 'phone_number', 'email', 'address', 'date_joined')


class PreferenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PreferenceSubCategory
        fields = ('name', 'values')
        
class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserDevicePref
        fields = ('device_tag', 'device_type', 'device_info')