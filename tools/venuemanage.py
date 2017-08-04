'''
Created on Feb 7, 2016

@author: sonu
'''
import os
import sys
from datetime import datetime, timedelta
import json
import requests
import re
import pika

import time
from optparse import OptionParser

ADWISE_URL = "http://127.0.0.1:8000"
AMQP_URL = "amqp://mrafhtxb:HuPwIQDIAxoC3HQTuyHluZPULpR6uReS@white-mynah-bird.rmq.cloudamqp.com/mrafhtxb"
NIKAZA_URL = "https://nikaza.io/"


def print_table(items, header=None, wrap=True, max_col_width=20, wrap_style="wrap", row_line=False, fix_col_width=False):
    ''' Prints a matrix of data as a human readable table. Matrix
    should be a list of lists containing any type of values that can
    be converted into text strings.

    Two different column adjustment methods are supported through
    the *wrap_style* argument:

       wrap: it will wrap values to fit max_col_width (by extending cell height)
       cut: it will strip values to max_col_width

    If the *wrap* argument is set to False, column widths are set to fit all
    values in each column.

    This code is free software. Updates can be found at
    https://gist.github.com/jhcepas/5884168

    '''

    if fix_col_width:
        c2maxw = dict([(i, max_col_width) for i in xrange(len(items[0]))])
        wrap = True
    elif not wrap:
        c2maxw = dict([(i, max([len(str(e[i])) for e in items])) for i in xrange(len(items[0]))])
    else:
        c2maxw = dict([(i, min(max_col_width, max([len(str(e[i])) for e in items])))
                        for i in xrange(len(items[0]))])
    if header:
        current_item = -1
        row = header
        if wrap and not fix_col_width:
            for col, maxw in c2maxw.iteritems():
                c2maxw[col] = max(maxw, len(header[col]))
                if wrap:
                    c2maxw[col] = min(c2maxw[col], max_col_width)
    else:
        current_item = 0
        row = items[current_item]
    while row:
        is_extra = False
        values = []
        extra_line = [""]*len(row)
        for col, val in enumerate(row):
            cwidth = c2maxw[col]
            wrap_width = cwidth
            val = str(val)
            try:
                newline_i = val.index("\n")
            except ValueError:
                pass
            else:
                wrap_width = min(newline_i+1, wrap_width)
                val = val.replace("\n", " ", 1)
            if wrap and len(val) > wrap_width:
                if wrap_style == "cut":
                    val = val[:wrap_width-1]+"+"
                elif wrap_style == "wrap":
                    extra_line[col] = val[wrap_width:]
                    val = val[:wrap_width]
            val = val.ljust(cwidth)
            values.append(val)
        print ' | '.join(values)
        if not set(extra_line) - set(['']):
            if header and current_item == -1:
                print ' | '.join(['='*c2maxw[col] for col in xrange(len(row)) ])
            current_item += 1
            try:
                row = items[current_item]
            except IndexError:
                row = None
        else:
            row = extra_line
            is_extra = True

        if row_line and not is_extra and not (header and current_item == 0):
            if row:
                print ' | '.join(['-'*c2maxw[col] for col in xrange(len(row)) ])
            else:
                print ' | '.join(['='*c2maxw[col] for col in xrange(len(extra_line)) ])


class NikazaConnection(object):
    def __init__(self, endpoint, key):
        self._endpoint = endpoint
        self.SENSOR_API_ENDPOINT = "get_beacon_placement"
        self._key = key

    def load_sensors(self, venuename):
        data = {"venueName": venuename}
        datastr = json.dumps(data)
        api_endpoint = self._endpoint + self.SENSOR_API_ENDPOINT
        headers = {"Content-type": "application/json",
                   "APIKey": self._key,
                   "User-Agent": "series5"}
        response = requests.post(url=api_endpoint,
                                 headers=headers,
                                 data=datastr)
        venuedetail = json.loads(response.text)
        return venuedetail

    def persist_sensor(self, connection, venuename, venueid, sensordata):
        venues = sensordata["venues"] if "venues" in sensordata else None
        if venues:
            # get the venue
            venue = venues[0]
            numDevices = venue["noOfDevices"]
            devices = sensordata["zones"] if "zones" in sensordata else None
            if devices:
                for device in devices:
                    zone = device["zone"]
                    zoneId = device["zoneId"]
                    zoneObjectId = device['zoneObjectId']
                    lat = device["lat"]
                    lon = device["lon"]

                    sensor_data = {"name": zone,
                                   "display_name": zone,
                                   "caption": "Nikaza-" + zone,
                                   "uuid": zoneObjectId,
                                   "type": "beacon",
                                   "range": "10",
                                   "location": [lat, lon],
                                   "beacon_type": "ibeacon",
                                   "max_tx_power": "65",
                                   "vendor": "nikaza",
                                   "mac_address": "N/A",
                                   "sensor_meta": {"zoneId": zoneId}}
                    # create and attach the sensor to the venue
                    res = connection.persist_sensor(venueid, sensor_data)
                    if res:
                        print "Added sensor to venue %s" % venueid
                    else:
                        print "Failed adding sensor to venue %s" % venueid
        else:
            print "No venue in Nikaza by the name %s" % venuename


