from mongoengine.fields import ListField,\
    StringField, DateTimeField, FloatField,\
    ReferenceField, GeoPointField
# from django_mongodb_engine.fields import GridFSField
from mongoengine.document import Document
from mongoengine import connect
from atlas_ws.settings import _MONGODB_NAME
from datetime import datetime
from mongoengine.base.fields import ObjectIdField


connect(_MONGODB_NAME, alias='default')

All = 'everyone'


# Leads for non-registered user
class StartupLeads(Document):
    # User email
    email = StringField(required=False)
    phone_number = StringField(required=False)
    # Last activity
    activity = DateTimeField(default=datetime.now())
    # Attempts to use the product w/o reg.
    attempts = FloatField(required=False)
    # latest location tried
    cordinates = GeoPointField(required=False)


class SearchQuery(Document):
    userid = ObjectIdField(required=False)
    raw_strings = StringField()
    query_fields = ListField(default=[])
    query_values = ListField(default=[])
    creation_time = DateTimeField(default=datetime.now())
    query_runtime_duration = FloatField()


class ResearchElement(Document):
    user = ReferenceField('MediaUser', required=False)
    archive_queries = ListField(ReferenceField('SearchQuery'))
    query = ReferenceField('SearchQuery')


class ResearchResult(Document):
    campaigns = ListField(ReferenceField('Campaign'))
    query_runtime_duration = FloatField(default=0.0)