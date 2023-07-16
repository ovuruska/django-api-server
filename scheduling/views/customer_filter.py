from django.apps import apps
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from drf_yasg import openapi
from common.search_pagination import SearchPagination
from scheduling.serializers.Customer import CustomerSerializer
from scheduling.serializers.Dog import DogSerializer

Customer = apps.get_model('scheduling', 'Customer')


class CustomerFilterAPIView(ListAPIView):
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

	@swagger_auto_schema(tags=['customers'])
	def get(self,*args,**kwargs):
		return super().get(*args,**kwargs)

class CustomerPetsListAPIView(ListAPIView):
	Pet = apps.get_model('scheduling', 'Dog')
	serializer_class = DogSerializer
	queryset= Pet.objects.all()

	filter_backends = [DjangoFilterBackend]

	def get_queryset(self):
		if 'pk' in self.kwargs:
			pk = self.kwargs['pk']
			queryset = self.Pet.objects.all().filter(owner=pk)
			return queryset
		return self.queryset.none()

	@swagger_auto_schema(tags=['customers'])
	def get(self,*args,**kwargs):
		return super().get(*args,**kwargs)

class CustomerListView(ListAPIView):
	@swagger_auto_schema(
		tags=['customers'],
		manual_parameters=[
			openapi.Parameter('sort', openapi.IN_QUERY, description="Sort by field", type=openapi.TYPE_STRING,
			                  default='name'),
			openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER,
			                  default=0),
			openapi.Parameter('pageCount', openapi.IN_QUERY, description="Items per page", type=openapi.TYPE_INTEGER,
			                  default=20),
			openapi.Parameter('name', openapi.IN_QUERY, description="Filter by name", type=openapi.TYPE_STRING),
		],
		responses={
			200: openapi.Response(description="List of Customers", schema=openapi.Schema(
				type=openapi.TYPE_OBJECT,
				properties={
					'total_items': openapi.Schema(type=openapi.TYPE_INTEGER),
					'items': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
						type=openapi.TYPE_OBJECT,
						properties={
							'name': openapi.Schema(type=openapi.TYPE_STRING),
							'email': openapi.Schema(type=openapi.TYPE_STRING),
							# Add other fields...
						})),
				}
			))
		}
	)
	def get(self, request, *args, **kwargs):
		# Retrieve query parameters
		sort = request.GET.get('sort', 'name')
		page = int(request.GET.get('page', '0'))
		page_count = int(request.GET.get('pageCount', '20'))
		name_query = request.GET.get('name')

		# Create a Q object for name__icontains filter
		name_filter = Q()
		if name_query:
			name_filter |= Q(name__icontains=name_query)
		# Retrieve and filter the customers
		customers = Customer.objects.filter(name_filter).order_by(sort)

		# Use Django's built-in pagination
		paginator = Paginator(customers, page_count)

		try:
			customers = paginator.page(page + 1)
		except Exception:
			return JsonResponse({'items':[],'total_items':paginator.count})

		# Prepare the response
		customer_list = list(customers.object_list.values())
		response = {
			'total_items': paginator.count,
			'items': customer_list
		}

		return JsonResponse(response)