class CloudAMQPConnection(object):

    def __init__(self, endpoint):
        self._endpoint = endpoint

        params = pika.URLParameters(self._endpoint)
        params.socket_timeout = 5

        self._connection = pika.BlockingConnection(params)
        self._channel = self._connection.channel()
        self._queues = {}

    def create_queue(self, name):
        if self._channel:
            q = self._channel.queue_declare(queue=name)
            self._queues[name] = q
            return q
        else:
            return None

    def welcome_message(self, message, name):
        body = {
                "date": datetime.now(),
                "message": message
            }
        # send a message
        rc = self._channel.basic_publish(exchange='', routing_key=name,
                                         body=body)
        print " [x] Message sent to consumer "
        return True if rc else False

    def load_sensors(self, venuename):
        print "CloudAMQPConnection:load_sensors() venuename %s" % venuename

    def persist_sensor(self, connection, venuename, venueid, sensordata):
        print "CloudAMQPConnection:load_sensors() venuename %s" % venuename

    def close_connection(self):
        if self._connection:
            self._connection.close()


class AdwiseHttpConnection(object):

    def __init__(self, endpoint, user, passwd):
        self._endpoint = endpoint
        self.VENUE_URL = "/mediacontentapp/mediasource/venue/"
        self._user = user
        self._passwd = passwd

    @property
    def enpoint(self):
        return self._endpoint

    def persist_venue(self, name, address):
        api_endpoint = self._endpoint + "/mediacontent/mediasource/venue/"
        data = {"venue_name": name, "venue_address": address, "venue_meta": {}}
        data_str = json.dumps(data)
        headers = {"Content-type": "application/json",
                   "accept": "application/json",
                   "username": self._user,
                   "password": self._passwd,
                   "email": self._user}

        response = requests.post(url=api_endpoint,
                                 headers=headers,
                                 data=data_str)
        return response

    def list_venues(self):
        api_endpoint = self._endpoint + "/mediacontent/mediasource/venue/"
        headers = {"Content-type": "application/json",
                   "accept": "application/json",
                   "username": self._user,
                   "password": self._passwd,
                   "email": self._user}

        response = requests.get(url=api_endpoint,
                                headers=headers)
        if response.ok:
            resp = json.loads(response.text)
            return resp
        else:
            return None

    def persist_sensor(self, venueid, sensordata):
        rest_body = {"sensor_data": sensordata, "sensor_type": "Beacon"}
        api_endpoint = self._endpoint + (
                        "/mediacontent/mediasource/venue/%s/?action=attach" % (
                                                                        venueid))
        data_str = json.dumps(rest_body)
        headers = {"Content-type": "application/json",
                   "accept": "application/json",
                   "username": self._user,
                   "password": self._passwd,
                   "email": self._user}
        response = requests.post(url=api_endpoint,
                                 headers=headers,
                                 data=data_str)
        if response.ok:
            resp = json.loads(response.text)
            return resp
        else:
            return None


def load_sensors(options, endpointtype, venuename, venueid, save=False):
    types = endpointtype.split(',')
    for etype in types:
        if etype == 'nikaza':
            ne = NikazaConnection(NIKAZA_URL, options.nikazapasswd)
        elif etype == 'nearby':
            ne = CloudAMQPConnection(AMQP_URL)
        else:
            print "unknown endpoint type %s" % endpointtype
            continue
        sensors = ne.load_sensors(venuename)
        if ne and save and sensors:
            ne.persist_sensor(AdwiseHttpConnection(ADWISE_URL,
                                                   options.adwiseuser,
                                                   options.adwisepasswd),
                              venuename,
                              venueid,
                              sensors)


