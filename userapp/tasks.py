'''
Created on Dec 30, 2015

@author: sonu
'''

from __future__ import absolute_import

from celery import shared_task
from mediacontentapp.models import ImageAd


@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param


@shared_task
def fetch_ad(user, geopoint):
    print 'Fetching ad for the user {%s} at location (%s)' % (
                                user['username'], geopoint['point'])
    # TBD: Actual work pending.
    # Step1 : Search for the Ad by location
    # Step2 : Deliver it via a driver (django-instapush)
    # TBD: Testing in progress
    ads = ImageAd.objects(
                ad_location_tag__near=geopoint['point'])
    print ads
    pass
