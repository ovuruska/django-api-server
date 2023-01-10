from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from scheduling.models import Employee
from scheduling.serializers.Employee import EmployeeFilterSerializer


class EmployeeFilterView(generics.ListAPIView):
	queryset = Employee.objects.all()
	serializer_class = EmployeeFilterSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = "__all__"
