from django.test import TestCase
import datetime

from io import BytesIO
from rest_framework.parsers import JSONParser
import json
from userapp.models import MediaUser
from models import Campaign, CampaignSpec
from testsdata import campaign_post_json_data, serviceuser_post_json_data, \
    campaign_update_post_json_data

from mongoengine import connect
from rest_framework.test import APIClient
from django.contrib.auth.models import User

_API_SERVER_URL = 'http://127.0.0.1:8000'
_API_USER_ROOT = '/users/'
_API_MEDIACONTENT_ROOT = '/mediacontent/'
_API_CAMPAIGN_RESOURCE = '/mediacontent/campaign/'


def parseJSON(response):
    stream = BytesIO(response.content)
    json = JSONParser().parse(stream)
    return json

# Create your tests here.


class MediaContentTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        TestCase.tearDown(self)


class SwaggerIntegrationTestCase(TestCase):
    def test_no_permission(self):
        response = self.client.get('%s/%s'
                                   % (_API_SERVER_URL, ''))
        self.assertEqual(response.status_code, 200)

    def test_campaign_serializer(self):
        response = self.client.get('%s/%s'
                                   % (_API_SERVER_URL,
                                      'api-docs/mediacontent'))
        self.assertEqual(response.status_code, 200)


class CampaignRestApiTestCase(TestCase):

    def _cleanUp(self):
        MediaUser.objects.all().delete()
        Campaign.objects.all().delete()
        User.objects.all().delete()

    def setUp(self):
        connect('rest_database', alias='default')
        self._cleanUp()
        self.client = APIClient()
        self.test_user = json.loads(serviceuser_post_json_data)
        # Creates default user for testing function
        response = self.client.post(_API_USER_ROOT,
                                    data=serviceuser_post_json_data,
                                    content_type='application/json',
                                    HTTP_USERNAME=self.test_user['user']['username'],
                                    HTTP_PASSWORD=self.test_user['user']['password'],
                                    HTTP_EMAIL=self.test_user['user']['email'])
        self.assertEqual(response.status_code, 201)

    def tearDown(self):
        TestCase.tearDown(self)
        MediaUser.objects.all().delete()
        Campaign.objects.all().delete()
        User.objects.all().delete()

    def test_create_campaign(self):
        req_json = json.loads(campaign_post_json_data)
        response = self.client.post(_API_CAMPAIGN_RESOURCE,
                                    data=campaign_post_json_data,
                                    content_type='application/json',
                                    HTTP_USERNAME=self.test_user['user']['username'],
                                    HTTP_PASSWORD=self.test_user['user']['password'],
                                    HTTP_EMAIL=self.test_user['user']['email'])
        self.assertEqual(response.status_code, 201)
        res_json = parseJSON(response)
        _camp = Campaign.objects.filter(name=req_json['name'])
        self.assertTrue(len(_camp) > 0)
        self.assertTrue(_camp[0] is not None)
        self.assertTrue(_camp[0].id is not None)
        self.assertTrue(_camp[0].spec.linked_source_ids is not None)
        self.assertTrue(len(_camp[0].spec.linked_source_ids) == len(
                                                req_json['spec']['linked_source_ids']))
        camp = _camp[0]
        # Update the campaign
        req_update_json = json.loads(campaign_update_post_json_data)
        response = self.client.post('%s%s/' % (
                                        _API_CAMPAIGN_RESOURCE, _camp[0].id),
                                    data=campaign_update_post_json_data,
                                    content_type='application/json',
                                    HTTP_USERNAME=self.test_user['user']['username'],
                                    HTTP_PASSWORD=self.test_user['user']['password'],
                                    HTTP_EMAIL=self.test_user['user']['email'])
        self.assertEqual(response.status_code, 200)
        _updated_camp = Campaign.objects.get(id=camp.id)
        self.assertTrue(_updated_camp is not None)
        self.assertTrue(
            req_update_json['spec']['linked_source_ids'][0] in _updated_camp.spec.linked_source_ids)



