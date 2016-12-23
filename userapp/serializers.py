from userapp.models import MediaUser,\
 UserMediaPref, UserService, ServiceRequest,\
 Project, UserRole, UserLocationPref,\
 Location, Offer, Event, Notification,\
 Cart, Meter, Service, Favourite
from userapp.models import UserPersonalPref, UserDevicePref
from rest_framework_mongoengine import serializers


class ProjectSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Project

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class UserRoleSerializer(serializers.DocumentSerializer):
    class Meta:
        model = UserRole

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class UserLocationPrefSerializer(serializers.DocumentSerializer):
    class Meta:
        model = UserLocationPref

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class UserDevicePrefSerializer(serializers.DocumentSerializer):
    class Meta:
        model = UserDevicePref

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class UserPersonalPrefSerializer(serializers.DocumentSerializer):
    class Meta:
        model = UserPersonalPref

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class UserMediaPrefSerializer(serializers.DocumentSerializer):
    class Meta:
        model = UserMediaPref

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class UserSerializer(serializers.DocumentSerializer):
    project_id = ProjectSerializer(read_only=True)
    role = UserRoleSerializer(read_only=True)
    device_pref = UserDevicePrefSerializer(many=True, read_only=True)
    personal_pref = UserPersonalPrefSerializer(many=True, read_only=True)
    media_pref = UserMediaPrefSerializer(many=True, read_only=True)
    loc_pref = UserLocationPrefSerializer(many=True, read_only=True)

    class Meta:
        model = MediaUser
        geo_point = "point"

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class DeviceSerializer(serializers.DocumentSerializer):
    class Meta:
        model = UserDevicePref
        fields = ('device_tag', 'device_type', 'device_info')


class ServiceSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Service

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class UserServiceSerializer(serializers.DocumentSerializer):
    service_id = ServiceSerializer(read_only=True)

    class Meta:
        model = UserService
        fields = ('id', 'service_id', 'enabled', 'last_report_time', 'auto_restart')

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class ServiceRequestSerializer(serializers.DocumentSerializer):
    user_ref = UserSerializer(read_only=True, required=False)
    service = UserServiceSerializer(read_only=True, required=False)

    class Meta:
        model = ServiceRequest

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class LocationSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Location

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class OfferSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Offer

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class EventSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Event

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class NotificationSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Notification

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class CartSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Cart

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class MeterSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Meter

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class FavouriteSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Favourite

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)
