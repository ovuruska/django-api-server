from django.apps import apps
from django.urls import reverse
from rest_framework import status
from common.auth_test_case import EmployeeAuthTestCase
from faker import Faker
from scheduling.models import Employee, Branch, Service, Product

Customer = apps.get_model('scheduling', 'Customer')
Dog = apps.get_model('scheduling', 'Dog')
class TestAppointmentEmployeeCreateAPIView(EmployeeAuthTestCase):
	url = reverse('scheduling/appointment-employee-create')

	def setUp(self):
		super().setUp()
		fake = Faker()

		self.customer = Customer.objects.create(name="John Doe")
		self.dog = Dog.objects.create(name='Fido', breed='Labrador', age=5, owner=self.customer)
		self.branch = Branch.objects.create(name='Main Branch', address='123 Main St')
		self.service = Service.objects.create(name='Bath', description='Dog bath service', cost=25.0,
		                                      duration=fake.time_delta())
		self.product = Product.objects.create(name='Shampoo', description='Dog shampoo', cost=10.0)

	def tearDown(self):
		super().tearDown()
		self.service.delete()
		self.product.delete()
		self.branch.delete()

	def test_valid_data(self):
		data = {
		  "pet": 1,
		  "customer": 1,
		  "employee": 1,
		  "branch": 1,
		  "start": "2019-08-24T14:15:22Z",
		  "end": "2019-08-24T14:35:22Z",
		  "products": [],
		  "service": "string"
		}
		response = self.client.post(self.url, data=data, format='json',**self.employee_headers)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)


	def test_with_missing_data(self):
		data = {
			"pet": 1,
			"customer": 1,
			"employee": 1,
			"branch": 1,
			"products": [],
			"service": "string"
		}
		response = self.client.post(self.url, data=data, format='json', **self.employee_headers)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_with_missing_product_validate(self):
		data = {
		  "pet": 1,
		  "customer": 1,
		  "employee": 1,
		  "branch": 1,
		  "start": "2019-08-24T14:15:22Z",
		  "end": "2019-08-24T14:35:22Z",
		  "service": "string"
		}
		response = self.client.post(self.url, data=data, format='json',**self.employee_headers)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)