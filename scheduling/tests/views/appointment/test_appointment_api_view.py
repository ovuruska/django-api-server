from django.test import TestCase


from rest_framework.test import APIClient

class TestAppointmentModifyAPIView(TestCase):

        def setUp(self):
            self.client = APIClient()

        def test_appointment_modify_api_view(self):
            response = self.client.get('/api/appointment/modify/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, [])