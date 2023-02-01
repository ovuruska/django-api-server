import datetime

from django.apps import apps


def update_customers():
	Customer = apps.get_model('scheduling', 'Customer')
	TopCustomer = apps.get_model('analytics', 'TopCustomer')
	Appointment = apps.get_model('scheduling', 'Appointment')

	customers = Customer.objects.all()
	for customer in customers:
		Appointment.objects.filter(customer=customer, )



def get_total_values_after_date(start_date: datetime.datetime):
	Appointment = apps.get_model('scheduling', 'Appointment')

	now = datetime.datetime.now()
	total_product_sales = 0
	total_service_sales = 0
	total_tips = 0


	appointments = Appointment.objects.filter(start_date__gte=start_date, status=Appointment.Status.COMPLETED,
	                                          start_date__lte=now)
	for appointment in appointments:
		for product in appointment.products.all():
			total_product_sales += product.cost
		for service in appointment.services.all():
			total_service_sales += service.cost
		total_tips += appointment.total_tips

	return total_product_sales, total_service_sales, total_tips