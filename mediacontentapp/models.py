from mongoengine.fields import GeoPointField, DictField, ListField,\
    StringField, URLField, BooleanField, DateTimeField, FloatField,\
    ReferenceField, ImageField
# from django_mongodb_engine.fields import GridFSField
from mongoengine.document import Document
from rest_framework import fields
from rest_framework.fields import IntegerField
from datetime import datetime
from bson.json_util import default
# TBD (Filters don't work out of the box)
# import django_filters

#connect(_MONGODB_NAME, alias='default')
#connect(_MONGODB_NAME, host='192.168.71.133')

All = 'everyone'


# Create your models here.
class MediaDashboard(Document):
    """
    Media dash-board for the user
    """
    user = ReferenceField('MediaUser', required=False)
    # Possible values (billboard_owner, media_agency, onboarding_partner,
    # unknown)
    dashboard_type = StringField(required=False)
    # Common dash-board elements.
    # view and date counter
    most_liked_source = ListField(default=[], required=False)
    # activity and date counter
    most_viewed_source = ListField(default=[], required=False)
    # availability counter
    available_source = ListField(default=[], required=False)
    # share and date counter
    most_shared_source = ListField(default=[], required=False)
    # created date counter
    new_additions = ListField(default=[], required=False)
    # premium and date counter
    premium_source = ListField(default=[], required=False)
    # Ownership related
    sources_owned = ListField(default=[], required=False)
    free_within_month = ListField(default=[], required=False)
    num_shared = FloatField(default=0.0, required=False)

    created = DateTimeField(default=datetime.now(), required=False)
    last_updated = DateTimeField(default=datetime.now(), required=False)


class CampaignTracking(Document):
    """
    Campaign specification
    """
    name = StringField()
    description = StringField()
    language_code = StringField()
    # Will be auto-filled
    short_url = StringField(required=False)

    campaign = ReferenceField('Campaign', required=False)

    def get_absolute_url(self):
        return "/mediacontent/campaign/%i/track/%i" % (
                                    self.campaign.id, self.id)


class CampaignSpec(Document):
    """
    Campaign specification
    """
    name = StringField()
    # Unique type
    type = StringField()
    # TODO (Sonu): different types of source cannot be supported
    # Bring in source type field.
    linked_source_ids = ListField(default=[], required=False)
    # Type of Impression - imageads, textads, callads etc.
    ad_type = StringField(default='imageads', required=True)

    def get_absolute_url(self):
        return "/mediacontent/campaignspec/%i/" % self.id


class Campaign(Document):
    """
    Campaign resource
    """
    name = StringField()
    description = StringField()

    creator = ReferenceField('MediaUser')
    creation_time = DateTimeField(default=datetime.now())
    # These fields are not used and deprecated.
    launched_at = DateTimeField(default=datetime.now())
    end_at = DateTimeField(required=False)
    # TODO (Sonu:) Move them to extension
    city = ListField(default=[], required=False)
    state = ListField(default=[], required=False)
    country = ListField(default=[], required=False)
    target_group = ListField(default=[], required=False)

    # social media URL for the campaign
    social_url = StringField(required=False)
    home_url = StringField(required=False)

    # search'able tags
    tags = StringField(required=False)
    # UI assumes certain categories
    category = StringField(required=False)
    # Administrative control
    enabled = BooleanField(default=True, required=False)
    # TODO(Sonu): Why not generalize tags?
    # Tag
    geo_tags = ListField(default=[], required=False)
    # Home page image
    image_url = StringField(required=False)
    image_content = ReferenceField('ImageContent', required=False)
    # Specifications! Do we need a list of them?
    spec = ReferenceField('CampaignSpec', required=False)

    def get_absolute_url(self):
        return "/mediacontent/campaign/%i/" % self.id


class SourceAdDetails(Document):
    """
    Monikers for the source of Ad. Example, the promoter details.
    (Angadi Silks, kent.co.in etc.)
    """
    pass


class Subscription(Document):
    pass


class SourceTag(Document):
    """
    User Activity, view delete
    """
    name = StringField(default="", required=False)
    tags = ListField(default=[], required=False)
    # Unique category to upload the tags in.
    # Becomes important for search etc.
    type = FloatField(default=-1.0, required=False)
    # Reference to MediaSource to which this tag applies.
    # This is only output serialized
    source_ref = ReferenceField('OOHMediaSource', required=False)


