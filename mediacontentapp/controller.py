'''
Created on Dec 12, 2015

@author: sonu
'''
from jinja2 import Template
import json
from django.conf import settings
from mediacontentapp import Config
from mediacontentapp import urlutils
from mediacontentapp.models import OOHMediaSource
from mongoengine.fields import GeoPointField
from pyes import ES
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK,\
 HTTP_500_INTERNAL_SERVER_ERROR, HTTP_204_NO_CONTENT
from userapp.JSONFormatter import JSONResponse
from mediacontentapp.models import Campaign, Playing, Venue, MediaAggregate
from mediacontentapp.serializers import PlayingSerializer
from mediacontentapp.sourceserializers import SensorSerializer, BeaconSerializer,\
    WiFiSerializer, VenueSerializer
from urlutils import TinyUrlDriver, Series5UrlDriver


class VenueController():

    # Use case where you would import all sensors from
    # partner portal. e.g GET nikaasa.com/sensors
    ATTACH_SENSOR = 'attach'
    ACTIVATE_SENSOR = 'activate'
    DEACTIVATE_SENSOR = 'deactivate'
    ADD_MEDIA_CONTENT = 'addcontent'
    PAUSE_MEDIA_CONTENT = 'pausecontent'
    RESUME_MEDIA_CONTENT = 'resumecontent'
    FILTER_BY_MEDIAAGGREGATE = "filter_by_mediaaggregate"

    def __init__(self):
        self.playing_template = Template(
                               open('%s%s' % (settings.MEDIAAPP_DIR,
                                    'templates/playing.j2'),
                                    'r').read())

    def _publish_campaign_to_sensors(self, play, sensor, campaign):
        from mediacontentapp.tasks import CampaignPublishingTask

        ps = PlayingSerializer(play)
        publishing_task = CampaignPublishingTask()
        # Publish the campaign
        rc = publishing_task.delay(args=[],
                                   pub_content_id=str(campaign.id),
                                   pub_source_id=str(sensor.id),
                                   pub_detail=json.dumps(ps.data),
                                   ignore_failures=True)
        if rc.ready():
            if rc.state == "SUCCESS":
                # put the meta returned by the vendor into play
                # attributes.
                if rc.get() is not None:
                    vendor_meta = rc.get()
                    play.playing_vendor_attributes = eval(vendor_meta)
                    play.save()
                    print "Posted campaign publish task: OK. Response %s" % vendor_meta
                    return 0
                else:
                    print "Posted campaign publish task: Failed. Unknown error"
                    return -1
            else:
                print "Posted campaign publish task: Celery task framework failed."
                return -1

    def _update_campaign_to_sensors(self, play, sensor, campaign):
        print "Update campaign not implemented"
        return -1

    def _control_campaign_on_sensors(self, play, sensor, campaign, update):
        from mediacontentapp.tasks import CampaignControlTask

        ps = PlayingSerializer(play)
        control_task = CampaignControlTask()
        # retrieve vendor data and pass it along for update operation.
        # ps.data has the details
        rc = control_task.delay(args=[],
                                pub_content_id=str(campaign.id),
                                pub_source_id=str(sensor.id),
                                pub_detail=json.dumps(ps.data),
                                update=update,
                                ignore_failures=True)
        if rc.ready():
            if rc.state == "SUCCESS":
                if rc.get() is not None:
                    print "Post of udpate campaign task: OK. Response %s" % rc.get()
                    return 0
                else:
                    print "Post of udpate campaign task: Failed. Response Unknown Error"
                    return -1
            else:
                print "Post of update campaign publish task: Failed."
                return -1

    def handle_update(self, inst, *args, **kwargs):
        pass

    def handle_operations(self, venue, action, action_args, action_data):
        # action= add media etc., action_args= content-id, action_data= {}
        print 'VenueController: Performing action %s' % action

        if action == self.ATTACH_SENSOR:
            # Add a sensor to the Venue object
            sensortype = action_data['sensor_type'] if 'sensor_type' in action_data else None
            sensordata = action_data['sensor_data'] if 'sensor_data' in action_data else None
            if sensortype is None or sensordata is None:
                return JSONResponse('sensor type and data cannot be None for action type'
                                    ' %s' % self.ATTACH_SENSOR,
                                    status=HTTP_400_BAD_REQUEST)
            # prepare the sensor based on type
            if sensortype.lower() == 'beacon':
                ser = BeaconSerializer(data=sensordata)
            elif sensortype.lower() == 'wifi':
                ser = WiFiSerializer(data=sensordata)
            else:
                return JSONResponse("Unknown sensor type. wifi and beacon are supported.",
                                    status=HTTP_400_BAD_REQUEST)
            # Save the venue
            if ser.is_valid(raise_exception=True):
                sensor = ser.save()
                # Save the venue information for use in sensor
                # e.g. publishing campaign needs venue Id with
                # some sensor cases.
                sensor.update(venue=venue)
                # Update sensors inside Venue
                venue.sensors.append(sensor)
                venue.save()
            return JSONResponse("Sensor added",
                                status=HTTP_200_OK)
        elif action == self.ACTIVATE_SENSOR:
            pass
        elif action == self.DEACTIVATE_SENSOR:
            pass
        elif action == self.ADD_MEDIA_CONTENT:
            # Add media content to the Venue object
            # It adds the content to all the sensors attached to the venue.
            campid = action_args['id'] if 'id' in action_args else None
            if campid is None:
                return JSONResponse('content id cannot be None for action type'
                                    ' %s' % self.ADD_MEDIA_CONTENT,
                                    status=HTTP_400_BAD_REQUEST)
            # error strings
            rcs = {}
            somefailed = False
            # get the campaign
            campaign = Campaign.objects.get(id=campid)
            # Get the sensors attached to the venue object
            for sensor in venue.sensors:
                _nv = {'source_type': 'sensor',
                       'start_date': action_data['start_date'],
                       'end_date': action_data['end_date']}
                _playing_data = json.loads(
                                    str(self.playing_template.render(**_nv)))
                playing = PlayingSerializer(data=_playing_data)
                # validate what we get
                playing.is_valid(raise_exception=True)
                # Check if there is a playing object already for the
                # campaign and source combination.
                plays = Playing.objects.filter(playing_content=campaign,
                                               primary_media_source=sensor)
                # Expect only one play per campaign, sensor pair
                play = plays[0] if plays else None
                if play:
                    # Update the playing object with incoming request
                    playing.update(play, playing.validated_data)
                    if play.state == 'ok':
                        rc = self._update_campaign_to_sensors(play=play,
                                                              sensor=sensor,
                                                              campaign=campaign)
                    else:
                        # Try to post the campaign to vendor once again
                        # after an earlier attempt.
                        rc = self._publish_campaign_to_sensors(play=play,
                                                               sensor=sensor,
                                                               campaign=campaign)
                        if rc != 0:
                            # Set the playing state to error.
                            play.update(state='error')
                            rcs[str(sensor.id)] = 'error'
                            somefailed = True
                        else:
                            # Set the playing state to error.
                            play.update(state='ok')
                else:
                    play = playing.save()
                    play.update(primary_media_source=sensor,
                                playing_content=campaign)
                    # Push the tasks to respective vendors.
                    rc = self._publish_campaign_to_sensors(play=play,
                                                           sensor=sensor,
                                                           campaign=campaign)
                    if rc != 0:
                        # Set the playing state to error.
                        play.update(state='error')
                        rcs[str(sensor.id)] = 'error'
                        somefailed = True
                    else:
                        # Set the playing state to error.
                        play.update(state='ok')
            if not venue.sensors:
                return JSONResponse("No sensors to play campaign",
                                    status=HTTP_204_NO_CONTENT)
            elif somefailed:
                failed_attach = [key for key in rcs.keys() if rcs[key] != 0]
                return JSONResponse("Playing failed on sensors %s" % failed_attach,
                                    status=HTTP_200_OK)
            else:
                return JSONResponse("Playing started",
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
            for sensor in venue.sensors:
                play = Playing.objects.get(primary_media_source=sensor,
                                           playing_content=campaign)
                if play.pause_playing is False:
                    play.pause_playing = True
                    play.save()
                # Pause the content by passing the command to driver
                self._control_campaign_on_sensors(play=play,
                                                  sensor=sensor,
                                                  campaign=campaign,
                                                  update='pause')
            if not venue.sensors:
                return JSONResponse("No sensors playing the campaign",
                                    status=HTTP_204_NO_CONTENT)
            return JSONResponse("Playing stopped",
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
            for sensor in venue.sensors:
                play = Playing.objects.get(primary_media_source=sensor,
                                           playing_content=campaign)
                if play.pause_playing is True:
                    play.pause_playing = False
                    play.save()
                # Resume the content by passing the command to driver
                self._control_campaign_on_sensors(play=play,
                                                  sensor=sensor,
                                                  campaign=campaign,
                                                  update='resume')
            return JSONResponse("Campaign resumed",
                                status=HTTP_200_OK)
        elif action == self.FILTER_BY_MEDIAAGGREGATE:
            maid = action_args['id'] if 'id' in action_args else None
            if maid is None:
                return JSONResponse('media aggregate id cannot be None for action type'
                                    ' %s' % self.FILTER_BY_MEDIAAGGREGATE,
                                    status=HTTP_400_BAD_REQUEST)
            # get the MA
            ma = MediaAggregate.objects.get(id=maid)
            src = ma.inhouse_source
            if src is None:
                return JSONResponse('Mediaaggregate with source none, uncommon!'
                                    ' %s' % self.FILTER_BY_MEDIAAGGREGATE,
                                    status=HTTP_500_INTERNAL_SERVER_ERROR)
            venues = Venue.objects.filter(source=src)
            venser = VenueSerializer(venues, many=True)
            return JSONResponse(venser.data,
                                status=HTTP_200_OK)
        else:
            pass


class OnlineMediaController():

    ADD_MEDIA_CONTENT = 'addcontent'

    def __init__(self):
        self.playing_template = Template(
                               open('%s%s' % (settings.MEDIAAPP_DIR,
                                    'templates/playing.j2'),
                                    'r').read())

    def handle_update(self, inst, *args, **kwargs):
        pass

    def handle_operations(self, online, action, action_args, action_data):
        # action= add media etc., action_args= content-id, action_data= {}
        print 'OnlineMediaController: Performing action %s' % action

        if action == self.ADD_MEDIA_CONTENT:
            # Add media content to OOH Media source object
            campid = action_args['id'] if 'id' in action_args else None
            if campid is None:
                return JSONResponse('content id cannot be None for action type'
                                    ' %s' % self.ADD_MEDIA_CONTENT,
                                    status=HTTP_400_BAD_REQUEST)
            # get the campaign
            campaign = Campaign.objects.get(id=campid)
            _nv = {'source_type': 'online',
                   'start_date': action_data['start_date'],
                   'end_date': action_data['end_date']}
            _playing_data = json.loads(
                                str(self.playing_template.render(**_nv)))
            playing = PlayingSerializer(data=_playing_data)
            if playing.is_valid(raise_exception=True):
                play = playing.save()
                play.update(primary_media_source=online,
                            playing_content=campaign)
                return JSONResponse(playing.validated_data,
                                    status=HTTP_200_OK)
        else:
            # Unknown operation
            pass


class OOHMediaController():

    ADD_VENUE = 'addvenue'
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
        elif action == self.ADD_VENUE:
            # Add venue to OOH Media source object
            # Venue has sensors that can detect users
            venueid = action_args['id'] if 'id' in action_args else None
            if venueid is None:
                return JSONResponse('venue id cannot be None for action type'
                                    ' %s' % self.ADD_VENUE,
                                    status=HTTP_400_BAD_REQUEST)
            # get the venue and update
            venue = Venue.objects.get(id=venueid)
            venue.source = ooh
            venue.save()
            return JSONResponse("venue updated with source information",
                                status=HTTP_200_OK)
        else:
            # Unknown operation
            pass


class MediaAggregateController():

    ADD_VENUE = 'addvenue'
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
        elif action == self.ADD_VENUE:
            # Add venue to a media source object
            # Venue has sensors that can detect users
            venueid = action_args['id'] if 'id' in action_args else None
            if venueid is None:
                return JSONResponse('venue id cannot be None for action type'
                                    ' %s' % self.ADD_VENUE,
                                    status=HTTP_400_BAD_REQUEST)
            # get the venue and update
            venue = Venue.objects.get(id=venueid)
            venue.source = amenity.inhouse_source
            venue.save()
            return JSONResponse("venue updated with source information",
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

    def __init__(self):
        '''
        Constructor
        '''
        param = {
            'default_ini': '%s%s' % (settings.MEDIAAPP_DIR, 'mediaconfig.ini'),
            'default_value_map': {}
            }

        self.cfg = Config.config(**param)
        self.type = self.cfg.get_config(
                                        'campaign.tracking', 'driver')
        if self.type == 'tinyurl':
            self.driver = TinyUrlDriver()
        else:
            self.driver = Series5UrlDriver()

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

    def update_nearby_fields(self, camp):
        near_by_args = {"short_url": camp.home_url}
        if camp:
            tiny_url = self.driver.get_URL(
                                    camp.home_url,
                                    urlmeta={'campaignId': camp.id})
            near_by_args["short_url"] = tiny_url
        return near_by_args

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
