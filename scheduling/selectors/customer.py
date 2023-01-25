

from django.apps import apps

def get_customer_lifetime_invoice(customer_id):
	"""
	:param customer_id: The id of the customer
	:return: The lifetime invoice of the customer
	"""
	Appointment = apps.get_model('scheduling', 'Appointment')

	return Appointment.filter(customer_id=customer_id,status=Appointment.Status.COMPLETED).aggregate(Sum('total_price'))