class MediaSourceActivity(Document):
    """
    User Activity, view delete
    """
    interacting_user = ReferenceField('MediaUser', required=False)
    mediasource = ReferenceField('MediaSource', required=False)
    activity_time = DateTimeField(required=False)
    activity_type = FloatField(required=False)
    # E.g. email:something, phone: some-number
    activity_meta = StringField(default="", required=False)
    activity_data = DictField(default="", required=False)


class MediaContentActivity(Document):
    """
    User Activity, view delete
    """
    interacting_user = ReferenceField('MediaUser', required=False)
    campaign = ReferenceField('Campaign', required=False)
    ad = ReferenceField('Ad', required=False)
    offer = ReferenceField('OfferExtension', required=False)
    activity_time = DateTimeField(required=False)
    activity_type = FloatField(required=False)
    # E.g. email:something, phone: some-number
    activity_meta = StringField(default="", required=False)
    activity_data = DictField(default="", required=False)


class SourceAnalyticalAttributes(Document):
    """
    Source analytical attributes

    These are categories of attributes that are set by
    administrator.
    Other values like roi, daily_viewerships are calculate
    by back-end analytics.
    """
    # e.g. food, travel
    preferred_categories = StringField(required=False)
    # e.g. youth, infants
    genre_affinities = StringField(required=False)
    # e.g. regular, tourists, distinct visitors, male, female
    target_audience_types = StringField(required=False)
    # Meta
    _created_time = DateTimeField(default=datetime.now)
    _source_id = StringField(default="unknown", required=False)

    meta = {'allow_inheritance': True}

    class Meta:
        abstract = True


class OOHAnalyticalAttributes(SourceAnalyticalAttributes):
    # e.g. ooh
    media_type = StringField(required=True)
    # e.g. reference to instance
    source_ref = ReferenceField('OOHMediaSource', required=True)


class OOHOperationalDailyDataFeed(Document):
    """
    Data can be fed to this class instance via
    CLI or data upload tools.

    Later this data will be aggregated by analytical
    database to derive daily, weekly and monthly average etc.

    This class is for each OOH instance on daily basis.
    """
    source_ref = ReferenceField('OOHMediaSource', required=False)
    visitor_total_count = FloatField(default=0.0, required=False)
    # {
    #   "age" : {"12-30": 1500, "30-60": 2000},
    #   "commute_types" : { "bus": 100, "cabs": 250, "cars": 100},
    #   "target_types" : { "professionals" : 100,
    #                      "drivers" : 200,
    #                      "online_ready" : 1000,
    #                      "leads_ready" : 1000},
    # Recognized types = ['age', 'commute', 'target']
    breakups = DictField(required=False)
    feed_timestamp = DateTimeField(default=datetime.now())
    trusted_source = BooleanField(default=False)


class OOHProcessedAnalytics(Document):
    """
    Data is the result set of analytics operation.
    For example, an outcome of R function.

    This class is for each OOH instance.
    """
    # List of ROIs, trend showing increase and decrease of ROI by
    # week/month/year.
    # ROI  = ((daily_viewership)/(daily_avg_price)) * functional_weight
    # where functional_weight = F(ad_type, ad_genere)
    # is a function derived based on ad_category, and relevance of target
    # viewer ship.
    # [roi_1, roi_2,....]
    roi = ListField()
    roi_mean = FloatField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    period = FloatField()


class Booking(Document):
    """
    Booking/Reservation orders
    for a OOH instance
    """
    # Start date
    start_time = DateTimeField()
    # Requested duration, How many days, 1w, 1d, 1m, 1y etc.
    duration = FloatField()
    # Calculated end time
    end_time = DateTimeField()
    # type of media
    type = StringField(required=True)
    # Reference of media in


class Pricing(Document):
    """
    Different pricing schemes
    """
    # Unique pricing strategy name
    # Christmas pricing
    name = StringField(required=True)
    # Trading
    currency = StringField()
    # Display unit, E.g. per sq.ft
    unit = StringField()
    # Value E.g 5
    rate = FloatField()
    # total price
    price = FloatField()
    # Price offer range
    offer_start_time = DateTimeField()
    offer_end_time = DateTimeField()


