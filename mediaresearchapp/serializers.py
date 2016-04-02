from mediacontentapp.models import Ad, TextAd, ProductAd, DynamicSearchAd,\
    Campaign, ImageContent, JpegImageContent, CampaignSpec, CampaignTracking
from mediaresearchapp.models import ResearchElement, ResearchResult,\
    SearchQuery
from rest_framework_mongoengine import serializers


class ResearchElementSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ResearchElement

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class ResearchResultSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ResearchResult

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class SearchQuerySerializer(serializers.DocumentSerializer):
    class Meta:
        model = SearchQuery

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)
