from django.test import TestCase ,Client
from rest_framework import status
from .models import Patient

# Create your tests here.
class createTestRecordApitest(TestCase):
    def setUp(self):
        self.client = Client()
        self.valid_data = {
            "patient_id":127,
            "test_name":"CHOL",
            "value":30,
            "unit":"mg/dl",
            "is_abnormal":1,
        }
        self.invalid_data = {
            "patient_id":129,
            "test_name":"COL",
            "value" : -30,
            "unit":"mg/dl",
            "is_abnormal":1,
        }
    
    def test_create_test_record_valid_data(self):
        response = self.client.post('/api/tests/', self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['test_name'], self.valid_data['test_name'])

    def test_create_test_record_invalid_data(self):
        response = self.client.post('/api/tests/', self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('test_name', response.data)
        self.assertIn('value', response.data)

class GetPatientTestsAPItestcases(TestCase):
    def setUp(self):
        self.client = Client()
        self.patient = Patient.objects.create( 
            patient_id=140,
            test_name="COL",
            value =30,
            unit="mg/dl",
            is_abnormal=1,)
        self.patient_id = self.patient.patient_id
    def test_get_tests_for_patients(self):
        response = self.client.get(f'/api/tests/?patient_id={self.patient_id}')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertContains(response,self.patient.test_name)

   

