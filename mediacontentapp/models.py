from mongoengine.fields import GeoPointField, DictField, ListField,\
    StringField, URLField, BooleanField, DateTimeField, FloatField,\
    ReferenceField, ImageField, FileField
# from django_mongodb_engine.fields import GridFSField
from mongoengine.document import Document
from mongoengine import connect
from atlas_ws.settings import _MONGODB_NAME
from rest_framework import fields
from rest_framework.fields import IntegerField
from datetime import datetime
from django_mongodb_engine.storage import GridFSStorage
from django.db.models.base import get_absolute_url

connect(_MONGODB_NAME, alias='default')
# gridfs = GridFSStorage(location='/uploads')


# Create your models here.
class Campaign(Document):
    """
    Campaign resource
    """
    name = StringField()
    description = StringField()
    # TBD (FixMe): Media Agency user should be added different
    creator = ReferenceField('MediaUser')
    creation_time = DateTimeField(default=datetime.now())
    launched_at = DateTimeField()
    end_at = DateTimeField()

    def get_absolute_url(self):
        return "/campaign/%i/" % self.id


class SourceAdDetails(Document):
    """
    Monikers for the source of Ad. Example, the promoter details.
    (Angadi Silks, kent.co.in etc.)
    """
    pass


class AmenityType(Document):
    """
    pre-defined amenity.
    Rating system could consider amenity.
    """
    # pre-known types of amenity
    typename = StringField()
    weight = FloatField()


class Amenity(Document):
    """
    Location specific amenities.
    Rating system could consider amenity.
    """
    # public roads, Community hall, leisure,
    type = ReferenceField('AmenityType')
    # Ring road, marriage, snack bar
    classifier = StringField()
    name = StringField(primary_key=True)
    rating = FloatField()


class MediaSource(Document):
    """
    Different types of media we integrate our solution with.
    """
    name = StringField()
    description = StringField()
    type = StringField()
    active = BooleanField()
    date_joined = DateTimeField()
    leased_by = StringField()
    leased_to = StringField()
    last_activity = DateTimeField()

    meta = {'allow_inheritance': True}

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return "/mediasource/%i/" % self.id


class OOHMediaSource(MediaSource):
    """
    Out of house advertising media type.
    """
    type = 'ooh'
    point = GeoPointField()
    min_viewing_distance = FloatField()
    avg_viewership = FloatField()
    street_name = StringField()
    city = StringField()
    state = StringField()
    country = StringField()
    pin = StringField()

    specials = ListField(ReferenceField('Amenity'))
    content = ListField(ReferenceField('Playing'))

    def get_absolute_url(self):
        return "/mediasource/ooh/%i/" % self.id


class DigitalMediaSource(MediaSource):
    """
    Digital media inside home advertising media type.
    For example, Televisions, DTH etc.
    """
    type = 'digital'
    # DTH:Aritel
    broadcaster_name = StringField()
    tune_number = FloatField()
    tune_name = StringField()
    broadcaster_url = URLField()
    broadcaster_api_url = URLField()
    broadcaster_api_key = StringField()

    def get_absolute_url(self):
        return "/mediasource/digital/%i/" % self.id


class VODMediaSource(MediaSource):
    """
    Digital media inside home but IP based advertising media type.
    For example, VoD service from sky etc.
    """
    type = 'vod'

    def get_absolute_url(self):
        return "/mediasource/vod/%i/" % self.id


class RadioMediaSource(MediaSource):
    """
    Advertising media type using Radio waves technology.
    For example, FM radio, AM radio etc.
    """
    type = 'radio'

    def get_absolute_url(self):
        return "/mediasource/radio/%i/" % self.id


class Playing(Document):
    """
    At a given time, a media source plays an advertisement
    for a sourceAdDetail. The time is captured as start and end,
    where the relationship is valid.
    This class realizes such relationship.
    """

    media_source = ReferenceField('MediaSource')
    media_content = ReferenceField('Ad')
    media_type = StringField()
    start_date = DateTimeField()
    end_date = DateTimeField()


class Period(Document):
    """
    Information to capture period of operation.
    """
    openDay = StringField()
    openTime = StringField()
    closeTime = StringField()
    closeDay = StringField()


class AdExtension(Document):
    """
    Each Advertisement impression can be supplemented using
    different extension types. And it is purely based on the
    intended type of Ad.
    For example, adding a location or call details in a Ad
    impression.
    """
    ex_name = StringField()
    ex_type = StringField()
    # meta
    meta = {'allow_inheritance': True}

    class Meta:
        abstract = True


