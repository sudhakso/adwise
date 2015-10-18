from django.test import TestCase
from models import MediaUser

from mongoengine import connect

# Create your tests here.
class MediaUserTestCase(TestCase):
    
    def setUp(self):
        connect('test_database', alias='default')        
        MediaUser.objects.create(username="lion", password='lion', phone_number="roar")
        MediaUser.objects.create(username="cat", password='cat', phone_number='meow')
        
    def tearDown(self):
        for auser in MediaUser.objects.all():
            auser.delete()
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
