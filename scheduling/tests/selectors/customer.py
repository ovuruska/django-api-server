from django.test import TestCase

from scheduling.common import Mock
from scheduling.models import Appointment, Dog


class CustomerSelectorTestCase(TestCase):
	number_of_appointments = 500

	def setUp(self) :
		self.mock = Mock(number_of_appointments=self.number_of_appointments,number_of_services=5,number_of_products=10,number_of_dogs=5,number_of_customers=5)
		self.data = self.mock.generate()

	def tearDown(self) -> None:
		self.mock.remove(self.data)


	def test_get_customer_total_tips(self):
		customer_id = self.data["customers"][0].id
		response = self.client.get("/api/scheduling/customer/"+str(customer_id))
		self.assertEqual(response.status_code, 200)

		total_tips = 0
		for appointment in Appointment.objects.filter(customer__id=customer_id,status=Appointment.Status.COMPLETED):
			total_tips += appointment.tip
		self.assertEqual(response.data["lifetime_tips"], total_tips)

	def test_get_customer_dogs(self):
		customer_id = self.data["customers"][0].id
		response = self.client.get("/api/scheduling/customer/"+str(customer_id))
		self.assertEqual(response.status_code, 200)

		dogs = []
		for dog in Dog.objects.filter(owner__id=customer_id):
			dogs.append(dog)
		self.assertEqual(len(response.data["dogs"]), len(dogs))


	def test_get_customer_total_product_sales(self):
		customer_id = self.data["customers"][0].id
		response = self.client.get("/api/scheduling/customer/"+str(customer_id))
		self.assertEqual(response.status_code, 200)

		total_product_sales = 0
		for appointment in Appointment.objects.filter(customer__id=customer_id,status=Appointment.Status.COMPLETED):
			for product in appointment.products.all():
				total_product_sales += product.cost
		self.assertEqual(response.data["lifetime_product_sales"], total_product_sales)


	def test_get_customer_total_service_sales(self):
		customer_id = self.data["customers"][0].id
		response = self.client.get("/api/scheduling/customer/"+str(customer_id))
		self.assertEqual(response.status_code, 200)

		total_service_sales = 0
		for appointment in Appointment.objects.filter(customer__id=customer_id,status=Appointment.Status.COMPLETED):
			for service in appointment.services.all():
				total_service_sales += service.cost
		self.assertEqual(response.data["lifetime_service_sales"], total_service_sales)