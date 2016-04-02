from mediacontentapp.models import Ad, TextAd, ProductAd, DynamicSearchAd,\
    Campaign, ImageContent, JpegImageContent, CampaignSpec, CampaignTracking
from mediacontentapp.models import CallOnlyAd, ImageAd
from mediacontentapp.models import LocationExtension, BusinessHoursExtension
from rest_framework_mongoengine import serializers


class CampaignSpecSerializer(serializers.DocumentSerializer):
    class Meta:
        model = CampaignSpec

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class CampaignSerializer(serializers.DocumentSerializer):
    spec = CampaignSpecSerializer(required=False, read_only=True)

    class Meta:
        model = Campaign
        exclude = ('creator',)
#         fields = ('id', 'spec', 'name', 'description', 'creation_time',
#                   'launched_at', 'end_at', 'geo_tags', 'enabled', 'city',
#                   'state', 'country', 'state', 'target_group',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class CampaignTrackingSerializer(serializers.DocumentSerializer):
    class Meta:
        model = CampaignTracking

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class AdSerializer(serializers.DocumentSerializer):
    campaign = CampaignSerializer(required=False, read_only=True)

    class Meta:
        model = Ad
        fields = ('url', 'display_url', 'final_urls', 'mobile_urls',
                  'app_urls', 'thirdparty_tracking_url', 'adwise_tracking_url',
                  'ad_type', 'custom_parameters', 'device_preference',
                  'campaign', 'extensions',)

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
    campaign = CampaignSerializer(required=False)

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


class JpegImageContentSerializer(serializers.DocumentSerializer):
    class Meta:
        model = JpegImageContent

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
