from mongoengine.fields import GeoPointField, DictField, ListField,\
    StringField, URLField, BooleanField, DateTimeField, FloatField,\
    ReferenceField, ImageField
# from django_mongodb_engine.fields import GridFSField
from mongoengine.document import Document
from mongoengine import connect
from atlas_ws.settings import _MONGODB_NAME
from rest_framework import fields
from rest_framework.fields import IntegerField
from datetime import datetime
from bson.json_util import default
from mediacontentapp.models import OOHMediaSource

connect(_MONGODB_NAME, alias='default')

All = 'everyone'


# Create your models here.
class oohplanrequest(Document):
    wish = StringField(required=True)
    filters = ListField(default=[], required=False)


class plannerresult(Document):
    oohs = ListField(ReferenceField('OOHMediaSource'))
    mediaaggregates = ListField(ReferenceField('MediaAggregate'))