def prep_venue(name, address, user, passwd):
    connection = AdwiseHttpConnection(ADWISE_URL, user, passwd)
    cloud = CloudAMQPConnection(AMQP_URL)

    adwiseresp = connection.persist_venue(name, address)
    if adwiseresp.ok:
        amqpresp = cloud.create_queue(name)
        return (adwiseresp, amqpresp)
    return (adwiseresp, None)


def list_venue(user, passwd):
    connection = AdwiseHttpConnection(ADWISE_URL, user, passwd)
    resp = connection.list_venues()
    if resp:
        return venue_summary(resp)


def venue_summary(venuedata):
#     [
#      [3,2, {"whatever": 1, "bla": [1,2]}],
#      [5,"function",777],
#      [1,1,1]
#     ]
    venueRecords = []
    for venue in venuedata:
        _rec = [venue['venue_name'], venue['id'],
                {"queue-url": AMQP_URL,
                 "queue-id": [venue['venue_name'], venue['venue_name']+"_control"]},
                {"sensors": venue['sensors']}]
        venueRecords.append(_rec)

    print_table(venueRecords,
                header=[ "Venue Name", "Venue Id", "Message Queue", "Sensor Ids"],
                wrap=True, max_col_width=50, wrap_style='wrap',
                row_line=True, fix_col_width=False,)


def main(argv):
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-c", "--create-venue",
                      action="store_true", dest="create")
    parser.add_option("-v", "--venue-name", dest="venuename",
                      help="create venue by the name. Venue names have to be unique")
    parser.add_option("-a", "--venue-addr", dest="venueaddr")
    parser.add_option("-e", "--endpoint-type", dest="endpointtype",
                      help="endpoint type supported are 'nikaza' and 'nearby'")
    parser.add_option("-l", "--load-sensor", action="store_true", dest="load")
    parser.add_option("-m", "--list-venue", action="store_true", dest="listvenue")
    parser.add_option("-s", "--show-venue", action="store_true", dest="show")
    parser.add_option("-p", "--adwise-user", dest="adwiseuser")
    parser.add_option("-q", "--adwise-passwd", dest="adwisepasswd",
                      help="Adwise  user access provided to You by Series-5")
    parser.add_option("-t", "--nikaza-key", dest="nikazapasswd")
    parser.add_option("-i", "--venue-id", dest="venueid")

    (options, args) = parser.parse_args()
    if not options.adwiseuser or not options.adwisepasswd:
        print "Usage error: Adwise access is required to do  operation."
        return -1
    if options.create:
        # create venue
        if options.venuename:
            (adwise, cloud) = prep_venue(
                             options.venuename,
                             options.venueaddr if options.venueaddr else "",
                             options.adwiseuser,
                             options.adwisepasswd)
            if adwise.ok:
                resp = json.loads(adwise.text)
                venue_summary([resp])
            else:
                print "Encountered error adding venue. %s" % adwise.text
            return 0
        else:
            print "Venue name is required."
            return -1
    elif options.load:
        # load sensor
        if not options.endpointtype:
            print "Usage error: endpoint is required to import sensors from."
            return -1
        if not options.venuename:
            print "Usage error: Venue name is required to import sensors to."
            return -1
        if not options.venueid:
            print "Usage error: VenueId is required to import sensors to."
            return -1
        if options.endpointtype == 'nikaza':
            if not options.nikazapasswd:
                print "Usage error: Nikaza access is required to import sensors."
                return -1
        # load sensor to a given venue
        resp = load_sensors(options,
                            endpointtype=options.endpointtype,
                            venuename=options.venuename,
                            venueid=options.venueid,
                            save=True)
        print resp
    elif options.show:
        # show all venues
        if not options.endpointtype:
            print "Usage error: endpointtype is required to show sensors available."
            return -1
        if not options.venuename:
            venuename = options.venuename
        else:
            venuename = "all"
        resp = load_sensors(
                    endpointtype=options.endpointtype,
                    venuename=venuename,
                    save=False)
        print resp
        return 0
    elif options.listvenue:
        list_venue(options.adwiseuser, options.adwisepasswd)
    else:
        print "Usage Error : unknown options"


if __name__ == '__main__':
    main(sys.argv[1:])