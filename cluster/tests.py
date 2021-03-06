import unittest, json
from django.test import TestCase,Client
from cluster.clustering import *

# Create your tests here.
class visitRecordTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        response = self.client.get('/cluster_get/',{'d': "200",'t': "3",'c':"2"})

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        print(response.data)


        # Check that the rendered context contains 5 customers.
        # self.assertEqual(len(response.context['customers']), 5)

