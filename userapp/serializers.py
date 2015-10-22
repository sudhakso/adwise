from userapp.models import MediaUser, PreferenceSubCategory, UserDevicePref
from rest_framework_mongoengine import serializers
from rest_framework import fields

class UserSerializer(serializers.DocumentSerializer):
#     url = fields.URLField(source='get_absolute_url', read_only=True)
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