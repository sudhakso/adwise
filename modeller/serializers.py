from rest_framework_mongoengine import serializers
from modeller.models import oohplanrequest, plannerresult
from mediacontentapp.sourceserializers import OOHMediaSourceSerializer,\
 MediaAggregateSerializer


class OOHPlanRequestSerializer(serializers.DocumentSerializer):
    class Meta:
        model = oohplanrequest

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class PlannerResultSerializer(serializers.DocumentSerializer):
    oohs = OOHMediaSourceSerializer(many=True, read_only=True)
    mediaaggregates = MediaAggregateSerializer(many=True, read_only=True)

    class Meta:
        model = plannerresult

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)
