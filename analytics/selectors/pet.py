from django.apps import apps


def get_average_service_time(pet_id):
	Appointment = apps.get_model('scheduling', 'Appointment')
	appointments = Appointment.objects.all().filter(dog=pet_id)

	# TODO: Calculate average service time

	if len(appointments) == 0:
		return 0

	duration = 0
	for appointment in appointments:
		duration_timedelta = appointment.end - appointment.start
		duration += duration_timedelta.seconds//60
	return duration/len(appointments)