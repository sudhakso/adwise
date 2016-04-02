from mongoengine.fields import ListField,\
    StringField, DateTimeField, FloatField,\
    ReferenceField
# from django_mongodb_engine.fields import GridFSField
from mongoengine.document import Document
from mongoengine import connect
from atlas_ws.settings import _MONGODB_NAME


connect(_MONGODB_NAME, alias='default')

All = 'everyone'


class SearchQuery(Document):
    query_fields = ListField(StringField())
    query_values = ListField(StringField())
    creation_time = DateTimeField()
    query_runtime_duration = FloatField()


class ResearchElement(Document):
    user = ReferenceField('MediaUser', required=False)
    archive_queries = ListField(ReferenceField('SearchQuery'))
    query = ReferenceField('SearchQuery')


class ResearchResult(Document):
    resource_urls = ListField(default=[], required=False)
    campaigns = ListField(default=[])
    ads = ListField(default=[])