class MediaSource(Document):
    """
    Different types of media we integrate our solution with.
    """
    # Basic properties
    name = StringField()
    display_name = StringField()
    caption = StringField(required=False)
    type = StringField()
    # tag data
    tags = StringField(required=False)
    # Can display
    enabled = BooleanField(default=True, required=False)
    # Verification,
    verified = BooleanField(default=False)
    verified_by = ReferenceField('MediaUser', required=False)
    # Media Owner
    owner = ReferenceField('MediaUser', required=False)
    # Creation attributes
    operated_by = ReferenceField('MediaUser', required=False)
    created_time = DateTimeField(default=datetime.now())
    updated_time = DateTimeField(required=False)
    # Subscription details
#     subscription = ReferenceField('Subscription', required=False)

    meta = {'allow_inheritance': True}

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return "/mediasource/%i/" % self.id


class MediaAggregateType(Document):
    """
    MediaAggregate types
    """
    # mall, hospital
    typename = StringField()
    category = StringField(required=True)
    # Any specifications
    typespec = DictField(required=False)
    typedesc = StringField()
    # Icon
    typeicon_image_url = StringField(default="", required=False)
    typeicon_content = ReferenceField('JpegImageContent', required=False)

    def get_absolute_url(self):
        return "/mediaaggregates/types/%i/" % self.id


class MediaAggregate(Document):
    """
    Location specific amenities.
    Every MediaAggregate could could contain one or more
    Media sources
    """
    # Type
    typespec = ReferenceField('MediaAggregateType', required=False)
    # Demographic properties
    name = StringField()
    display_name = StringField()
    description = StringField()
    survey_name = StringField()
    address1 = StringField()
    address2 = StringField()
    city = StringField()
    state = StringField()
    country = StringField()
    # Creation attributes
    owner = ReferenceField('MediaUser', required=False)
    created_time = DateTimeField(default=datetime.now())
    updated_time = DateTimeField(required=False)

    # geo-enabled properties
    location = GeoPointField()
    poi_marker_data = DictField(required=False)
    # IoT properties
    internet_settings = DictField(required=False)
    # Image properties
    icon_image_url = StringField(default="")
    icon_content = ReferenceField('JpegImageContent', required=False)
    image_url = StringField(default="")
    image_content = ReferenceField('JpegImageContent', required=False)
    # e.g. Mall as the media-source
    inhouse_source = ReferenceField('DigitalMediaSource', required=False)
    # retail sources inside a MediaAggregate
    digital_sourcelist = ListField(ReferenceField('DigitalMediaSource'),
                                   default=[], required=False)
    # OOH advertisement source for MediaAggregate
    ooh_sourcelist = ListField(ReferenceField('OOHMediaSource'),
                               default=[], required=False)
    # Radio advertisement source for MediaAggregate
    radio_sourcelist = ListField(ReferenceField('RadioMediaSource'),
                                 default=[], required=False)

    def get_absolute_url(self):
        return "/mediaaggregates/%i/" % self.id


class OOHMediaSource(MediaSource):
    """
    Out of house advertising media type.
    """
    type = 'ooh'
    point = GeoPointField()
    # Uniquely identify OOH instance
    # by location
    location_hash = StringField()

    # Basic attributes
    street_name = StringField()
    city = StringField()
    state = StringField()
    country = StringField()
    pin = StringField()

    # Other attributes
    # 40,30
    size = ListField(default=[])
    lighting_type = StringField()
    ooh_type = StringField()
    area = FloatField()
    min_booking_days = FloatField(default=15.0)

    # Pricing
    pricing = ReferenceField('Pricing', required=False)
    # Bookings
    booking = ReferenceField('Booking', required=False)
    # Advanced parameters
    image_url = StringField()
    primary_image_content = ReferenceField('JpegImageContent')

    def get_absolute_url(self):
        return "/mediasource/ooh/%i/" % self.id


class FloatingMediaSource(MediaSource):
    """
    Floating media source represents a physical source that can be
    moved along a path with a floating range of coverage with respect
    to its current location.
    For example, moving bus ,  etc.
    """
    type = 'floating'
    category = StringField(required=True)
    # Latest Geo location reported
    point = GeoPointField()
    # Radius in KMs
    coverage_area = FloatField(default=0.5)

    def get_absolute_url(self):
        return "/mediasource/floating/%i/" % self.id


class OnlineMediaSource(MediaSource):
    """
    Online media source represents a virtual source that can be
    specified with a floating range of coverage.
    Cloud media source have multiple locations to deliver ads in, 
    all simultaneously.
    For example, online ,  etc.
    """
    type = 'online'
    home_url = StringField(required=True)
    verification_url = StringField(required=True)
    category = StringField(required=True)

    # geo-fences
    fence = GeoPointField(required=True)
    radius = IntegerField(default=100)

    def get_absolute_url(self):
        return "/mediasource/online/%i/" % self.id


