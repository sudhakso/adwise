from django.test import TestCase
import datetime
from models import MediaUser
from io import BytesIO
from rest_framework.parsers import JSONParser
import json
from testsdata import user_post_json_data,\
                user_service_post_json_data

from mongoengine import connect
from django.test.client import Client
from rest_framework.test import APIClient
from userapp.models import UserSession, UserService
from django.contrib.gis.geos.tests.test_geos_mutation import api_get_geom_typeid

_MOCK_ATTR_X1 = -123.0208
_MOCK_ATTR_X2 = 44.0464
_MOCK_ATTR_Y1 = 54.0000
_MOCK_ATTR_Y2 = 0.0
_API_SERVER_URL = 'http://127.0.0.1:8000'
_API_USER_ROOT = '/users/'
_API_USER_SERVICE_ROOT = '/users/services/'
_API_ADVERTISER_ROOT = 'advertisers'
_API_LOCATION_SERVICE_NAME = 'location'


_MOCK_SESSION_ID1 = '15d545b8-7cc7-4a8e-afa5-d5847a55be9f'
_MOCK_SESSION_ID2 = '15d545b8-7cc7-4a8e-afa5-d5847a55be9g'


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
        UserService.objects.all().delete()
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

    def test_user_multi_session(self):
        """Multiple Users session can be created"""
        lion = MediaUser.objects.get(username="lion")

        sess1 = UserSession.objects.create(session_id=_MOCK_SESSION_ID1,
                                           user_ref=lion)
        sess2 = UserSession.objects.create(session_id=_MOCK_SESSION_ID2,
                                           user_ref=lion)

        svc = UserService.objects.create(user_ref=lion, user_session=sess1,
                                         service_id=None, enabled=True,
                                         last_report_time=(
                                            datetime.datetime.now()),
                                         auto_restart=True)
        sess1.services.append(svc)
        sess2.services.append(svc)

        # Check the session count for the user
        sessions = UserSession.objects.filter(user_ref=lion)
        self.assertTrue(len(sessions), len((sess1, sess2)))

    def test_user_multi_service(self):
        """Multiple Users services can be created"""
        lion = MediaUser.objects.get(username="lion")

        sess = UserSession.objects.create(session_id=_MOCK_SESSION_ID1,
                                          user_ref=lion)

        svc1 = UserService.objects.create(user_ref=lion, user_session=sess,
                                          service_id=None, enabled=True,
                                          last_report_time=(
                                            datetime.datetime.now()),
                                          auto_restart=True)

        svc2 = UserService.objects.create(user_ref=lion, user_session=sess,
                                          service_id=None, enabled=True,
                                          last_report_time=(
                                            datetime.datetime.now()),
                                          auto_restart=True)
        sess.services.append(svc1)
        sess.services.append(svc2)

        # Check the session count for the user
        created_svc = UserService.objects.filter(user_ref=lion)
        self.assertTrue(len(created_svc), len(sess.services))


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

    def test_user_services_serializer(self):
        response = self.client.get('%s/%s'
                                   % (_API_SERVER_URL,
                                       'api-docs/users'))
        self.assertEqual(response.status_code, 200)
        json = parseJSON(response)
        self.assertTrue('UserServiceSerializer' in json['models'])


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

    def test_create_request_for_user(self):
        response = self.client.get(_API_USER_ROOT)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(_API_USER_ROOT,
                                    data=user_post_json_data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        res_json = parseJSON(response)

        apiurl = '%s%s/%s/' % (_API_USER_SERVICE_ROOT,
                               res_json['username'],
                               _API_LOCATION_SERVICE_NAME)
        print 'POST request %s' % (apiurl)
        print 'POST data %s' % (user_service_post_json_data)
        response = self.client.post(apiurl,
                                    data=user_service_post_json_data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        res_json = parseJSON(response)
        self.assertEqual(UserService.objects.count(), 1)
