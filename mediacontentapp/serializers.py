from mediacontentapp.models import Ad, TextAd, ProductAd, DynamicSearchAd
from mediacontentapp.models import CallOnlyAd, ImageAd,MobileAd, TemplateAd
from mediacontentapp.models import LocationExtension, BusinessHoursExtension
from rest_framework_mongoengine import serializers
from rest_framework import fields


class AdSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Ad

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class TextAdSerializer(serializers.DocumentSerializer):
    class Meta:
        model = TextAd

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class ProductAdSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ProductAd

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class CallOnlyAdSerializer(serializers.DocumentSerializer):
    class Meta:
        model = CallOnlyAd

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class ImageAdSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ImageAd

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class MobileAdSerializer(serializers.DocumentSerializer):
    class Meta:
        model = MobileAd

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class DynamicSearchAdSerializer(serializers.DocumentSerializer):
    class Meta:
        model = DynamicSearchAd

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class LocationExtensionSerializer(serializers.DocumentSerializer):
    class Meta:
        model = LocationExtension

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class BusinessHoursExtensionSerializer(serializers.DocumentSerializer):
    class Meta:
        model = BusinessHoursExtension

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