class DigitalMediaSource(MediaSource):
    """
    Digital media inside home/mall advertising media type.
    For example, retail outlets,  etc.
    """
    type = 'digital'
    source_internet_settings = DictField(required=True)
    category = StringField(required=True)
    point = GeoPointField()

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


class Amenity(Document):
    """
    Unique amenity
    """
    node_id = StringField(required=True)
    # lat/lon
    point = GeoPointField(required=True)
    # type from OSM
    type = StringField(required=True)
    name = StringField(required=True)
    # tags returned by OSM native APIs
    tags = DictField()
    # book keeping entries
    creation_date = DateTimeField(default=datetime.now())
    updation_date = DateTimeField(default=datetime.now())

    def get_absolute_url(self):
        return "/mediasource/nearby/amenity/%i/" % self.id


class NearBy(Document):
    """
    At a given time, a media source could be near to several amenities.
    Amenity will be unique by its node-id from OSM framework.
    """
    # for e.g. Mall's default source
    media_source = ReferenceField('MediaSource', required=False)
    amenity = ReferenceField('Amenity', required=False)
    # distance
    distance = IntegerField()
    # book-keeping entries
    creation_date = DateTimeField(default=datetime.now())
    deletion_date = DateTimeField()


class Playing(Document):
    """
    At a given time, a media source could play multiple Campaigns.
    The time is captured as start and end, where the relationship is valid.
    This class realizes a  relationship.

    If the media owner decides to abrupt the campaign, he sets the flag
    is_valid to False through Media dash-board. deletion_date will be updated
    for records.
    """
    # for e.g. Mall's default source
    primary_media_source = ReferenceField('MediaSource', required=False)
    playing_content = ReferenceField('Campaign', default=None, required=False)
    # for e.g. VOD, OOH, Sensor etc.
    source_type = StringField()
    # official start-end date
    start_date = DateTimeField(default=datetime.now())
    end_date = DateTimeField()
    # forceful setting of the play flag
    pause_playing = BooleanField(default=False)
    # book-keeping entries
    creation_date = DateTimeField(default=datetime.now())
    deletion_date = DateTimeField()

    def get_absolute_url(self):
        return "/mediacontent/playing/%i/" % self.id


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
    url = StringField(required=False)
    display_url = StringField(required=False)

    # TBD (Sonu): Collection of product urls
    final_urls = StringField(required=False)
    mobile_urls = StringField(required=False)
    app_urls = StringField(required=False)

    # Customer trusted tracking
    thirdparty_tracking_url = StringField(required=False)

    # AdWise tracking
    adwise_tracking_url = StringField(required=False)

    # Location tag
    # TBD: Make tags very generic by nature.
    # For example, tags should be search'able- location,
    # genre, keywords etc.
    ad_location_tag = GeoPointField(required=False)

    # Meta
    ad_type = StringField(required=False)
    custom_parameters = DictField(required=False)
    device_preference = IntegerField(required=False)

    # Campaign this Ad refers to.
    campaign = ReferenceField('Campaign',
                              required=False)
    # List of extension
    offerex = ListField(ReferenceField('OfferExtension'),
                        required=False)
    socialex = ListField(ReferenceField('SocialExtension'),
                         required=False)
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
        return "/mediacontent/ads/extension/location/%i/" % self.id


class BusinessHoursExtension(AdExtension):
    """
    This extension adds business working hours to the
    advertisement impression.
    """
    periods = ListField(ReferenceField(Period))
    days = ListField()

    def get_absolute_url(self):
        return "/mediacontent/ads/extension/businesshours/%i/" % self.id


class SocialMediaExtension(AdExtension):
    """
    This extension adds social media links to the
    advertisement impression.
    """
    facebook_handle = URLField(default="", required=False)
    twitter_handle = URLField(default="", required=False)


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
    # Discount, Introductory, festive etc,
    # Search-tag
    offer_type = StringField(default='offer')
    offer_code = StringField()
    offer_url = StringField()
    # offer_url = StringField(required=False)
    # Search-tag
    offer_description = StringField()
    openDay = DateTimeField()
    closeDay = DateTimeField()

    # Internal data, Stored in ad-wise
    # not to be serialized
    offer_meta = DictField()

    def get_absolute_url(self):
        return "/mediacontent/ads/extension/offer/%i/" % self.id