class Ad(Document):
    """
    Advertisement impression on Users mobile device.
    Represents the base class for possible advertisement
    impression types.
    """
    url = URLField()
    display_url = URLField()

    # Collection of product urls
    final_urls = ListField()
    mobile_urls = ListField()
    app_urls = ListField()

    # Customer trusted tracking
    thirdparty_tracking_url = URLField()

    # AdWise tracking
    adwise_tracking_url = URLField()

    # Meta
    ad_type = StringField()
    custom_parameters = DictField()
    device_preference = IntegerField()

    # Campaign this Ad refers to.
    campaign = ReferenceField(Campaign)
    # List of extension
    extenstions = ListField(ReferenceField('AdExtension'))

    # reference - DRF field
    url = fields.URLField(source='get_absolute_url', read_only=False)

    # meta
    meta = {'allow_inheritance': True}

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return "/mediacontent/ads/%i/" % self.id

"""
The standard type of Ad.
Includes a link to your website and a description
or promotion of your product or service.
"""


class TextAd(Ad):
    """
    The standard type of Ad.
    Includes a link to your website and a description
    or promotion of your product or service.
    """

    headline = StringField(max_length=2048)
    description1 = StringField()
    description2 = StringField()

    ad_type = StringField(default='TextAd')
    # reference - DRF field
    url = fields.URLField(source='get_absolute_url', read_only=False)

    def get_absolute_url(self):
        return "/mediacontent/ads/textads/%i/" % self.id


class ProductAd(Ad):

    """
    A product ad based on product data
    of a Shopping campaign's associated Merchant Center
    account.
    """
    # Promotional line for this ad.
    # This text will be displayed in addition to the products.
    promotionLine = StringField()
    ad_type = StringField(default='ProductAd')

    # reference - DRF field
    url = fields.URLField(source='get_absolute_url', read_only=False)

    def get_absolute_url(self):
        return "/mediacontent/ads/productads/%i/" % self.id


class DynamicSearchAd(Ad):
    """
    Dynamically generated search ads based on the content
    of a web site.
    """
    # All fields are filled dynamically.
    # Simple variation of base class 'Ad'.
    ad_type = StringField(default='DynamicSearchAd')
    # reference - DRF field
    url = fields.URLField(source='get_absolute_url', read_only=False)

    def get_absolute_url(self):
        return "/mediacontent/ads/dynamicsearchads/%i/" % self.id


class CallOnlyAd(Ad):
    """
    An ad for a Click to Call Only Campaign.
    """
    # Call'able parameters
    countryCode = StringField()
    phone_number = StringField()
    business_name = StringField()
    # Enable call tracking by parameters
    callTracked = BooleanField()
    # Parameters measures, count, call length
    callTrackParameters = DictField()
    # Phone number verification
    phonenumberVerificationUrl = URLField()

    ad_type = StringField(default='CallOnlyAd')

    def get_absolute_url(self):
        return "/mediacontent/ads/callonlyads/%i/" % self.id


class ImageContent(Document):
    """
    An image instance .
    """

    image_type = StringField(default='jpg')
    image = ImageField()

    def get_absolute_url(self):
        return "/mediacontent/ads/imageads/images/%s/" % (
                                        self.id)


class ImageAd(Ad):
    """
    An ad that includes a graphic to promote
    your business.
    """
    ad_type = StringField(default='ImageAd')
    image_url = StringField()
    image_content = ReferenceField('ImageContent')

    def get_absolute_url(self):
        return "/mediacontent/ads/imageads/%i/%i/" % (
                                        self.campaign.id, self.id)


class MobileAd(Ad):
    """
    Contains a click-to-call phone number,
    a link to a website, or both.
    """
    ad_type = StringField(default='MobileAd')

    def get_absolute_url(self):
        return "/mediacontent/ads/mobileads/%i/" % self.id


class TemplateAd(Ad):
    """
    An ad based on a predefined template.
    """
    ad_type = StringField(default='TemplateAd')

    def get_absolute_url(self):
        return "/mediacontent/ads/templateads/%i/" % self.id


class LocationExtension(AdExtension):
    """
    This extension add locations to the advertisement
    impression.
    """
    locationName = StringField()
    locationCode = StringField()
    locationPrimaryPhone = StringField()
    locationPrimaryCategory = StringField()
    locationtWebsiteUrl = URLField()
    locationAddresslines = ListField()
    locationAddressLocality = StringField()
    locationAdministrativeArea = StringField()
    locationCountry = StringField()
    locationPostalCode = StringField()
    # optional
    locationcode = GeoPointField()

    def get_absolute_url(self):
        return "/mediacontent/ext/locationextensions/%i/" % self.id


class BusinessHoursExtension(AdExtension):
    """
    This extension adds business working hours to the
    advertisement impression.
    """
    periods = ListField(ReferenceField(Period))
    days = ListField()

    def get_absolute_url(self):
        return "/mediacontent/ext/businesshoursextensions/%i/" % self.id


class ReviewExtension(AdExtension):
    """
    This extension adds user review extension to the
    advertisement impression.
    """
    pass


class SiteLinkExtension(AdExtension):
    pass


class AppExtension(AdExtension):
    """
    This extension adds mobile app to the
    advertisement impression.
    """
    pass


class OfferExtension(AdExtension):
    """
    This extension adds coupons and offers extension to the
    advertisement impression.
    """
    pass
