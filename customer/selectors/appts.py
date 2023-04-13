from datetime import datetime

from django.apps import apps

Appointment = apps.get_model('scheduling', 'Appointment')
def get_customer_past_appts(customer):

	past_appts = Appointment.objects.filter(customer=customer, start__lt=datetime.now())
	return past_appts

def get_customer_upcoming_appts(customer):

	upcoming_appts = Appointment.objects.filter(customer=customer, start__gt=datetime.now())
	return upcoming_appts

def get_customer_all_appts(customer):
	all_appts = Appointment.objects.filter(customer=customer)
	return all_appts
