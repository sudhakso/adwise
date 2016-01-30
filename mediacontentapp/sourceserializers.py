from rest_framework_mongoengine import serializers
from userapp.serializers import UserSerializer

from mediacontentapp.models import MediaSource, OOHMediaSource,\
        VODMediaSource, DigitalMediaSource, RadioMediaSource


class MediaSourceSerializer(serializers.DocumentSerializer):
    verified_by = UserSerializer(required=False)
    owner = UserSerializer(required=False)
    operated_by = UserSerializer(required=False)
    
    class Meta:
        model = MediaSource
        fields = ('verified_by', 'owner', 'operated_by')

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class OOHMediaSourceSerializer(serializers.DocumentSerializer):
    verified_by = UserSerializer(required=False)
    owner = UserSerializer(required=False)
    operated_by = UserSerializer(required=False)
    
    class Meta:
        model = OOHMediaSource
        exclude = ('primary_image_content',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class DigitalMediaSourceSerializer(serializers.DocumentSerializer):

    class Meta:
        model = DigitalMediaSource

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class VODMediaSourceSerializer(serializers.DocumentSerializer):

    class Meta:
        model = VODMediaSource

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class RadioMediaSourceSerializer(serializers.DocumentSerializer):

    class Meta:
        model = RadioMediaSource

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)
