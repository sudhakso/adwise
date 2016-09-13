from mediaresearchapp.models import ResearchResult,\
    SearchQuery, CampaignResearchResult, MediaAggregateResearchResult,\
    StructuredQuery
from rest_framework_mongoengine import serializers
from mediacontentapp.serializers import CampaignSerializer
from mediacontentapp.sourceserializers import OOHMediaSourceSerializer,\
  MediaAggregateSerializer


class MediaAggregateResearchResultSerializer(serializers.DocumentSerializer):
    amenties = MediaAggregateSerializer(many=True, read_only=True)

    class Meta:
        model = MediaAggregateResearchResult

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class CampaignResearchResultSerializer(serializers.DocumentSerializer):
    campaigns = CampaignSerializer(many=True, read_only=True)

    class Meta:
        model = CampaignResearchResult

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class ResearchResultSerializer(serializers.DocumentSerializer):
    campaigns = CampaignSerializer(many=True, read_only=True)
    oohs = OOHMediaSourceSerializer(many=True, read_only=True)
    mediaaggregates = MediaAggregateSerializer(many=True, read_only=True)

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


class StructuredQuerySerializer(serializers.DocumentSerializer):
    class Meta:
        model = StructuredQuery

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)
