from django.test import TestCase
from models import MediaUser
from io import BytesIO
from rest_framework.parsers import JSONParser
import json
from testsdata import user_post_json_data

from mongoengine import connect
from django.test.client import Client
from rest_framework.test import APIClient

_MOCK_ATTR_X1 = -123.0208
_MOCK_ATTR_X2 = 44.0464
_MOCK_ATTR_Y1 = 54.0000
_MOCK_ATTR_Y2 = 0.0
_API_SERVER_URL = 'http://127.0.0.1:8000'
_API_USER_ROOT = '/users/'
_API_ADVERTISER_ROOT = 'advertisers'


def parseJSON(response):
    stream = BytesIO(response.content)
    json = JSONParser().parse(stream)
    return json

# Create your tests here.


class MediaUserTestCase(TestCase):

    def setUp(self):
        connect('test_database', alias='default')
        MediaUser.objects.create(username="lion",
                                 password='lion',
                                 phone_number="roar",\
                                 city="remote", state='jungle',
                                 address='tourism',
                                 point=[_MOCK_ATTR_X1, _MOCK_ATTR_Y1])
        MediaUser.objects.create(username="cat",
                                 password='cat',
                                 phone_number='meow',
                                 city="suburb",
                                 state='house',
                                 address='pet',
                                 point=[_MOCK_ATTR_X2, _MOCK_ATTR_Y2])
        self.client = APIClient()

    def tearDown(self):
        MediaUser.objects.all().delete()
        TestCase.tearDown(self)

    def test_user_is_created(self):
        """Users created are correctly stored"""
        lion = MediaUser.objects.get(username="lion")
        cat = MediaUser.objects.get(username="cat")

        self.assertEqual(lion.phone_number, 'roar')
        self.assertEqual(cat.phone_number, 'meow')

        self.assertIsNotNone(lion.last_updated)
        self.assertIsNotNone(lion.date_joined)

    def test_user_is_updated(self):
        """Users updated are correctly stored"""
        lion = MediaUser.objects.get(username="lion")
        cat = MediaUser.objects.get(username="cat")

        lion.do_update(phone_number='meow')
        cat.do_update(phone_number='roar')

        self.assertEqual(lion.phone_number, 'meow')
        self.assertEqual(cat.phone_number, 'roar')

        self.assertLess(lion.date_joined, lion.last_updated)
        self.assertLess(cat.date_joined, cat.last_updated)

    def test_user_location_attr(self):
        """Users updated are correctly stored"""
        lion = MediaUser.objects.get(username="lion")
        cat = MediaUser.objects.get(username="cat")

        infocat = cat.point
        self.assertTrue(isinstance(cat.point, (list, tuple)))
        self.assertTrue(infocat[0] == _MOCK_ATTR_X2)
        self.assertTrue(infocat[1] == _MOCK_ATTR_Y2)

        infolion = lion.point
        self.assertTrue(isinstance(lion.point, (list, tuple)))
        self.assertTrue(infolion[0] == _MOCK_ATTR_X1)
        self.assertTrue(infolion[1] == _MOCK_ATTR_Y1)


class SwaggerIntegrationTestCase(TestCase):
    def test_no_permission(self):
        response = self.client.get('%s/%s'
                                   % (_API_SERVER_URL, ''))
        self.assertEqual(response.status_code, 200)

    def test_user_serializer(self):
        response = self.client.get('%s/%s'
                                   % (_API_SERVER_URL, 'api-docs/users'))
        self.assertEqual(response.status_code, 200)
        json = parseJSON(response)
        self.assertTrue('UserSerializer' in json['models'])


class UserAppRestApiTestCase(TestCase):
    def test_get_user(self):
        response = self.client.get(_API_USER_ROOT)
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        response = self.client.get(_API_USER_ROOT)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(_API_USER_ROOT,
                                    data=user_post_json_data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        res_json = parseJSON(response)
        req_json = json.loads(user_post_json_data)
        self.assertEqual(MediaUser.objects.count(), 1)
        self.assertEqual(res_json['username'], req_json['username'])
