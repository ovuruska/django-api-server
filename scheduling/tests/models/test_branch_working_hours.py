import datetime
from random import randint

from django.test import TestCase

from common import Mock


class BranchWorkingHoursTestCase(TestCase):
	root_url = "/api/scheduling/hours/branch"
	all_zero = "".join(["0" for _ in range(24)])
	first = "".join([str(randint(0, 1)) for _ in range(24)])
	second = "".join([str(randint(0, 1)) for _ in range(24)])

	def setUp(self) -> None:
		self.mock = Mock(number_of_appointments=500)
		self.data = self.mock.generate()

	def tearDown(self) -> None:
		self.mock.remove(self.data)

	def test_add_working_hours(self):
		branch_id = 1
		body = {
			"branch": branch_id,
			"weekDay": 1,
			"workingHours": self.first
		}

		resp = self.client.post(self.root_url, body)
		self.assertEqual(resp.status_code, 201)
		self.assertEqual(resp.data, body)

	def test_get_working_hours(self):
		branch_id = 1

		body = {
			"branch": branch_id,
			"weekDay": 1,
			"workingHours": self.first
		}

		start = datetime.datetime.now().strftime("%Y-%m-%d")
		end = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
		resp = self.client.get(self.root_url + "?id=" + str(branch_id) + "&start=" + start + "&end=" + end)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(len(resp.data), 1)
		self.assertEqual(resp.data[0]["workingHours"], self.first)

	def test_update_working_hours(self):
		branch_id = 1
		body = {
			"branch": branch_id,
			"weekDay": 1,
			"workingHours": self.first
		}

		resp = self.client.post(self.root_url, body)
		self.assertEqual(resp.status_code, 201)
		self.assertEqual(resp.data, body)

		body = {
			"branch": branch_id,
			"weekDay": 1,
			"workingHours": self.second
		}

		resp = self.client.post(self.root_url, body)
		self.assertEqual(resp.status_code, 201)
		self.assertEqual(resp.data, body)

		start = datetime.datetime.now().strftime("%Y-%m-%d")
		end = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
		resp = self.client.get(self.root_url + "?id=" + str(branch_id) + "&start=" + start + "&end=" + end)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(len(resp.data), 1)
		self.assertEqual(resp.data[0]["workingHours"], self.second)

	def test_working_hours_weekly(self):
		branch_id = 1
		body = {
			"branch": branch_id,
			"weekDay": 1,
			"workingHours": self.first
		}

		resp = self.client.post(self.root_url, body)
		self.assertEqual(resp.status_code, 201)
		self.assertEqual(resp.data, body)

		body = {
			"branch": branch_id,
			"weekDay": 1,
			"workingHours": self.second
		}

		resp = self.client.post(self.root_url, body)
		self.assertEqual(resp.status_code, 201)
		self.assertEqual(resp.data, body)

		days = 8

		start = datetime.datetime.now().strftime("%Y-%m-%d")
		end = (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
		resp = self.client.get(self.root_url + "?id=" + str(branch_id) + "&start=" + start + "&end=" + end)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(len(resp.data), days)
		self.assertEqual(resp.data[0]["workingHours"], self.second)
		for i in range(1, 7):
			self.assertEqual(resp.data[i]["workingHours"], self.all_zero)
		self.assertEqual(resp.data[7]["workingHours"], self.second)
