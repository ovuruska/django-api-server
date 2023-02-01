from django.test import TestCase

from common import Mock


class EmployeeFilterTestCase(TestCase):

	root_url = "/api/employees"

	def setUp(self):
		self.mock = Mock()
		self.data = self.mock.generate()


	def tearDown(self):
		self.mock.remove(self.data)

	def test_get_all(self):
		response = self.client.get(self.root_url+"?")
		employees = self.data["employees"]
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), len(employees))


	def test_get_all_under_branch(self):
		branches = self.data["branches"]
		branch = branches[0]
		response = self.client.get(self.root_url+f"?branch={branch.id}")
		employees = self.data["employees"]
		employees = [employee for employee in employees if employee.branch.id == branch.id]
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), len(employees))

	def test_get_all_given_employee_name(self):
		employees = self.data["employees"]
		employee = employees[0]
		employee_name = employee.name
		response = self.client.get(self.root_url+f"?name={employee.name}")
		employees = [employee for employee in employees if employee.name == employee_name]
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.data), len(employees))