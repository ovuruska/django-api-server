from scheduling.models import Appointment


def get_pending_appointments():
	"""
	:return: A list of appointments that are pending
	"""
	return Appointment.objects.filter(status=Appointment.Status.PENDING)


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





