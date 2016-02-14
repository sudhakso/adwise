import datetime
from rest_framework_mongoengine import serializers
from userapp.serializers import UserSerializer

from mediacontentapp.models import MediaSource, OOHMediaSource,\
        VODMediaSource, DigitalMediaSource, RadioMediaSource, Pricing,\
        Booking, MediaDashboard, MediaActivity
from datetime import timedelta


class MediaDashboardSerializer(serializers.DocumentSerializer):

    class Meta:
        model = MediaDashboard
        exclude = ('user',)
#         fields = ('most_viewed_source', 'available_source', 'sources_owned',
#                   'free_within_month', 'created')

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    def update(self, instance, validated_data=None):
        today = datetime.datetime.now()
        if instance:
            user = instance.user
            # Get all media source for the user
            if user:
                sources = OOHMediaSource.objects(
                                        owner=user)
                sourceidlist = [str(source.id) for source in sources]
                # Enumerate sources
                available_sources = OOHMediaSource.objects.filter(
                                        owner=user, booking=None)
                available_sourceid_list = [
                        str(source.id) for source in available_sources]

                booked_sources = [source
                                  for source in sources if source not in
                                  available_sources]
                in30days = today + timedelta(days=30)
                expiring_in30days_sources_id = []
                for source in booked_sources:
                    source_end_time = source.booking.end_time
                    if source_end_time < in30days:
                        expiring_in30days_sources_id.append(str(source.id))
                # Update dash board instance
                instance.update(sources_owned=sourceidlist,
                                available_source=available_sourceid_list,
                                free_within_month=expiring_in30days_sources_id)
                instance.save()
                return instance


class MediaActivitySerializer(serializers.DocumentSerializer):
    class Meta:
        model = MediaActivity

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class BookingSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Booking

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class PricingSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Pricing

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


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
    # Owner details
    verified_by = UserSerializer(required=False)
    owner = UserSerializer(required=False)
    operated_by = UserSerializer(required=False)
    # SSP details
    pricing = PricingSerializer(required=False, read_only=True)
    booking = BookingSerializer(required=False, read_only=True)

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
