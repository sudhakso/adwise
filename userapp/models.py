from django.db import models
from django.db.models.fields.related import ForeignKey
from mongoengine.fields import GeoPointField, DictField, ListField,\
    DateTimeField, StringField, EmailField
from datetime import datetime
from mongoengine.document import Document

# Create your models here.
class MediaUser(Document):
    username = StringField(verbose_name='username', required=True, max_length=30)
    password = StringField(verbose_name='password', required=True, max_length=30)
    phone_number = StringField(verbose_name='phone_number', required=True, max_length=30)
    email = EmailField()
    address = GeoPointField()
    date_joined = DateTimeField(default=datetime.now())
    last_updated = DateTimeField(default=datetime.now())
    last_activity = DateTimeField(default=datetime.now())
    
    def do_update(self, password=None, phone_number=None, email=None, address=None):
        if password:
            self.password = password            
        if phone_number : 
            self.phone_number = phone_number           
        if email:
            self.email = email
                    
        self.last_updated = datetime.now();
    
class PreferenceCategory(Document):
#   ['Arts and Entertainment', 'Food', 'Sports', 'Travel', 'shop', 'outdoor', 'Home', 
#    'work', 'others'...]
    name = StringField(max_length=30)

class PreferenceSubCategory(Document):
    
    name = StringField(max_length=30)
    values = ListField()
    category_ref = ForeignKey('PreferenceCategory')

class UserPersonalPref(Document):
    preferences = models.ManyToManyField('PreferenceSubCategory')
    user_ref = ForeignKey('MediaUser')

class UserDevicePref(Document):
    device_tag = models.CharField(max_length=30)
    device_type = models.CharField(max_length=30)
    # Device specific data
    device_info = DictField()
    # Primary user who owns device    
    user_ref = ForeignKey('MediaUser')

class UserMediaPref(Document):
    media_tag = models.CharField(max_length=30)
    media_type = models.CharField(max_length=30)
    # Device specific data
    media_info = DictField()
    # Primary user who owns device    
    user_ref = ForeignKey('MediaUser')
    