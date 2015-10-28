from django.db import models
from mongoengine.fields import GeoPointField, DictField, ListField,\
    StringField, URLField, LongField, BooleanField
from mongoengine.document import Document
from rest_framework import fields
from rest_framework.fields import IntegerField


# Create your models here.
class Period(Document):
    openDay = StringField()
    openTime = StringField()
    closeTime = StringField()
    closeDay = StringField()


class AdExtension(Document):
    ex_name = StringField()
    ex_type = StringField()
    # meta
    meta = {'allow_inheritance': True}

    class Meta:
        abstract = True


class Ad(Document):

    url = URLField()
    display_url = URLField()

    # Collection of product urls
    final_urls = ListField<URLField>()
    mobile_urls = ListField<URLField>()
    app_urls = ListField<URLField>()

    # Lead for grabbing customer info
    tracking_url = URLField()

    # Meta
    ad_type = StringField()
    custom_parameters = DictField()
    device_preference = IntegerField()

    # List of extension
    extenstions = models.ManyToManyField('AdExtension')

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

    headline = StringField(max_length=2048)
    description1 = StringField()
    description2 = StringField()

    ad_type = StringField(default='TextAd')
    # reference - DRF field
    url = fields.URLField(source='get_absolute_url', read_only=False)

    def get_absolute_url(self):
        return "/mediacontent/textads/%i/" % self.id

"""
A product ad based on product data 
of a Shopping campaign's associated Merchant Center
account.
"""


class ProductAd(Ad):

    # Promotional line for this ad.
    # This text will be displayed in addition to the products.
    promotionLine = StringField()
    ad_type = StringField(default='ProductAd')

    # reference - DRF field
    url = fields.URLField(source='get_absolute_url', read_only=False)

    def get_absolute_url(self):
        return "/mediacontent/productads/%i/" % self.id

"""
Dynamically generated search ads based on the content
of a web site.
"""


class DynamicSearchAd(Ad):
    # All fields are filled dynamically.
    # Simple variation of base class 'Ad'.
    ad_type = StringField(default='DynamicSearchAd')
    # reference - DRF field
    url = fields.URLField(source='get_absolute_url', read_only=False)

    def get_absolute_url(self):
        return "/mediacontent/dynamicsearchads/%i/" % self.id


"""
An ad for a Click to Call Only Campaign.
"""


class CallOnlyAd(Ad):

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
        return "/mediacontent/callonlyads/%i/" % self.id


"""
An ad that includes a graphic to promote 
your business.
"""


class ImageAd(Ad):

    ad_type = StringField(default='ImageAd')

    def get_absolute_url(self):
        return "/mediacontent/imageads/%i/" % self.id


"""
Contains a click-to-call phone number, 
a link to a website, or both.
"""


class MobileAd(Ad):
    ad_type = StringField(default='MobileAd')

    def get_absolute_url(self):
        return "/mediacontent/mobileads/%i/" % self.id

"""
An ad based on a predefined template.
"""


class TemplateAd(Ad):
    ad_type = StringField(default='TemplateAd')

    def get_absolute_url(self):
        return "/mediacontent/templateads/%i/" % self.id


class LocationExtension(AdExtension):

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
        return "/mediacontent/locationextensions/%i/" % self.id


class BusinessHoursExtension(AdExtension):

    periods = ListField<Period>()
    days = ListField()

    def get_absolute_url(self):
        return "/mediacontent/businesshoursextensions/%i/" % self.id


class ReviewExtension(AdExtension):
    pass


class SiteLinkExtension(AdExtension):
    pass


class AppExtension(AdExtension):
    pass


class OfferExtension(AdExtension):
    pass
