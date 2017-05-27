'''
Created on Dec 12, 2015

@author: sonu
'''
from jinja2 import Template
import json
from django.conf import settings
from mediacontentapp import Config
from mediacontentapp.models import OOHMediaSource
from mongoengine.fields import GeoPointField
from pyes import ES
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK,\
    HTTP_304_NOT_MODIFIED
from userapp.JSONFormatter import JSONResponse
from mediacontentapp.models import Campaign, Playing
from mediacontentapp.serializers import PlayingSerializer


class CloudMediaController():

    ADD_MEDIA_CONTENT = 'addcontent'

    def __init__(self):
        self.playing_template = Template(
                               open('%s%s' % (settings.MEDIAAPP_DIR,
                                    'templates/playing.j2'),
                                    'r').read())

    def handle_update(self, inst, *args, **kwargs):
        pass

    def handle_operations(self, cloud, action, action_args, action_data):
        # action= add media etc., action_args= content-id, action_data= {}
        print 'CloudMediaController: Performing action %s' % action

        if action == self.ADD_MEDIA_CONTENT:
            # Add media content to OOH Media source object
            campid = action_args['id'] if 'id' in action_args else None
            if campid is None:
                return JSONResponse('content id cannot be None for action type'
                                    ' %s' % self.ADD_MEDIA_CONTENT,
                                    status=HTTP_400_BAD_REQUEST)
            # get the campaign
            campaign = Campaign.objects.get(id=campid)
            _nv = {'source_type': 'cloudmediasource',
                   'start_date': action_data['start_date'],
                   'end_date': action_data['end_date']}
            _playing_data = json.loads(
                                str(self.playing_template.render(**_nv)))
            playing = PlayingSerializer(data=_playing_data)
            if playing.is_valid(raise_exception=True):
                play = playing.save()
                play.update(primary_media_source=cloud,
                            playing_content=campaign)
                return JSONResponse(playing.validated_data,
                                    status=HTTP_200_OK)
        else:
            # Unknown operation
            pass


class OOHMediaController():

    ADD_MEDIA_CONTENT = 'addcontent'
    PAUSE_MEDIA_CONTENT = 'pausecontent'
    RESUME_MEDIA_CONTENT = 'resumecontent'

    def __init__(self):
        self.playing_template = Template(
                               open('%s%s' % (settings.MEDIAAPP_DIR,
                                    'templates/playing.j2'),
                                    'r').read())


    # TBD
    def handle_update(self, inst, *args, **kwargs):
        pass

    def handle_operations(self, ooh, action, action_args, action_data):
        # action= add media etc., action_args= content-id, action_data= {}
        print 'OOHMediaController: Performing action %s' % action

        if action == self.ADD_MEDIA_CONTENT:
            # Add media content to OOH Media source object
            campid = action_args['id'] if 'id' in action_args else None
            if campid is None:
                return JSONResponse('content id cannot be None for action type'
                                    ' %s' % self.ADD_MEDIA_CONTENT,
                                    status=HTTP_400_BAD_REQUEST)
            # get the campaign
            campaign = Campaign.objects.get(id=campid)
            _nv = {'source_type': 'oohmediasource',
                   'start_date': action_data['start_date'],
                   'end_date': action_data['end_date']}
            _playing_data = json.loads(
                                str(self.playing_template.render(**_nv)))
            playing = PlayingSerializer(data=_playing_data)
            if playing.is_valid(raise_exception=True):
                play = playing.save()
                play.update(primary_media_source=ooh,
                            playing_content=campaign)
                return JSONResponse(playing.validated_data,
                                    status=HTTP_200_OK)
        elif action == self.PAUSE_MEDIA_CONTENT:
            # Add media content to MediaAggregate object
            campid = action_args['id'] if 'id' in action_args else None
            if campid is None:
                return JSONResponse('content id cannot be None for action type'
                                    ' %s' % self.PAUSE_MEDIA_CONTENT,
                                    status=HTTP_400_BAD_REQUEST)
            # get the campaign
            campaign = Campaign.objects.get(id=campid)
            play = Playing.objects.get(primary_media_source=ooh,
                                       playing_content=campaign)
            # Valid playing object
            if play.pause_playing is False:
                play.update(pause_playing=True)
                play.save()

            return JSONResponse("Campaign paused momentarily",
                                status=HTTP_200_OK)
        elif action == self.RESUME_MEDIA_CONTENT:
            # Add media content to MediaAggregate object
            campid = action_args['id'] if 'id' in action_args else None
            if campid is None:
                return JSONResponse('content id cannot be None for action type'
                                    ' %s' % self.RESUME_MEDIA_CONTENT,
                                    status=HTTP_400_BAD_REQUEST)
            # get the campaign
            campaign = Campaign.objects.get(id=campid)
            play = Playing.objects.get(primary_media_source=ooh,
                                       playing_content=campaign)
            # Valid playing object
            if play.pause_playing is True:
                play.update(pause_playing=False)
                play.save()

            return JSONResponse("Campaign resumed",
                                status=HTTP_200_OK)
        else:
            # Unknown operation
            pass


