from mongoengine.fields import ListField,\
    StringField, DateTimeField, FloatField,\
    ReferenceField, DictField
# from django_mongodb_engine.fields import GridFSField
from mongoengine.document import Document
from mongoengine import connect
from atlas_ws.settings import _MONGODB_NAME
from datetime import datetime
from mongoengine.base.fields import ObjectIdField


connect(_MONGODB_NAME, alias='default')

All = 'everyone'


class SearchQuery(Document):
    userid = ObjectIdField(required=False)
    query_object_type = StringField(required=True)
    query_type = StringField(default='multifield', required=False)
    # e.g. 15-20, youth
    raw_strings = StringField()
    # e.g.
    #        {"field-1":4,
    #         "field-2":5}
    # where, 4, 5 are the ranking
    query_fields = DictField(default={})
    creation_time = DateTimeField(default=datetime.now())
    query_runtime_duration = FloatField()


class CampaignResearchResult(Document):
    campaigns = ListField(ReferenceField('Campaign'))
    query_runtime_duration = FloatField(default=0.0)


class ResearchResult(Document):
    campaigns = ListField(ReferenceField('Campaign'))
    oohs = ListField(ReferenceField('OOHMediaSource'))
    query_runtime_duration = FloatField(default=0.0)