class SocialExtension(AdExtension):
    """
    This extension adds social extension to the
    advertisement impression.
    """
    # Discount, Introductory, festive etc,
    # Search-tag
    socialmedia_type = StringField(default='')
    socialmedia_url = StringField()
    # Search-tag
    socialmedia_headline = StringField()
    # Internal data, Stored in ad-wise
    # not to be serialized
    _meta = DictField()

    def get_absolute_url(self):
        return "/mediacontent/ads/extension/social/%i/" % self.id


class T_C_Extension(AdExtension):
    """
    This extension adds Terms and Condition extension
    to the advertisement impression.
    """
    t_c_text = StringField()
    # Internal data, Stored in ad-wise
    # not to be serialized
    _meta = DictField()

    def get_absolute_url(self):
        return "/mediacontent/ads/extension/tc/%i/" % self.id


class AmenityExtension(Document):
    """
    Each Mediaaggregate instance can be supplemented using
    different extension. And it is purely based on the
    choice of the Mediaaggregate owner.
    For example, adding or listing brands in a shopping mall.
    or listing the retail extensions in a Shopping mall.
    """
    ex_name = StringField()
    ex_type = StringField()
    userref = ReferenceField('MediaUser')
    amenityref = ReferenceField('MediaAggregate')
    common_name = StringField(required=True)
    image_url = StringField(required=False)
    image = ReferenceField('JpegImageContent', required=False)
    valid_from = DateTimeField(default=datetime.now())
    category = StringField(required=False)
    tagwords = StringField(required=False)
    # Contact details
    phone_numbers = ListField()
    email = StringField()
    # Exact location where the services are offered. (optional)
    point = GeoPointField(required=False)
    # meta
    meta = {'allow_inheritance': True}

    class Meta:
        abstract = True


class BrandExtension(AmenityExtension):
    """
    This extension adds a brand to be part of the
    amenity.
    """
    ex_name = StringField(default='Brands', required=False)
    ex_type = StringField(default='brand')
    brand_name = StringField(required=True)
    brand_description = StringField(required=True)
    brand_url = StringField(required=False)
    # Internal data, Stored in ad-wise
    # not to be serialized
    _meta = DictField(required=False)

    def get_absolute_url(self):
        return "/mediacontent/extension/brands/%i/" % self.id


class RetailExtension(AmenityExtension):
    """
    This extension adds a retail store to be part of the
    amenity.
    """
    ex_name = StringField(default='Retail Stores', required=False)
    ex_type = StringField(default='retail')
    outlet_name = StringField(required=True)
    outlet_description = StringField(required=True)
    # floor, shop number etc.
    outlet_address1 = StringField(required=True)
    outlet_address2 = StringField(required=True)
    affliations = StringField(required=False)
    outlet_url = StringField(required=False)
    brands = StringField()
    # Internal data, Stored in ad-wise
    # not to be serialized
    _meta = DictField(required=False)

    def get_absolute_url(self):
        return "/mediacontent/extension/retail/%i/" % self.id


class FNBExtension(AmenityExtension):
    """
    This extension adds a Food joint to be part of the
    amenity.
    """
    ex_name = StringField(default='Food and Beverages', required=False)
    ex_type = StringField(default='fnb')
    outlet_name = StringField(required=True)
    outlet_description = StringField(required=True)
    # floor, shop number etc.
    outlet_address1 = StringField(required=True)
    outlet_address2 = StringField(required=True)
    # continental, fast food etc.
    cusine = StringField(required=False)
    # Restro-bar, fine dining, driveway etc.
    outlet_type = StringField(required=False)
    average_price_for_2 = StringField(required=False)
    smoking_allowed = BooleanField(default=False)
    beverages_served = BooleanField(default=False)
    outlet_url = StringField(required=False)

    def get_absolute_url(self):
        return "/mediacontent/extension/fnb/%i/" % self.id


class PlayingAracadeExtension(AmenityExtension):
    """
    This extension adds a playing aracade to be part of the
    amenity.
    """
    ex_name = StringField(default='Playing Aracade', required=False)
    ex_type = StringField(default='playingaracade')
    brand_name = StringField(required=True)
    brand_description = StringField(required=True)
    brand_url = StringField(required=True)
    # floor, shop number etc.
    outlet_address1 = StringField(required=True)
    outlet_address2 = StringField(required=True)
    playing_age_group = StringField()
    play_type = StringField(default="indoor")
    play_type_description = StringField()
    open_days = StringField()
    open_timings = StringField()
    # Internal data, Stored in ad-wise
    # not to be serialized
    _meta = DictField(required=False)

    def get_absolute_url(self):
        return "/mediacontent/extension/playaracade/%i/" % self.id


