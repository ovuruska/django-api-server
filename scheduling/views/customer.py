from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response

from ..models import Dog
from ..models.customer import Customer
from ..serializers.Customer import CustomerSerializer, CustomerDetailsSerializer
from ..serializers.Dog import DogSerializer


class CustomerDogsRetrieveAPIView(ListAPIView):
	serializer_class = CustomerSerializer

	def get_queryset(self):
		uid = self.kwargs['uid']
		return Customer.objects.filter(uid=uid)

	def list(self, request, *args, **kwargs):
		queryset = self.get_queryset()
		dogs = Dog.objects.filter(owner=queryset[0].id)
		serializer = DogSerializer(dogs, many=True)
		return Response(serializer.data)

class CustomerDetailsAPIView(RetrieveAPIView):
	serializer_class = CustomerDetailsSerializer
	queryset = Customer.objects.all()



class CustomerFilterAPIView(generics.ListAPIView):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = "__all__"
