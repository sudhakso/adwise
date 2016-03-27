from userapp.models import MediaUser,\
 PreferenceSubCategory, UserDevicePref, UserService, ServiceRequest,\
 UserCreateRequest, Project, UserRole
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


class UserSerializer(serializers.DocumentSerializer):
    project_id = ProjectSerializer(required=False)
    role = UserRoleSerializer(required=False)

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
    role = UserRoleSerializer(required=False)

    class Meta:
        model = UserCreateRequest
        fields = ('user', 'project', 'role')

    def create(self, validated_data):
        proj = None
        role = None
        is_admin = False
        if 'role' in validated_data:
            role = UserRole(**validated_data['role'])
            role.save()
        # Save the project if mentioned
        if 'project' in validated_data:
            proj = Project(**validated_data['project'])
            proj.save()
        if 'user' in validated_data:
            user = MediaUser(project_id=proj, role=role,
                             **validated_data['user'])
            user.save()
        if user:
            # If project is given, the user is marked as admin
            # for the project.
            # Else, it is a normal user
            if proj:
                user.update(is_admin=is_admin, role=role)
                user.save()
 
        return UserCreateRequest(project=proj, user=user, role=role)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)
