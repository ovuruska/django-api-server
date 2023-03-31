from django.test import TestCase
from django.urls import reverse

from common.auth_test_case import EmployeeAuthTestCase

"""
from rest_framework import serializers


class MonthlyCapacityRequestSerializer(serializers.Serializer):
    employees = serializers.ListField(child=serializers.IntegerField(), required=False, default=[])
    branches = serializers.ListField(child=serializers.IntegerField(), required=False, default=[])
    service = serializers.CharField(required=True)
    date = serializers.CharField(required=True)
"""

class GetMonthlyCapacity400TestCase(EmployeeAuthTestCase):
	url = reverse("get_monthly_capacity")

	def test_with_invalid_data_1(self):

		data = {
			"employees": [1, 2],
			"branches": [1, 2],
			"service": "service",

		}

		response = self.client.post(self.url,data=data, **self.employee_headers)
		self.assertEqual(response.status_code, 400)

	def test_with_invalid_service_should_fail(self):

		data = {
			"employees": [1, 2],
			"branches": [1, 2],
			"date": "2023-04-01",
		}

		response = self.client.post(self.url, **self.employee_headers,data=data,format='json')
		self.assertEqual(response.status_code, 400)

	def test_with_invalid_date_should_fail(self):

		data = {
			"employees": [1, 2],
			"branches": [1, 2],
			"service": "service",
		}

		response = self.client.post(self.url, **self.employee_headers,data=data,format='json')
		self.assertEqual(response.status_code, 400)


	def test_400_on_non_existing_fields(self):

		data = {
			'date':'01/2019',
			'branch':[1],
			'employee':[1],
			'service':'We Wash'
		}

		response = self.client.post(self.url, **self.employee_headers, data=data, format='json')
		self.assertEqual(response.status_code, 400)