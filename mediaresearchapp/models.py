from mongoengine.fields import ListField,\
    StringField, DateTimeField, FloatField,\
    ReferenceField, GeoPointField, DictField
# from django_mongodb_engine.fields import GridFSField
from mongoengine.document import Document
from mongoengine import connect
from atlas_ws.settings import _MONGODB_NAME
from datetime import datetime
from mongoengine.base.fields import ObjectIdField


connect(_MONGODB_NAME, alias='default')

All = 'everyone'


class ByFieldSearchQuery(Document):
    userid = ObjectIdField(required=False)
    # e.g. 15-20
    search_string = StringField()
    # e.g. target_group
    query_field = StringField(required=True)
    creation_time = DateTimeField(default=datetime.now())
    query_runtime_duration = FloatField()


class SearchQuery(Document):
    userid = ObjectIdField(required=False)
    query_type = StringField(default="Campaign", required=False)
    # e.g. 15-20, youth
    raw_strings = StringField()
    # e.g.
    #        {"field-1":4,
    #         "field-2":5}
    # where, 4, 5 are the ranking
    query_fields = DictField(default={})
    creation_time = DateTimeField(default=datetime.now())
    query_runtime_duration = FloatField()


class ResearchElement(Document):
    user = ReferenceField('MediaUser', required=False)
    archive_queries = ListField(ReferenceField('SearchQuery'))
    query = ReferenceField('SearchQuery')


class ResearchResult(Document):
    campaigns = ListField(ReferenceField('Campaign'))
    oohs = ListField(ReferenceField('OOHMediaSource'))
    query_runtime_duration = FloatField(default=0.0)
