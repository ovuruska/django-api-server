from django.apps import apps
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from common.search_pagination import SearchPagination
from scheduling.serializers.Customer import CustomerSerializer


class CustomerFilterAPIView(ListAPIView):
	Customer = apps.get_model('scheduling', 'Customer')
	serializer_class = CustomerSerializer
	filter_backends = [DjangoFilterBackend]
	queryset = Customer.objects.all()
	filterset_fields = "__all__"




class CustomerFilterAPIView2(CustomerFilterAPIView):
	pagination_class = SearchPagination
	def get_queryset(self):
		# Get query params
		queryset = super().queryset

		query_params = self.request.query_params
		if query_params is not None:

			name_contains = query_params.get('name__in', "")
			queryset = queryset.filter(
				Q(name__icontains=name_contains)
			)

		return queryset

