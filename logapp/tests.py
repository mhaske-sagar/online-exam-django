import cmath
import unittest
from django.test import TestCase
from logapp.models import Userdata
from logapp.views import register
from faker import Faker
fake = Faker()

"""
class FirstTestCase(unittest.TestCase):

    
   
    def test_1(self):
        t = Userdata.objects.get(username='ab')
        self.assertEquals(t.username,'ab')
        self.assertEquals(t.password,'12345')

    def test_2(self):
        a=Userdata.objects.create(username="ab",password="1234",mobile_no=34567)
       
        self.assertEquals(a.username,'aa')
        self.assertEquals(a.password,"1234") 
    def test_3(self):
        a=Userdata.objects.create(username="abaaaaaaaaaaaaaaaaaaaaaaaaa",password="1234",mobile_no=34567)
        fake=len(a.username)
    
        self.assertLessEqual(fake,20) """
from rest_framework.test import APITestCase

   


    