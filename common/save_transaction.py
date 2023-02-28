import datetime
from datetime import timezone

from django.apps import apps


def save_transaction(func):
	Transaction = apps.get_model("transactions", "Transaction")
	Appointment = apps.get_model("scheduling", "Appointment")
	def wrapper(self, request, *args, **kwargs):
		pk = self.kwargs.get("pk")
		appointment = Appointment.objects.get(id=pk)

		Transaction = apps.get_model("transactions", "Transaction")
		employee = None
		if request.user.is_authenticated:
			try:
				employee = request.user.employee
			except Exception as e:
				pass
		customer = None
		if request.user.is_authenticated:
			try:
				customer = request.user.customer
			except Exception as e:
				pass

		description = ""
		for key, value in request.data.items():
			original_value = getattr(appointment, key, None)
			if original_value is not None and original_value != value:
				description += f"{key} changed from {original_value} to {value}."



		transaction = Transaction(
			appointment=appointment,
			date=datetime.datetime.now(),
			action="modified appointment",
			description=description  # initialize the description
		)
		if employee is not None:
			transaction.employee = employee
		if customer is not None:
			transaction.customer = customer

		transaction.save()
		return func(self, request, *args, **kwargs)

	return wrapper