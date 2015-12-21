from mediacontentapp.models import Ad, TextAd, ProductAd, DynamicSearchAd,\
    Campaign, ImageContent
from mediacontentapp.models import CallOnlyAd, ImageAd
from mediacontentapp.models import LocationExtension, BusinessHoursExtension
from rest_framework_mongoengine import serializers


class CampaignSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Campaign
        fields = ('id', 'name', 'description', 'creation_time', 'launched_at',
                  'end_at')

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


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
        exclude = ('image_content',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class ImageContentSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ImageContent

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
