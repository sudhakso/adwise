'''
Created on Dec 12, 2015

@author: sonu
'''
from django.conf import settings
from mediacontentapp import Config
from mediacontentapp.models import OOHMediaSource
from mongoengine.fields import GeoPointField
from pyes import ES


class IndexingService():

    def __init__(self):
        '''
        Constructor
        '''
        param = {
            'default_ini': '%s%s' % (settings.MEDIAAPP_DIR, 'mediaconfig.ini'),
            'default_value_map': {}
            }

        self.indexcfg = Config.config(**param)
        self.endpoint = self.indexcfg.get_config(
                                        'indexing', 'pyes_endpoint')
        self.indexing_tags = [e.strip() for e in self.indexcfg.get_config(
                                            'indexing', 'index').split(',')]
        self._conn = ES(self.endpoint)
        # create the indexes
        self.create_indexes(self.indexing_tags)

    @property
    def connection(self):
        return self._conn

    def status(self):
        pass

    def create_indexes(self, tags):
        for index in tags:
            try:
                self.connection.indices.create_index_if_missing(index.lower())
            except TypeError as te:
                print "Exception creating index (%s). Index exists : (%s)." % (
                                                        index, str(te))
            except Exception as e:
                print "Exception creating index (%s). Critical : (%s)." % (
                                                        index, str(e))


class CampaignManager():

    def _valid_geo(self, param):
        if isinstance(param, GeoPointField):
            return True

    def prepare_campaign(self, user, camp, spec):
        # update the geo-hash for the campaign
        if camp and spec:
            for _id in spec.linked_source_ids:
                ooh = OOHMediaSource.objects.filter(id=_id)
                if ooh and ooh[0].point:
                    camp.geo_tags.append(ooh[0].point)
            camp.save()

    def enable_campaign(self):
        pass


class DashboardController():

    def update_dashboard(self, dash, args):
        pass

    def process_query(self, *args):
        pass

    def type(self, role_name):
        if role_name is None:
            return "UNKNOWN"

        if role_name == "BO":
            return "MEDIA_OWNER"
        elif role_name == "MA":
            return "MEDIA_BROWSER"
        elif role_name == "OP":
            return "PARTNER"
        else:
            return "UNKNOWN"


class ActivityManager():

    @staticmethod
    def get_activity_id(activity_name):
        activities = dict(share=1,
                          like=2,
                          dislike=3,
                          quote=4,
                          view=5)

        if activity_name in activities:
            return activities[activity_name]
        else:
            return -1


class TagManager():

    # Add more tags here.
    # Idea is not to support wild variety of tags.
    # Tags must be designed properly.
    # Please note the values in the tag is not controlled.
    @staticmethod
    def get_tag_id(tag_name):
        tags = dict(nearby=1,
                    seenby=2,
                    adtype=3)

        if tag_name in tags:
            return tags[tag_name]
        else:
            return -1
