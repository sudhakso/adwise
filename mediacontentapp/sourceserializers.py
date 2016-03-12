import datetime
from rest_framework_mongoengine import serializers
from userapp.serializers import UserSerializer

from mediacontentapp.models import MediaSource, OOHMediaSource,\
        VODMediaSource, DigitalMediaSource, RadioMediaSource, Pricing,\
        Booking, MediaDashboard, MediaSourceActivity, SourceTag
from datetime import timedelta
from mediacontentapp.controller import ActivityManager


class MediaDashboardSerializer(serializers.DocumentSerializer):

    class Meta:
        model = MediaDashboard
        exclude = ('user',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    def update(self, instance, validated_data=None):
        today = datetime.datetime.now()
        in30days = today + timedelta(days=30)
        if instance:
            user = instance.user
            # Get all media source for the user
            if user:
                # Media owner
                if instance.dashboard_type == 'MEDIA_OWNER':
                    # All sources owned by Owner
                    A = OOHMediaSource.objects(
                                        owner=user, enabled=True)
                    instance.sources_owned = [str(source.id) for source in A]
                    # All sources sure shot available
                    A_a = OOHMediaSource.objects.filter(
                                            owner=user, booking=None, enabled=True)
                    # All past/future/current booked instances
                    B = [source for source in A if source not in A_a]
                    # All expired bookings
                    B_e = [source for source in
                           B if source.booking.end_time < today]
                    # All future bookings (> 1 day)
                    B_f = [source for source in
                           B if source.booking.start_time > in30days]
                    # Booked but available now within 30 days
                    B_a = list(set(B_e).union(B_f))
                    # Availability final
                    A_f = list(set([source for source in A_a]).union(B_a))
                    instance.available_source = [str(source.id) for source in
                                                 A_f]
                    # Booking future Expiring in < 30 days
                    B_f_e = [source for source in B if source not in A_f and
                             source.booking.end_time < in30days]
                    instance.free_within_month = [str(source.id) for source in
                                                  B_f_e]
                    # Activity tracking counters
                    instance.shared = len(MediaSourceActivity.objects.filter(
                                        interacting_user=user,
                                        activity_type=ActivityManager.get_activity_id(
                                                                    "share")))
                    # Update dash board instance
                    instance.save()
                    return instance
                # Media browser
                elif instance.dashboard_type == 'MEDIA_BROWSER':
                    # All MB fields
                    # Enumerate sources
                    N = []
                    # Get all sources known
                    A = OOHMediaSource.objects.filter(enabled=True)
                    # Get sure shot available
                    A_a = OOHMediaSource.objects.filter(
                                                    booking=None, enabled=True)
                    # All past/future/current booked instances
                    B = [source for source in A if source not in A_a]
                    # All expired bookings
                    B_e = [source for source in
                           B if source.booking.end_time < today]
                    # All future bookings (> today)
                    B_f = [source for source in
                           B if source.booking.start_time > in30days]
                    # Booked but available now within 30 days
                    B_a = list(set(B_e).union(B_f))
                    # Availability final
                    A_f = list(set([source for source in A_a]).union(B_a))
                    instance.available_source = [str(source.id) for source in
                                                 A_f]
                    for source in A_f:
                        last7days = today - timedelta(days=7)
                        if source.created_time > last7days:
                            N.append(str(source.id))
                    instance.new_additions = N
                    # Get shared counter
                    most_shared_recently = []
                    shared = MediaSourceActivity.objects.filter(
                                activity_type=ActivityManager.get_activity_id(
                                                            "share"))
                    for share in shared:
                        if share.activity_time > last7days:
                            most_shared_recently.append(
                                                str(share.mediasource.id))
                    instance.most_shared_source = list(set(
                        most_shared_recently)) if most_shared_recently else None
                    # Get liked counter
                    most_liked_recently = []
                    liked = MediaSourceActivity.objects.filter(
                                activity_type=ActivityManager.get_activity_id(
                                                                "like"))
                    for like in liked:
                        if like.activity_time > last7days:
                            most_liked_recently.append(
                                                str(like.mediasource.id))
                    instance.most_liked_source = list(set(
                        most_liked_recently)) if most_liked_recently else None
                    # Get viewed counter
                    most_viewed_recently = []
                    viewed = MediaSourceActivity.objects.filter(
                                activity_type=ActivityManager.get_activity_id("view"))
                    for view in viewed:
                        if view.activity_time > last7days:
                            most_viewed_recently.append(
                                                str(view.mediasource.id))
                    instance.most_viewed_source = list(set(
                        most_viewed_recently)) if most_viewed_recently else None
                    # Save finally.
                    instance.save()
                    return instance
                elif instance.dashboard_type == 'partner':
                    # on boarding partner
                    # TBD
                    pass
                else:
                    # in-efficient, but get everything. e.g serviceuser
                    # TBD
                    pass
                return instance


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
        exclude = ('primary_image_content', 'enabled',)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class SourceTagSerializer(serializers.DocumentSerializer):

    class Meta:
        model = SourceTag
        exclude = ('source_ref',)

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


class MediaSourceActivitySerializer(serializers.DocumentSerializer):

    class Meta:
        model = MediaSourceActivity
        exclude = ('interacting_user', 'mediasource')

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

