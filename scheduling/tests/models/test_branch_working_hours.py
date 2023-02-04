import datetime
from random import randint
from common.mock_test_case import MockTestCase


class BranchWorkingHoursTestCase(MockTestCase):
	root_url = "/api/scheduling/hours/branch"
	all_zero = "".join(["0" for _ in range(24)])
	first = "".join([str(randint(0, 1)) for _ in range(24)])
	second = "".join([str(randint(0, 1)) for _ in range(24)])

	date = datetime.datetime.now()
	date_str = date.strftime("%Y-%m-%d")


	def test_add_working_hours(self):
		branch_id = 1
		body = {
			"branch": branch_id,
			"date": self.date_str,
			"working_hours": self.first
		}

		resp = self.client.post(self.root_url, body)

		self.assertEqual(resp.status_code, 200)
		self.assertEqual(resp.data["working_hours"], body["working_hours"])

	def test_get_working_hours(self):
		branch_id = 1

		body = {
			"branch": branch_id,
			"working_hours": self.first,
			"date": self.date_str

		}

		resp = self.client.post(self.root_url, body)
		self.assertEqual(resp.status_code, 200)

		start = self.date_str
		end = (self.date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
		resp = self.client.get(self.root_url + "?id=" + str(branch_id) + "&start=" + start + "&end=" + end)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(len(resp.data), 2)
		self.assertEqual(resp.data[0]["working_hours"], self.first)

	def test_update_working_hours(self):
		branch_id = 1
		body = {
			"branch": branch_id,
			"working_hours": self.first,
			"date":self.date_str
		}

		resp = self.client.post(self.root_url, body)
		self.assertEqual(resp.status_code, 200)

		body = {
			"branch": branch_id,
			"working_hours": self.second,
			"date": self.date_str

		}

		resp = self.client.post(self.root_url, body)
		self.assertEqual(resp.status_code, 200)

		start = self.date_str
		end = (self.date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
		resp = self.client.get(self.root_url + "?id=" + str(branch_id) + "&start=" + start + "&end=" + end)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(len(resp.data), 2)
		self.assertEqual(resp.data[0]["working_hours"], self.second)

	def test_working_hours_weekly(self):
		branch_id = 1
		body = {
			"branch": branch_id,
			"working_hours": self.first,
			"date": self.date_str

		}

		resp = self.client.post(self.root_url, body)
		self.assertEqual(resp.status_code, 200)

		body = {
			"branch": branch_id,
			"working_hours": self.second,
			"date": self.date_str

		}

		resp = self.client.post(self.root_url, body)
		self.assertEqual(resp.status_code, 200)

		days = 8

		start = self.date_str
		end = (self.date + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
		resp = self.client.get(self.root_url + "?id=" + str(branch_id) + "&start=" + start + "&end=" + end)
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(len(resp.data), days+1)
		self.assertEqual(resp.data[0]["working_hours"], self.second)
		for i in range(1, 7):
			self.assertEqual(resp.data[i]["working_hours"], self.all_zero)
		self.assertEqual(resp.data[7]["working_hours"], self.second)
