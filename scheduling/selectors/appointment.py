from scheduling.models import Appointment


def get_pending_appointments():
	"""
	:return: A list of appointments that are pending
	"""
	return Appointment.objects.filter(status=Appointment.Status.PENDING)

def get_appointment_by_id(appointment_id):
	"""
	:param appointment_id: The id of the appointment
	:return: The appointment with the given id
	"""
	return Appointment.objects.get(id=appointment_id)

def get_completed_appointments():
	"""
	:return: A list of appointments that are completed
	"""
	return Appointment.objects.filter(status=Appointment.Status.COMPLETED)


def get_cancelled_appointments():
	"""
	:return: A list of appointments that are cancelled
	"""
	return Appointment.objects.filter(status=Appointment.Status.CANCELLED)


def get_confirmed_appointments():
	"""
	:return: A list of appointments that are confirmed
	"""
	return Appointment.objects.filter(status=Appointment.Status.CONFIRMED)


def get_appointments_by_status(status):
	"""
	:param status: The status of the appointment
	:return: A list of appointments that match the status
	"""
	return Appointment.objects.filter(status=status)


def is_available(appointment_id):
	"""
	:param appointment_id: The id of the appointment
	:return: True if the appointment is available, False otherwise
	"""
	appointment = Appointment.objects.get(id=appointment_id)
	return appointment.is_available()


