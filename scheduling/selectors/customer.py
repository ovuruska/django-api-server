

from django.apps import apps
from django.db.models import Sum


def get_customer_lifetime_product_invoice(customer_id):
	"""
	:param customer_id: The id of the customer
	:return: The lifetime invoice of the customer
	"""
	Appointment = apps.get_model('scheduling', 'Appointment')

	return Appointment.objects.filter(customer__id=customer_id,status=Appointment.Status.COMPLETED).aggregate(Sum('products__cost'))


def get_customer_lifetime_service_invoice(customer_id):
	"""
	:param customer_id: The id of the customer
	:return: The lifetime invoice of the customer
	"""
	Appointment = apps.get_model('scheduling', 'Appointment')

	return Appointment.objects.filter(customer__id=customer_id,status=Appointment.Status.COMPLETED).aggregate(Sum('services__cost'))


def get_customer_dogs(customer_id):
	"""
	:param customer_id: The id of the customer
	:return: A list of dogs that belong to the customer
	"""
	Dog = apps.get_model('scheduling', 'Dog')

	return Dog.objects.filter(owner__id=customer_id)


def get_customer_lifetime_tips(customer_id):
	"""
	:param customer_id: The id of the customer
	:return: The lifetime tip of the customer
	"""
	Appointment = apps.get_model('scheduling', 'Appointment')

	return Appointment.objects.filter(customer__id=customer_id,status=Appointment.Status.COMPLETED).aggregate(Sum('tip'))