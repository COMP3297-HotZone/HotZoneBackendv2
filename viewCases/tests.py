import unittest, json
from .models import CaseRecord
from django.test import TestCase,Client

# Create your tests here.
class AllCaseRecordTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a POST request.
        response = self.client.get('/all_caserecord_get/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # print(response.data)


        # Check that the rendered context contains 5 customers.
        # self.assertEqual(len(response.context['customers']), 5)

class SearchCaseRecordTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a POST request.
        response = self.client.post('/search_caserecord_post/',{'idNumber': 'Y321256(6)'})

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        print(response.data)

# class ViewCaseSerializerTest(unittest.TestCase):
#     def setUp(self):
#         # Every test needs a client.
#         self.client = Client()
    
#     def test_details(self):
#         allCase = CaseRecord.objects.all()
