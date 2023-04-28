import django
from django.apps import apps
from rest_framework import generics
from rest_framework.response import Response

from common.validate_request import validate_request
from customer.selectors.pet_details import get_customer_pet_details
from customer.serializers.requests.pet import CreatePetRequestSerializer
from customer.serializers.responses.pet_details import CustomerPetDetailsResponseSerializer

Dog = apps.get_model("scheduling", "Dog")


class GetCustomerPetDetails(generics.ListAPIView):
	serializer_class = CustomerPetDetailsResponseSerializer

	def get_queryset(self):
		customer = self.request.user.customer
		return get_customer_pet_details(customer)


class CustomerCreatePetView(generics.CreateAPIView):
	serializer_class = CustomerPetDetailsResponseSerializer

	@validate_request(CreatePetRequestSerializer)
	def create(self, request, *args, **kwargs):
		serialized_data = kwargs.get("serialized_data")
		customer = request.user.customer
		pet_name = serialized_data.get("name")
		try:
			pet = Dog.objects.create(owner=customer, name=pet_name, breed=serialized_data.get("breed"),birth_date=serialized_data.get("birth_date"),
			                         rabies_vaccination=serialized_data.get("rabies_vaccination"),
			                         customer_notes=serialized_data.get("special_handling"),
				age=serialized_data.get("age"), weight=serialized_data.get("weight"), gender=serialized_data.get("gender"))
		except django.db.utils.IntegrityError:
			return Response({"message": "Pet already exists"}, status=400)
		pet_details = get_customer_pet_details(customer, pet_name)

		serializer = CustomerPetDetailsResponseSerializer(pet_details[0])

		return Response(serializer.data)