class MediaAggregateController():

    ADD_MEDIA = 'addmedia'
    ADD_MEDIA_CONTENT = 'addcontent'
    PAUSE_MEDIA_CONTENT = 'pausecontent'
    RESUME_MEDIA_CONTENT = 'resumecontent'
    ADD_SERVICE = 'addservice'

    def __init__(self):
        self.playing_template = Template(
                               open('%s%s' % (settings.MEDIAAPP_DIR,
                                    'templates/playing.j2'),
                                    'r').read())


    # TBD
    def handle_update(self, inst, *args, **kwargs):
        pass

    def handle_operations(self, amenity, action, action_args, action_data):
        # action= add media etc., action_args= content-id, action_data= {}
        print 'MediaAggregateController: Performing action %s' % action

        if action == self.ADD_MEDIA:
            # Add source to Mediaaggregate object
            pass
        elif action == self.ADD_MEDIA_CONTENT:
            # Add media content to MediaAggregate object
            campid = action_args['id'] if 'id' in action_args else None
            if campid is None:
                return JSONResponse('content id cannot be None for action type'
                                    ' %s' % self.ADD_MEDIA_CONTENT,
                                    status=HTTP_400_BAD_REQUEST)
            # get the campaign
            campaign = Campaign.objects.get(id=campid)
            _nv = {'source_type': 'mediaaggregate',
                   'start_date': action_data['start_date'],
                   'end_date': action_data['end_date']}
            _playing_data = json.loads(
                                str(self.playing_template.render(**_nv)))
            playing = PlayingSerializer(data=_playing_data)
            if playing.is_valid(raise_exception=True):
                play = playing.save()
                play.update(primary_media_source=amenity.inhouse_source,
                            playing_content=campaign)
                return JSONResponse(playing.validated_data,
                                    status=HTTP_200_OK)
        elif action == self.PAUSE_MEDIA_CONTENT:
            # Add media content to MediaAggregate object
            campid = action_args['id'] if 'id' in action_args else None
            if campid is None:
                return JSONResponse('content id cannot be None for action type'
                                    ' %s' % self.PAUSE_MEDIA_CONTENT,
                                    status=HTTP_400_BAD_REQUEST)
            # get the campaign
            campaign = Campaign.objects.get(id=campid)
            play = Playing.objects.get(primary_media_source=amenity.inhouse_source,
                                       playing_content=campaign)
            if play.pause_playing is False:
                play.pause_playing = True
                play.save()

            return JSONResponse("Campaign paused momentarily",
                                status=HTTP_200_OK)
        elif action == self.RESUME_MEDIA_CONTENT:
            # Add media content to MediaAggregate object
            campid = action_args['id'] if 'id' in action_args else None
            if campid is None:
                return JSONResponse('content id cannot be None for action type'
                                    ' %s' % self.RESUME_MEDIA_CONTENT,
                                    status=HTTP_400_BAD_REQUEST)
            # get the campaign
            campaign = Campaign.objects.get(id=campid)
            play = Playing.objects.get(primary_media_source=amenity.inhouse_source,
                                       playing_content=campaign)
            if play.pause_playing is True:
                play.pause_playing = False
                play.save()
            return JSONResponse("Campaign resumed",
                                status=HTTP_200_OK)
        elif action == self.ADD_SERVICE:
            # Fill directory service in MediaAggregate object
            pass
        else:
            # Unknown operation
            pass


class ESMapper():
    # Initialize the mapper config
    def __init__(self, config):
        self.mappers = [e.strip() for e in config.get_config(
                                    'indexing', 'mapping').split(',')]

    def get_mapping(self, _type):
        for mapper in self.mappers:
            name = mapper.split(':')[0]
            maptemplate = mapper.split(':')[1]
            if name == _type:
                j2_template = Template(
                        open('%s%s' % (settings.MEDIAAPP_DIR,
                                       'templates/%s' % maptemplate),
                             'r').read())
                _data = json.loads(str(j2_template.render()))
                return _data
        return None


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
        self._mapper = ESMapper(self.indexcfg)
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
                print "Creating index (%s)..." % (index)
                self.connection.indices.create_index_if_missing(index.lower())
                # Generate the mapping for the index if specified.
                print "Checking mapping types for index (%s)..." % (index)
                mapdata = self._mapper.get_mapping(index)
                if mapdata is not None:
                    print "Creating mapping types for index (%s)..." % (index)
                    self.connection.indices.put_mapping(
                                                'external',
                                                {'properties': mapdata},
                                                [index.lower()])
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
