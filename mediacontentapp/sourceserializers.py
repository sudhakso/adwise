from datetime import datetime
from rest_framework_mongoengine import serializers
from userapp.serializers import UserSerializer
from datetime import timedelta
from mediacontentapp import ActivityManager
from userapp.models import MediaUser
from mediacontentapp.models import MediaDashboard, SourceTag, Booking,\
    Pricing, OOHOperationalDailyDataFeed, OOHAnalyticalAttributes,\
    MediaSource, OOHMediaSource, DigitalMediaSource, VODMediaSource,\
    RadioMediaSource, MediaSourceActivity, MediaContentActivity, MediaAggregate,\
    MediaAggregateType, Amenity, AmenityExtension, AmenityExtensionCollection,\
    RetailExtension, SpecialInterestExtension, SpecialityClinicExtension,\
    EmergencyServiceExtension, OPDServiceExtension, PlayingAracadeExtension,\
    StayingExtension, Sensor, SensorActivity, Venue, DoctorExtension,\
    PharmacyExtension, HelpdeskExtension, MultiplexExtension, OnlineMediaSource,\
    FloatingMediaSource, WiFi, Beacon, BrandExtension, FNBExtension, FacilityExtension,\
    AdventureSportExtension


class MediaDashboardSerializer(serializers.DocumentSerializer):

    class Meta:
        model = MediaDashboard
        exclude = ('user',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    def update(self, instance, validated_data=None):
        today = datetime.now()
        if instance:
            user = instance.user
            # Get all media source for the user
            if user:
                # Media owner
                if instance.dashboard_type == 'MEDIA_OWNER':
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
                    # Activity tracking counters
                    shared = len(MediaSourceActivity.objects.filter(
                                interacting_user=user,
                                activity_type=ActivityManager.get_activity_id(
                                                                    "share")))

                    # Update dash board instance
                    instance.update(
                            sources_owned=sourceidlist,
                            available_source=available_sourceid_list,
                            free_within_month=expiring_in30days_sources_id,
                            num_shared=shared)
                    instance.save()
                # Media browser
                elif instance.dashboard_type == 'MEDIA_BROWSER':
                    # All MB fields
                    # Enumerate sources
                    new_sources = []
                    available_sources = OOHMediaSource.objects.filter(
                                                            booking=None)
                    available_sourceid_list = [
                            str(source.id) for source in available_sources]
                    for source in available_sources:
                        last7days = today - timedelta(days=7)
                        if source.created_time > last7days:
                            new_sources.append(str(source.id))
                    # Get shared counter
                    most_shared_recently = []
                    shared = MediaSourceActivity.objects.filter(
                                activity_type=ActivityManager.get_activity_id("share"))
                    for share in shared:
                        if share.activity_time > last7days:
                            most_shared_recently.append(
                                                str(share.mediasource.id))
                    # Get liked counter
                    most_liked_recently = []
                    liked = MediaSourceActivity.objects.filter(
                                activity_type=ActivityManager.get_activity_id("like"))
                    for like in liked:
                        if like.activity_time > last7days:
                            most_liked_recently.append(
                                                str(like.mediasource.id))
                    # Get viewed counter
                    most_viewed_recently = []
                    viewed = MediaSourceActivity.objects.filter(
                                activity_type=ActivityManager.get_activity_id("view"))
                    for view in viewed:
                        if view.activity_time > last7days:
                            most_viewed_recently.append(
                                                str(view.mediasource.id))
                    # Update dash board instance
                    instance.update(
                            most_viewed_source=most_viewed_recently,
                            most_liked_source=most_liked_recently,
                            most_shared_source=most_shared_recently,
                            new_additions=new_sources,
                            premium_source=[],
                            available_source=available_sourceid_list)
                    # Save finally. Do we need?
                    instance.save()
                    pass
                elif instance.dashboard_type == 'partner':
                    # on boarding partner
                    # TBD
                    pass
                else:
                    # in-efficient, but get everything. e.g serviceuser
                    # TBD
                    pass
                return instance


class SourceTagSerializer(serializers.DocumentSerializer):
    class Meta:
        model = SourceTag

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


class OOHOperationalDailyDataFeedSerializer(serializers.DocumentSerializer):

    class Meta:
        model = OOHOperationalDailyDataFeed
        fields = ('visitor_total_count', 'breakups', 'feed_timestamp',  'trusted_source',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class OOHAnalyticalAttributesSerializer(serializers.DocumentSerializer):
    class Meta:
        model = OOHAnalyticalAttributes

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

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class OOHMediaSourceSerializer(serializers.DocumentSerializer):
    # Owner details
    verified_by = UserSerializer(required=False, read_only=True)
    owner = UserSerializer(required=False, read_only=True)
    operated_by = UserSerializer(required=False, read_only=True)
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
    # Owner details
    verified_by = UserSerializer(required=False, read_only=True)
    owner = UserSerializer(required=False, read_only=True)
    operated_by = UserSerializer(required=False, read_only=True)
    
    class Meta(MediaSourceSerializer.Meta):
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


class MediaSourceActivitySerializer(serializers.DocumentSerializer):

    class Meta:
        model = MediaSourceActivity
        exclude = ('interacting_user', 'mediasource')

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class MediaContentActivitySerializer(serializers.DocumentSerializer):
    interacting_user = UserSerializer(required=False, read_only=True)

    class Meta:
        model = MediaContentActivity
        exclude = ('campaign', 'ad', 'offer')

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class MediaAggregateTypeSerializer(serializers.DocumentSerializer):

    class Meta:
        model = MediaAggregateType
        exclude = ('typeicon_image_url', 'typeicon_content')

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class MediaAggregateSerializer(serializers.DocumentSerializer):
    # Serializes amenity
    inhouse_source = DigitalMediaSourceSerializer(required=False,
                                                  read_only=True)
    digital_sourcelist = DigitalMediaSourceSerializer(required=False,
                                                      read_only=True,
                                                      many=True)
    ooh_sourcelist = OOHMediaSourceSerializer(required=False,
                                              read_only=True,
                                              many=True)
    radio_sourcelist = RadioMediaSourceSerializer(required=False,
                                                  read_only=True,
                                                  many=True)
    typespec = MediaAggregateTypeSerializer(required=False, read_only=True)

    owner = UserSerializer(required=False, read_only=True)

    class Meta:
        model = MediaAggregate
        exclude = ('icon_content', 'image_content',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class AmenitySerializer(serializers.DocumentSerializer):
    class Meta:
        model = Amenity

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class AmenityExtensionSerializer(serializers.DocumentSerializer):

#     amenityref = MediaAggregateSerializer(required=False, read_only=True)
#     userref = UserSerializer(required=False, read_only=True)

    class Meta:
        model = AmenityExtension
        exclude = ('image', 'userref', 'amenityref',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class RetailExtensionSerializer(serializers.DocumentSerializer):

#     amenityref = MediaAggregateSerializer(required=False, read_only=True)
#     userref = UserSerializer(required=False, read_only=True)

    class Meta:
        model = RetailExtension
        exclude = ('image', 'userref', 'amenityref',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class BrandExtensionSerializer(serializers.DocumentSerializer):

#     amenityref = MediaAggregateSerializer(required=False, read_only=True)
#     userref = UserSerializer(required=False, read_only=True)

    class Meta:
        model = BrandExtension
        exclude = ('image', 'userref', 'amenityref',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class FNBExtensionSerializer(serializers.DocumentSerializer):

#     amenityref = MediaAggregateSerializer(required=False, read_only=True)
#     userref = UserSerializer(required=False, read_only=True)

    class Meta:
        model = FNBExtension
        exclude = ('image', 'userref', 'amenityref',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class DoctorExtensionSerializer(serializers.DocumentSerializer):

#     amenityref = MediaAggregateSerializer(required=False, read_only=True)
#     userref = UserSerializer(required=False, read_only=True)

    class Meta:
        model = DoctorExtension
        exclude = ('image', 'userref', 'amenityref',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class SpecialityClinicExtensionSerializer(serializers.DocumentSerializer):

#     amenityref = MediaAggregateSerializer(required=False, read_only=True)
#     userref = UserSerializer(required=False, read_only=True)

    class Meta:
        model = SpecialityClinicExtension
        exclude = ('image', 'userref', 'amenityref',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class PharmacyExtensionSerializer(serializers.DocumentSerializer):

#     amenityref = MediaAggregateSerializer(required=False, read_only=True)
#     userref = UserSerializer(required=False, read_only=True)

    class Meta:
        model = PharmacyExtension
        exclude = ('image', 'userref', 'amenityref',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class FacilityExtensionSerializer(serializers.DocumentSerializer):

#     amenityref = MediaAggregateSerializer(required=False, read_only=True)
#     userref = UserSerializer(required=False, read_only=True)

    class Meta:
        model = FacilityExtension
        exclude = ('image', 'userref', 'amenityref',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class EmergencyServiceExtensionSerializer(serializers.DocumentSerializer):

#     amenityref = MediaAggregateSerializer(required=False, read_only=True)
#     userref = UserSerializer(required=False, read_only=True)

    class Meta:
        model = EmergencyServiceExtension
        exclude = ('image', 'userref', 'amenityref',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class opdServiceExtensionSerializer(serializers.DocumentSerializer):

#     amenityref = MediaAggregateSerializer(required=False, read_only=True)
#     userref = UserSerializer(required=False, read_only=True)

    class Meta:
        model = OPDServiceExtension
        exclude = ('image', 'userref', 'amenityref',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class HelpdeskExtensionSerializer(serializers.DocumentSerializer):

#     amenityref = MediaAggregateSerializer(required=False, read_only=True)
#     userref = UserSerializer(required=False, read_only=True)

    class Meta:
        model = HelpdeskExtension
        exclude = ('image', 'userref', 'amenityref',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class AdventureSportExtensionSerializer(serializers.DocumentSerializer):

#     amenityref = MediaAggregateSerializer(required=False, read_only=True)
#     userref = UserSerializer(required=False, read_only=True)

    class Meta:
        model = AdventureSportExtension
        exclude = ('image', 'userref', 'amenityref',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class SpecialInterestExtensionSerializer(serializers.DocumentSerializer):

#     amenityref = MediaAggregateSerializer(required=False, read_only=True)
#     userref = UserSerializer(required=False, read_only=True)

    class Meta:
        model = SpecialInterestExtension
        exclude = ('image', 'userref', 'amenityref',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class StayingExtensionSerializer(serializers.DocumentSerializer):

#     amenityref = MediaAggregateSerializer(required=False, read_only=True)
#     userref = UserSerializer(required=False, read_only=True)

    class Meta:
        model = StayingExtension
        exclude = ('image', 'userref', 'amenityref',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class MultiplexExtensionSerializer(serializers.DocumentSerializer):

#     amenityref = MediaAggregateSerializer(required=False, read_only=True)
#     userref = UserSerializer(required=False, read_only=True)

    class Meta:
        model = MultiplexExtension
        exclude = ('image', 'userref', 'amenityref',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class AmenityExtensionCollectionSerializer(serializers.DocumentSerializer):
    retails = RetailExtensionSerializer(required=False,
                                        read_only=True,
                                        many=True)
    brands = BrandExtensionSerializer(required=False,
                                      read_only=True,
                                      many=True)
    fnbs = FNBExtensionSerializer(required=False,
                                  read_only=True,
                                  many=True)

    class Meta:
        model = AmenityExtensionCollection
        exclude = ('id',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


# Serializer for indexing ooh mediasource
class OOHMediaSourceIndexSerializer(serializers.DocumentSerializer):

    class Meta:
        model = OOHMediaSource
        fields = ('id',
                  'name',
                  'display_name',
                  'caption',
                  'tags',
                  'street_name',
                  'city',
                  'state',
                  'country',
                  'pin',
                  'point')

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class OnlineMediaSourceSerializer(serializers.DocumentSerializer):
    # Owner details
    verified_by = UserSerializer(required=False, read_only=True)
    owner = UserSerializer(required=False, read_only=True)
    operated_by = UserSerializer(required=False, read_only=True)

    class Meta:
        model = OnlineMediaSource

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class FloatingMediaSourceSerializer(serializers.DocumentSerializer):
    # Owner details
    verified_by = UserSerializer(required=False, read_only=True)
    owner = UserSerializer(required=False, read_only=True)
    operated_by = UserSerializer(required=False, read_only=True)

    class Meta:
        model = FloatingMediaSource

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class SensorSerializer(serializers.DocumentSerializer):

    # Owner details
#     verified_by = UserSerializer(required=False, read_only=True)
#     operated_by = UserSerializer(required=False, read_only=True)
    owner = UserSerializer(required=False, read_only=True)

    class Meta:
        model = Sensor
        exclude = ('venue', 'verified_by', 'operated_by')

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class VenueSerializer(serializers.DocumentSerializer):

    source = MediaSourceSerializer(required=False, read_only=True)
    sensors = SensorSerializer(required=False, read_only=True, many=True)

    class Meta:
        model = Venue

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class BeaconSerializer(serializers.DocumentSerializer):

    # Owner details
    verified_by = UserSerializer(required=False, read_only=True)
    owner = UserSerializer(required=False, read_only=True)
    operated_by = UserSerializer(required=False, read_only=True)
    venue = VenueSerializer(required=False, read_only=True)

    class Meta:
        model = Beacon

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class WiFiSerializer(serializers.DocumentSerializer):

    # Owner details
    verified_by = UserSerializer(required=False, read_only=True)
    owner = UserSerializer(required=False, read_only=True)
    operated_by = UserSerializer(required=False, read_only=True)

    class Meta:
        model = WiFi

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class SensorActivitySerializer(serializers.DocumentSerializer):

    interacting_user = UserSerializer(required=False, read_only=True)
    sensor = SensorSerializer(required=False, read_only=True)

    class Meta:
        model = SensorActivity

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)
