from userapp.models import MediaUser,\
 PreferenceSubCategory, UserDevicePref, UserService, ServiceRequest
from rest_framework_mongoengine import serializers
from rest_framework import fields
from datetime import datetime


class UserSerializer(serializers.DocumentSerializer):
    class Meta:
        model = MediaUser
        geo_point = "point"

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class PreferenceSerializer(serializers.DocumentSerializer):
    class Meta:
        model = PreferenceSubCategory
        fields = ('name', 'values')


class DeviceSerializer(serializers.DocumentSerializer):
    class Meta:
        model = UserDevicePref
        fields = ('device_tag', 'device_type', 'device_info')


class UserServiceSerializer(serializers.DocumentSerializer):
    class Meta:
        model = UserService

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class ServiceRequestSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ServiceRequest

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)