class SpecialityClinicExtension(AmenityExtension):
    """
    This extension adds a specialty clinic to be part of the
    amenity.
    """
    ex_name = StringField(default='Speciality Clinic', required=False)
    ex_type = StringField(default='specialityclinic')
    brand_name = StringField(required=True)
    brand_description = StringField(required=True)
    brand_url = StringField(required=True)
    # floor, shop number etc.
    outlet_address1 = StringField(required=True)
    outlet_address2 = StringField(required=True)
    treatment_services = ListField()
    # > 400
    number_of_beds = StringField()
    # e.g. Religare, Mediassist etc.
    insurance_partners = ListField()
    # e.g. dialysis, neurosurgery, transplant etc.
    service_condition = StringField()
    appointment_facility = BooleanField()
    average_price = IntegerField()
    open_days = StringField()
    open_timings = StringField()
    # Internal data, Stored in ad-wise
    # not to be serialized
    _meta = DictField(required=False)

    def get_absolute_url(self):
        return "/mediacontent/extension/clinic/%i/" % self.id


class DoctorExtension(AmenityExtension):
    """
    This extension adds doctors to be part of the
    amenity.
    """
    ex_name = StringField(default='Doctor', required=False)
    ex_type = StringField(default='doctor')
    name = StringField(required=True)
    description = StringField(required=True)
    url = StringField(required=True)
    # e.g. MD-General Medicine
    subscripts = StringField(required=True)
    experience = StringField(required=True)
    # Achievements - Award, Gold Medalist etc.
    accolades = ListField()
    avg_consultation_charge = StringField()
    appointment_facility = BooleanField()
    available_days = StringField()
    available_timings = StringField()
    # Internal data, Stored in ad-wise
    # not to be serialized
    _meta = DictField(required=False)

    def get_absolute_url(self):
        return "/mediacontent/extension/doctor/%i/" % self.id


class PharmacyExtension(AmenityExtension):
    """
    This extension adds a pharmacy to be part of the
    amenity.
    """
    ex_name = StringField(default='Pharmacy', required=False)
    ex_type = StringField(default='pharmacy')
    brand_name = StringField(required=True)
    brand_description = StringField(required=True)
    brand_url = StringField(required=True)
    # homeo, Ayurveda, English etc.
    pharmacy_type = ListField()
    cards_accepted = ListField()
    medical_registration_id = StringField()
    license_owner_email = StringField()
    # floor, shop number etc.
    outlet_address1 = StringField(required=True)
    outlet_address2 = StringField(required=True)
    open_days = StringField()
    open_timings = StringField()
    # Internal data, Stored in ad-wise
    # not to be serialized
    _meta = DictField(required=False)

    def get_absolute_url(self):
        return "/mediacontent/extension/pharmacy/%i/" % self.id


class FacilityExtension(AmenityExtension):
    # CT-scan, Feeding room, Day care, X-Ray, Wheel chair,
    # 24x7 lab etc.
    """
    This extension adds a facility to be part of the
    amenity.
    """
    ex_name = StringField(default='Value Added Services', required=False)
    ex_type = StringField(default='facility')
    description = StringField(required=True)
    url = StringField(required=True)
    # floor, shop number etc.
    outlet_address1 = StringField(required=True)
    outlet_address2 = StringField(required=True)
    open_days = StringField()
    open_timings = StringField()
    # Internal data, Stored in ad-wise
    # not to be serialized
    _meta = DictField(required=False)

    def get_absolute_url(self):
        return "/mediacontent/extension/facility/%i/" % self.id


class EmergencyServiceExtension(AmenityExtension):
    """
    This extension adds emergency services to be part of the
    amenity.
    """
    ex_name = StringField(default='Emergency Services', required=False)
    ex_type = StringField(default='emergencyservice')
    description = StringField(required=True)
    url = StringField(required=True)
    dial_on_emergency_1 = StringField(required=True)
    dial_on_emergency_2 = StringField(required=True)
    dial_on_emergency_3 = StringField(required=True)
    # floor, shop number etc.
    outlet_address1 = StringField(required=True)
    outlet_address2 = StringField(required=True)
    # Internal data, Stored in ad-wise
    # not to be serialized
    _meta = DictField(required=False)

    def get_absolute_url(self):
        return "/mediacontent/extension/emergency/%i/" % self.id


