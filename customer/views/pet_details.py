from rest_framework import generics

from customer.selectors.pet_details import get_customer_pet_details
from customer.serializers.responses.pet_details import CustomerPetDetailsResponseSerializer


class GetCustomerPetDetails(generics.ListAPIView):

	serializer_class = CustomerPetDetailsResponseSerializer

	def get_queryset(self):
		customer = self.request.user.customer
		return get_customer_pet_details(customer)

