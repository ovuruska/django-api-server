from rest_framework import generics

from scheduling.models import Service
from scheduling.serializers.Service import ServiceSerializer


class ServiceCreateAPIView(generics.CreateAPIView):
	serializer_class = ServiceSerializer
	queryset = Service.objects.all()


class ServiceModifyAPIView(generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
	queryset = Service.objects.all()
	serializer_class = ServiceSerializer


class ServiceListAllAPIView(generics.ListAPIView):
	queryset = Service.objects.all()
	serializer_class = ServiceSerializer