class OPDServiceExtension(AmenityExtension):
    """
    This extension adds an OPD department to be part of the
    amenity.
    """
    ex_name = StringField(default='OPD Services', required=False)
    ex_type = StringField(default='opdservice')
    brand_name = StringField(required=True)
    brand_description = StringField(required=True)
    brand_url = StringField(required=True)
    # floor, shop number etc.
    outlet_address1 = StringField(required=True)
    outlet_address2 = StringField(required=True)
    treatment_services = ListField()
    # e.g. dialysis, neurosurgery, transplant etc.
    service_condition = StringField()
    appointment_facility = BooleanField()
    average_price = IntegerField()
    open_days = StringField()
    open_timings = StringField()
    # Internal data, Stored in ad-wise
    # not to be serialized
    _meta = DictField(required=False)

    def get_absolute_url(self):
        return "/mediacontent/extension/opd/%i/" % self.id


class HelpdeskExtension(AmenityExtension):
    """
    This extension adds a helpdesk service to be part of the
    amenity.
    """
    ex_name = StringField(default='Helpdesk', required=False)
    ex_type = StringField(default='helpdesk')
    description = StringField(required=True)
    url = StringField(required=True)
    helpdesk_phone_1 = StringField(required=True)
    helpdesk_phone_2 = StringField(required=True)
    # parking assistance, feedback, promotions
    assistance_types = ListField()
    # floor, shop number etc.
    outlet_address1 = StringField(required=True)
    outlet_address2 = StringField(required=True)
    # Internal data, Stored in ad-wise
    # not to be serialized
    _meta = DictField(required=False)

    def get_absolute_url(self):
        return "/mediacontent/extension/helpdesk/%i/" % self.id


class AdventureSportExtension(AmenityExtension):
    """
    This extension adds an adventure sport to be part of the
    amenity.
    """
    ex_name = StringField(default='Adventure', required=False)
    ex_type = StringField(default='adventuresport')
    brand_name = StringField(required=True)
    brand_description = StringField(required=True)
    brand_url = StringField(required=True)
    # floor, shop number etc.
    outlet_address1 = StringField(required=True)
    outlet_address2 = StringField(required=True)
    # Elephant ride, Water ride etc.
    sport_name = StringField()
    sport_description = StringField()
    # > 400
    capacity = StringField()
    target_age_group = StringField()
    # e.g. Decathlon etc.
    brand_partners = ListField()
    # e.g. precaution etc.
    service_condition = StringField()
    reservation_facility = BooleanField()
    reservation_number = StringField()
    average_price = StringField()
    open_days = StringField()
    open_timings = StringField()
    # Internal data, Stored in ad-wise
    # not to be serialized
    _meta = DictField(required=False)

    def get_absolute_url(self):
        return "/mediacontent/extension/sport/%i/" % self.id


# tribal dances, movies etc.
class SpecialInterestExtension(AmenityExtension):
    """
    This extension adds a special interests to be part of the
    amenity.
    """
    ex_name = StringField(default='Special Interest Activity', required=False)
    ex_type = StringField(default='specialinterest')
    description = StringField(required=True)
    url = StringField(required=True)
    # NatureExperience like Butterfly garden
    # WildlifeExperience like Wild life Safari
    interest_target_group = StringField()
    # e.g. precaution etc.
    service_condition = StringField()
    reservation_facility = BooleanField()
    reservation_number = StringField()
    open_days = StringField()
    open_timings = StringField()
    # Internal data, Stored in ad-wise
    # not to be serialized
    _meta = DictField(required=False)

    def get_absolute_url(self):
        return "/mediacontent/extension/special/%i/" % self.id


class StayingExtension(AmenityExtension):
    """
    This extension adds an adventure sport to be part of the
    amenity.
    """
    ex_name = StringField(default='Staying', required=False)
    ex_type = StringField(default='staying')
    brand_name = StringField(required=True)
    brand_description = StringField(required=True)
    brand_url = StringField(required=True)
    # floor, shop number etc.
    outlet_address1 = StringField(required=True)
    outlet_address2 = StringField(required=True)
    # > 400
    capacity = StringField()
    # e.g. precaution etc.
    service_condition = StringField()
    reservation_facility = BooleanField()
    reservation_number = StringField()
    average_price = StringField()
    # Internal data, Stored in ad-wise
    # not to be serialized
    _meta = DictField(required=False)

    def get_absolute_url(self):
        return "/mediacontent/extension/staying/%i/" % self.id


