from mediacontentapp.models import Ad, TextAd, ProductAd, DynamicSearchAd,\
    Campaign, ImageContent, JpegImageContent, CampaignSpec, CampaignTracking,\
    MediaAggregate
from mediacontentapp.models import CallOnlyAd, ImageAd
from mediacontentapp.models import AdExtension,\
    LocationExtension, BusinessHoursExtension,\
    OfferExtension, SocialExtension, T_C_Extension,\
    Period, Playing
from rest_framework_mongoengine import serializers
from rest_framework.serializers import ListSerializer


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
        exclude = ('creator', 'image_content',)
#         fields = ('id', 'spec', 'name', 'description', 'creation_time',
#                   'launched_at', 'end_at', 'geo_tags', 'enabled', 'city',
#                   'state', 'country', 'state', 'target_group',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


# Serializer for indexing campaign
class CampaignIndexSerializer(serializers.DocumentSerializer):

    class Meta:
        model = Campaign
        fields = ('id',
                  'name',
                  'description',
                  'launched_at',
                  'end_at',
                  'geo_tags',
                  'city',
                  'state',
                  'country',
                  'tags',
                  'category')

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class ImageAdIndexSerializer(serializers.DocumentSerializer):

    class Meta:
        model = ImageAd
        fields = ('id',
                  'ad_type',
                  'ad_location_tag')

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class OfferIndexSerializer(serializers.DocumentSerializer):

    class Meta:
        model = OfferExtension
        fields = ('id',
                  'offer_type',
                  'offer_code',
                  'offer_description')

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


# Serializer for indexing campaign
class MediaAggregateIndexSerializer(serializers.DocumentSerializer):

    class Meta:
        model = MediaAggregate
        fields = ('id',
                  'name',
                  'display_name',
                  'survey_name',
                  'address1',
                  'address2',
                  'city',
                  'state',
                  'country',
                  'location')

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class CampaignTrackingSerializer(serializers.DocumentSerializer):
    campaign = CampaignSerializer(required=False, read_only=True)
    class Meta:
        model = CampaignTracking

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class OfferExtensionSerializer(serializers.DocumentSerializer):

    class Meta:
        model = OfferExtension

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class SocialMediaExtensionSerializer(serializers.DocumentSerializer):

    class Meta:
        model = SocialExtension

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class T_C_ExtensionSerializer(serializers.DocumentSerializer):

    class Meta:
        model = T_C_Extension

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


class AdSerializer(serializers.DocumentSerializer):
#    campaign = CampaignSerializer(required=False, read_only=True)
#     offerex = OfferExtensionSerializer(required=False,
#                                        read_only=True,
#                                        many=True)
#     socialex = SocialMediaExtensionSerializer(required=False,
#                                               read_only=True,
#                                               many=True)

    class Meta:
        model = Ad
        fields = ('url', 'display_url', 'final_urls', 'mobile_urls',
                  'app_urls', 'thirdparty_tracking_url', 'adwise_tracking_url',
                  'ad_type', 'custom_parameters', 'device_preference',
                  'campaign', 'offerex', 'socialex',)

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
    campaign = CampaignSerializer(required=False, read_only=True)
    offerex = OfferExtensionSerializer(required=False,
                                       many=True,
                                       read_only=True)
    socialex = SocialMediaExtensionSerializer(required=False,
                                              many=True,
                                              read_only=True)

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


class AdExtensionSerializer(serializers.DocumentSerializer):
    class Meta:
        model = AdExtension

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


class PeriodSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Period

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class PlayingSerializer(serializers.DocumentSerializer):

    playing_content = CampaignSerializer(required=False, read_only=True)

    class Meta:
        model = Playing
#         exclude = ('primary_media_source',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)
