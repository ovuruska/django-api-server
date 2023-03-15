from collections import defaultdict
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from django.db.models import Sum

from django.apps import apps


def get_customer_invoice_distribution(customer_id):
	"""
	:param customer_id: The id of the customer
	:return: The invoice distribution for the customer
	"""
	Appointment = apps.get_model('scheduling', 'Appointment')

	appointments = Appointment.objects.filter(customer__id=customer_id)
	we_wash = appointments.filter( appointment_type='We Wash').aggregate(Sum('services__cost'))["services__cost__sum"] or 0

	grooming = appointments.filter( appointment_type='Full Grooming').aggregate(Sum('services__cost'))["services__cost__sum"] or 0

	tips = appointments.aggregate(Sum('tip'))["tip__sum"] or 0

	products = appointments.aggregate(Sum('products__cost'))["products__cost__sum"] or 0

	invoice_distribution = {
		'We Wash': float(round(we_wash,2)),
		'Full Grooming': float(round(grooming,2)),
		'Tips': float(round(tips,2)),
		'Products': float(round(products,2))
	}

	return invoice_distribution

def get_appointment_type_count_distribution(customer_id):
	Appointment = apps.get_model('scheduling', 'Appointment')

	appointments = Appointment.objects.filter(customer__id=customer_id)
	we_wash_count = appointments.filter( appointment_type='We Wash').count()
	grooming_count = appointments.filter( appointment_type='Full Grooming').count()
	return {
		'We Wash': we_wash_count,
		'Full Grooming': grooming_count
	}

def get_appointment_cancellation_rate(customer_id):
	Appointment = apps.get_model('scheduling', 'Appointment')

	appointments = Appointment.objects.filter(customer__id=customer_id)
	cancelled_appointments = appointments.filter(status='Cancelled').count()
	total_appointments = appointments.count()
	if total_appointments == 0:
		return 0
	return float(cancelled_appointments/total_appointments)

def get_appointment_no_show_rate(customer_id):
	Appointment = apps.get_model('scheduling', 'Appointment')

	appointments = Appointment.objects.filter(customer__id=customer_id)
	no_show_appointments = appointments.filter(status='No Show').count()
	total_appointments = appointments.count()
	if total_appointments == 0:
		return 0
	return float(no_show_appointments/total_appointments)


def get_yearly_appointment_summary(customer_id):
	Appointment = apps.get_model('scheduling', 'Appointment')


	start_date = (datetime.now() - timedelta(days=365)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
	end_date = datetime.now()


	appointments = Appointment.objects.filter(customer__id=customer_id, start__gte=start_date, end__lte=end_date)
	non_cancelled_appointments = appointments.exclude(status='Cancelled')
	summary = defaultdict(lambda: {
		"tip": 0,
		"we_wash": 0,
		"full_grooming": 0,
		"products": 0,
	})

	for appointment in non_cancelled_appointments:
		month = appointment.start.month
		summary[month]["tip"] += appointment.tip
		summary[month]["products"] += appointment.products.aggregate(sum=Sum('cost'))['sum'] or 0
		if appointment.appointment_type == 'We Wash':
			summary[month]["we_wash"] +=  appointment.services.aggregate(sum=Sum('cost'))['sum'] or 0
		else:
			summary[month]["full_grooming"] +=  appointment.services.aggregate(sum=Sum('cost'))['sum'] or 0
	for month in range(1, 13):
		if month not in summary:
			summary[month] = {
				"tip": 0,
				"we_wash": 0,
				"full_grooming": 0,
				"products": 0,
			}

	# Add month names to the summary
	sorted_summary =sorted(summary.items())
	# 01/01/2019
	date_summary = {
		(start_date + relativedelta(months=month)).strftime("%d-%m-%Y")
		: data
		for month, data in sorted_summary
	}

	return date_summary