class MultiplexExtension(AmenityExtension):
    """
    This extension adds a multi-plex to be part of the
    amenity.
    """
    ex_name = StringField(default='Multiplex', required=False)
    ex_type = StringField(default='moviemultiplex')
    brand_name = StringField(required=True)
    brand_description = StringField(required=True)
    brand_url = StringField(required=True)
    # floor, shop number etc.
    outlet_address1 = StringField(required=True)
    outlet_address2 = StringField(required=True)
    # > 400
    audis = StringField()
    capacity_per_audi = StringField()
    # e.g. precaution etc.
    service_condition = StringField()
    reservation_facility = BooleanField()
    reservation_number = StringField()
    rservation_url = StringField()
    average_price = StringField()
    open_days = StringField()
    # [9:30-12:30, 12:45-2:30]
    show_timings = ListField()
    # Internal data, Stored in ad-wise
    # not to be serialized
    _meta = DictField(required=False)

    def get_absolute_url(self):
        return "/mediacontent/extension/movie/%i/" % self.id


class AmenityExtensionCollection(Document):

    retails = ListField(ReferenceField('RetailExtension'),
                        default=[], required=False)
    brands = ListField(ReferenceField('BrandExtension'),
                       default=[], required=False)
    fnbs = ListField(ReferenceField('FNBExtension'),
                     default=[], required=False)


class JpegImageContent(Document):
    """
    A JPEG image instance .
    """

    image_type = StringField(default='jpg')
    image = ImageField(required=True)

    def get_absolute_url(self):
        return "/mediacontent/images/%s/" % (
                                self.id)


class Venue(Document):
    """
    A venue that is relevant to a visitor.
    For example, a retail outlet can have multiple
    venues.

    Typically a venue represents an information
    source. A visitor can extract some information
    being near to the venue.

    A visitor can be in vicitnity of many venues at
    any given point in time.

    Venue forms the grouping of sensors.
    Venue forms the object for reporting.
    """
    # Which source
    source = ReferenceField('MediaSource', required=False)
    # venue properties
    venue_name = StringField(unique=True)
    venue_id = StringField(required=True)
    
    zone_name = StringField(required=True)
    zone_id = StringField(required=True)

    venue_address = StringField()
    venue_type = StringField()
    point = GeoPointField()

    venue_meta = DictField(default={}, required=False)
    # created
    created_time = DateTimeField(default=datetime.now(), required=False)

    sensors = ListField(ReferenceField('Sensor'))

    def get_absolute_url(self):
        return "/mediacontent/venue/%s/" % (
                                self.id)


class Sensor(MediaSource):
    uuid = StringField(required=True)
    # beacon, wifi, gps etc.
    type = "sensor"
    range = FloatField(default=10.0)

    # vendor info - nikaza, nearby, google
    vendor = StringField(default='nearby', required=False)

    # Every sensor can be associated with
    # an optional [lat,lng] fields.
    location = GeoPointField(required=False)
    # reference to the venue
    venue = ReferenceField('Venue', required=False)

    meta = {'allow_inheritance': True}

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return "/mediasource/sensor/%s/" % (
                                self.id)


class Beacon(Sensor):
    name = StringField()
    major = IntegerField(default=0)
    minor = IntegerField(default=0)
    beacon_type = StringField(default='iBeacon')

    max_tx_power = FloatField(required=True)

    # optional content
    broadcast_url = StringField(default="http://www.series-5.com/research")

    def get_absolute_url(self):
        return "/mediasource/beacon/%s/" % (
                                self.id)


class WiFi(Sensor):
    name = StringField()
    hw_addr = StringField()
    max_tx_power = FloatField()

    def get_absolute_url(self):
        return "/mediasource/wifi/%s/" % (
                                self.id)


class SensorActivity(Document):
    """
    Sensor Activity, enter, leave, block
    """
    interacting_user = ReferenceField('MediaUser', required=False)
    sensor = ReferenceField('Sensor', required=False)
    activity_time = DateTimeField(required=False)
    # 1 -> enter
    # 2 -> exit
    # 3 -> optout
    activity_type = FloatField(default=0.0, required=False)
    # E.g. email:something, phone: some-number
    activity_data = DictField(default="", required=False)
