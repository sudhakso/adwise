'''
Created on Jan 21, 2017

@author: sonu
'''
from __future__ import absolute_import

from celery import Task
from modeller.classifierclient import Classifier
from mediacontentapp.models import Amenity, NearBy
import json
from mediacontentapp.sourceserializers import MediaSourceSerializer


class ClassifierTask(Task):
    ignore_errors = True
    _clsifier = None

    @property
    def classifier(self):
        if self._clsifier is None:
            self._clsifier = Classifier()
        return self._clsifier

    def run(self, message):
        print 'Classifying %s ...' % message
        category = self.classifier.classify(message)

        print 'Classifier classified %s into category %s ...' % (
                                                    message, category)
        return category


class FindOOHFiltered(Task):
    # category = sports|bank etc..
    # filters =
    #    [
    #     {"type": "costfilter", "condition": "maximum", "value": "100000"},
    #     {"type": "dgfilter", "condition": "target", "value": "parents"}
    #    ]
    ignore_errors = True

    def run(self, category, filters):
        # TBD :  filters to be implemented!
        print 'FindOOHFiltered %s (%s)...' % (category, filters)
        amenities = Amenity.objects.filter(type=category)
        nearbys = NearBy.objects.filter(amenity__in=amenities)
        sources_relevant = [nearby.media_source for nearby in nearbys]
        ser_sources = MediaSourceSerializer(sources_relevant,
                                            many=True)
        _srjson = json.dumps(ser_sources.data, encoding='utf-8')
        return _srjson
