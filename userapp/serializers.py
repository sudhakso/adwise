from userapp.models import MediaUser,\
 PreferenceSubCategory, UserDevicePref, UserService, ServiceRequest,\
 UserCreateRequest, Project
from rest_framework_mongoengine import serializers


class ProjectSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Project

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


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


class UserCreateRequestSerializer(serializers.DocumentSerializer):
    user = UserSerializer()
    project = ProjectSerializer(required=False)

    class Meta:
        model = UserCreateRequest

    def create(self, validated_data):
        proj = None
        # Save the project if mentioned
        if 'project' in validated_data:
            proj = Project(**validated_data['project'])
        if 'user' in validated_data:
            user = MediaUser(project_id=proj, **validated_data['user'])
        if user:
            # If project is given, the user is marked as admin
            # for the project.
            # Else, it is a normal user
            if proj:
                proj.save()
                user.save(is_admin=True)
            else:
                user.save()
        return UserCreateRequest(project=proj, user=user)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)
