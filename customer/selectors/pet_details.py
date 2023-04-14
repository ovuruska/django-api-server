from django.apps import apps
from django.db.models import Count

Dog = apps.get_model("scheduling","Dog")
Appointment = apps.get_model("scheduling","Appointment")


def get_customer_pet_details(customer):

	dogs = Dog.objects.filter(owner=customer)

	dog_appts = Appointment.objects.filter(
		dog__in=dogs,
	)
	we_washes = dog_appts.filter(
		appointment_type=Appointment.AppointmentType.WE_WASH
	)
	groomings = dog_appts.filter(
		appointment_type=Appointment.AppointmentType.FULL_GROOMING
	)
	number_of_we_washes = we_washes.values('dog').annotate(number_of_we_washes=Count('dog'))
	number_of_groomings = groomings.values('dog').annotate(number_of_groomings=Count('dog'))
	we_washes_count_dict = {item['dog']: item['number_of_we_washes'] for item in number_of_we_washes}
	groomings_count_dict = {item['dog']: item['number_of_groomings'] for item in number_of_groomings}

	return [{
		**dog.to_dict(),
		"number_of_wewashes":we_washes_count_dict[dog.id],
		"number_of_groomings":groomings_count_dict[dog.id],
		"owner":customer.id
	} for dog in dogs]




