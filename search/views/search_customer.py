from django.db.models import Q, QuerySet
from rest_framework.generics import ListAPIView

from common.search_pagination import SearchPagination
from scheduling.models import Customer, Dog
from scheduling.serializers.Customer import CustomerDetailsSerializer


class SearchCustomerListView(ListAPIView):
	serializer_class = CustomerDetailsSerializer
	pagination_class = SearchPagination

	def get_queryset(self):
		queryset = Customer.objects.all()

		search = self.request.query_params.get('search', None)
		if search is not None:
			queryset = queryset.filter(
				Q(name__icontains=search) |
				Q(phone__icontains=search)
			)
			response = set(queryset)

			dog_queryset = Dog.objects.all().filter(
				Q(name__icontains=search)
			)

			for dog in dog_queryset:
				response.add(dog.owner)

			return list(response)

		else:
			return queryset