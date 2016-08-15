from mongoengine.fields import GeoPointField, DictField, ListField,\
    DateTimeField, StringField, EmailField, BooleanField,\
    ReferenceField
from datetime import datetime
from mongoengine.document import Document
from mongoengine import connect
from atlas_ws.settings import _MONGODB_NAME
from rest_framework import fields

connect(_MONGODB_NAME, alias='default')


class UserRole(Document):
    name = StringField()
    description = StringField(required=False)
    # reference - DRF field
    url = fields.URLField(source='get_absolute_url', read_only=False)


# Represents the agency/organization
class Project(Document):
    # unique name
    name = StringField(verbose_name='name', required=True)
    # organization type
    type = StringField(verbose_name='type', required=True)
    # correspondence
    address = StringField(verbose_name='address', required=True,
                          max_length=256)
    city = StringField(verbose_name='city', required=True, max_length=80)
    state = StringField(verbose_name='state', required=True, max_length=80)
    pin = StringField(verbose_name='pin', required=True, max_length=80)
    is_verified = BooleanField(default=False, required=False)

    # Organization location/geo-spatial
    point = GeoPointField()
    date_created = DateTimeField(default=datetime.now())
    # reference - DRF field
    url = fields.URLField(source='get_absolute_url', read_only=False)


class UserPersonalPref(Document):
    type = 'personal'
    personal_name = StringField(max_length=30)
    value = StringField(max_length=30)
    # Person's behavior related opaque data
    personal_info = DictField(required=False)


class UserDevicePref(Document):
    type = 'device'
    device_tag = StringField(max_length=30)
    device_type = StringField(max_length=30)
    # Device specific data
    device_info = DictField(required=False)


class UserMediaPref(Document):
    type = 'media'
    media_tag = StringField(max_length=30)
    media_type = StringField(max_length=30)
    # Device specific data
    media_info = DictField(required=False)


class UserLocationPref(Document):
    type = 'location'
    # 'work', 'home' etc.
    location_name = StringField(max_length=30)
    # Device specific data
    loc = GeoPointField(required=True)


# Any user in the AdWise system
class MediaUser(Document):
    # Friendly name
    name = StringField(required=True)
    # Identity
    username = StringField(required=True)
    password = StringField(required=True)
    # e-correspondence
    phone_number = StringField(required=True)
    email = EmailField(verbose_name='email', required=True)
    gender = StringField(required=False)
    # correspondence
    address = StringField(verbose_name='address', required=False,
                          max_length=256)
    city = StringField(verbose_name='city', required=False, max_length=80)
    state = StringField(verbose_name='state', required=False, max_length=80)
    pin = StringField(verbose_name='pin', required=False, max_length=80)
    # current location
    point = GeoPointField(required=False)
    # Records
    date_joined = DateTimeField(default=datetime.now())
    last_updated = DateTimeField(default=datetime.now())
    last_activity = DateTimeField(default=datetime.now())
    # Properties
    is_admin = BooleanField(default=False, required=False)
    email_verified = BooleanField(default=False, required=False)
    phone_verified = BooleanField(default=False, required=False)
    # Organization link (optional)
    project_id = ReferenceField(Project, required=False)
    # TBD (Note:Sonu) More role association
    role = ReferenceField(UserRole, required=False)
    # Preferences
    device_pref = ListField(ReferenceField('UserDevicePref'), required=False)
    personal_pref = ListField(ReferenceField('UserPersonalPref'),
                              required=False)
    media_pref = ListField(ReferenceField('UserMediaPref'), required=False)
    loc_pref = ListField(ReferenceField('UserLocationPref'), required=False)

    # Reference - DRF field
    url = fields.URLField(source='get_absolute_url', read_only=False)

    def do_update(self, password=None, phone_number=None, email=None,
                  address=None, email_verified=None, phone_verified=None):
        if password:
            self.password = password
        if phone_number:
            self.phone_number = phone_number
        if email:
            self.email = email
        if email_verified:
            self.email_verified = email_verified
        if phone_verified:
            self.phone_verified = phone_verified

        self.last_updated = datetime.now()

    def get_absolute_url(self):
        return "/users/%i/" % self.id


class UserService(Document):
    user_ref = ReferenceField('MediaUser')
    user_session = ReferenceField('UserSession')
    service_id = ReferenceField('Service')
    enabled = BooleanField()
    last_report_time = DateTimeField()
    auto_restart = BooleanField()


class Service(Document):
    service_friendly_name = StringField(max_length=30)
    service_id = StringField()
    service_provider = StringField()
    service_driver = StringField()


class UserSession(Document):
    session_id = StringField()
    # Session for the user.
    user_ref = ReferenceField('MediaUser')
    # services included in session
    services = ListField(ReferenceField('UserService'))


class ServiceRequest(Document):

    target_service_name = StringField(max_length=30)
    request_time = DateTimeField()
    target_service_id = ReferenceField('Service')
    requesting_user_id = ReferenceField('MediaUser')
    # unknown data, delegated to driver.
    service_meta = StringField()


class Location(Document):
    service_key = StringField()
    point = GeoPointField()


class Meter(Document):
    service_key = StringField()


# Token that is passed when a user is added by
# a referee. E.g P(X) admin adding employee.
class ReferedUserCreateRequest(Document):
    user = ReferenceField('MediaUser')
    token = StringField(required=False)
