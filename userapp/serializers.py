from userapp.models import MediaUser, PreferenceSubCategory, UserDevicePref
#from rest_framework import serializers
from rest_framework_mongoengine import serializers

class UserSerializer(serializers.DocumentSerializer):
    class Meta:
        model = MediaUser
        concrete_model = MediaUser
        fields = ('username', 'phone_number', 'email', 'city', 'state', 'password', 'address', 'point')
        geo_point = "point"
    
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)
    
#     username = serializers.CharField(allow_blank=False, required=True, max_length=30)
#     password = serializers.CharField(allow_blank=False, required=True, max_length=30)
#     phone_number = serializers.CharField(allow_blank=False, required=True, max_length=30)
#     email = serializers.EmailField(allow_blank=False, required=True, max_length=80)
#     address = serializers.CharField(allow_blank=False, required=True, max_length=256)
#     city = serializers.CharField(allow_blank=False, required=True, max_length=80)
#     state = serializers.CharField(allow_blank=False, required=True, max_length=80)
#     point = serializers.DictField()     
#     date_joined = serializers.DateField()
#     last_updated = serializers.DateField()
#     last_activity = serializers.DateField()

    
class PreferenceSerializer(serializers.DocumentSerializer):
    class Meta:
        model = PreferenceSubCategory
        fields = ('name', 'values')
        
class DeviceSerializer(serializers.DocumentSerializer):
    class Meta:
        model = UserDevicePref
        fields = ('device_tag', 'device_type', 'device_info')