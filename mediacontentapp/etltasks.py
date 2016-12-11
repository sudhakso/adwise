'''
Created on April 1, 2016

@author: sonu
'''

from __future__ import absolute_import

from mediacontentapp.models import Amenity, NearBy, MediaSource
from mediacontentapp.templates import AmenityTemplate

from celery import Task
import overpy
import json
import datetime

# Initialize the service
# indexing_service = IndexingService()


class ExtractNearByAmenitiesTask(Task):
    ignore_errors = False
    _overpy = None

    @property
    def osmhandle(self):
        if self._overpy is None:
            self._overpy = overpy.Overpass()
        return self._overpy

    def run(self, querystr):
        print 'Running ExtractMapDataTask query %s...' % querystr
        nodes = []
        val = str(querystr)
        try:
            result = self.osmhandle.query(val)
            print 'Returning amenity nodes [%d]' % len(result.nodes)
            for node in result.nodes:
                nodes.append({'id': str(node.id),
                              'lat': str(node.lat),
                              'lon': str(node.lon),
                              'tags': node.tags})
            return json.dumps({"nodes": nodes})
        except Exception as e:
            print "ExtractNearByAmenitiesTask exception...."
            print e


class AddAmenitiesToBillboardTask(Task):
    ignore_errors = False

    def run(self, stringdata, billboard_id):
        print 'Running AddAmenitiesToBillboardTask...'
        # (param-1 : Billboard Id,
        #  param-2 : Amenity data)
        # Create "amenity" instance if not Found!
        # Add a "nearby" relation to the Amenity for the
        # billboard.
        try:
            amenitydata = json.loads(stringdata)
            print "Adding following amenities to billboard (%s)=>(%s)" % (
                                                        billboard_id,
                                                        amenitydata)
            bb = MediaSource.objects.get(id=billboard_id)
            # Span across all the amenities discovered.
            nodes = amenitydata['nodes'] if 'nodes' in amenitydata else []
            for node in nodes:
                print "Node discovered %s" % node
                amenity_qs = Amenity.objects.filter(node_id=node['id'])
                if amenity_qs:
                    # Amenity already added, just create a NearBy relation
                    amenity = amenity_qs[0]
                    print "Amenity already existing %s." % amenity.name
                else:
                    # Create amenity
                    data = {"id": node['id'],
                            "name": node['tags']['name'] if 'tags' in node else 'Not Available',
                            "type": node['tags']['amenity'] if 'tags' in node else 'Unknown',
                            "lat": node['lat'],
                            "lon": node['lon'],
                            "tags": node['tags'] if 'tags' in node else {},
                            "creation_date": datetime.datetime.now(),
                            "updation_date": datetime.datetime.now()
                            }
                    print "Creating amenity..."
                    print data
                    try:
                        templ = AmenityTemplate()
                        amenity = templ.create_instance(**data)
                    except Exception as e:
                        print "Error creating amenity. Failed with exception %s" % str(e)
                        continue
                print "Adding a near-by relation to (%s) for source (%s)" % (
                                                        amenity.name,
                                                        billboard_id)
                # Add NearBy relation to the amenity object
                nearby = NearBy(media_source=bb,
                                amenity=amenity,
                                creation_date=datetime.datetime.now(),
                                deletion_date=None)
                nearby.save()
        except Exception as e:
            print 'AddAmenitiesToBillboardTask exception...'
            print e

