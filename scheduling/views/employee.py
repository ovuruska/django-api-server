from rest_framework import generics

from scheduling.models import Employee
from scheduling.selectors.employee import get_groomers
from scheduling.serializers.Employee import EmployeeUserRetrieveSerializer, EmployeeSerializer, \
	EmployeeModifySerializer, EmployeeWorkingHoursSerializer


class EmployeeGroomerListRetrieve(generics.ListAPIView):
	serializer_class = EmployeeUserRetrieveSerializer

	def get_queryset(self):
		groomers = get_groomers()
		return groomers


class EmployeeCreateAPIView(generics.CreateAPIView):
	serializer_class = EmployeeSerializer
	queryset = Employee.objects.all()


class EmployeeRetrieveModifyDestroyAPIView(generics.DestroyAPIView, generics.RetrieveAPIView, generics.UpdateAPIView):
	serializer_class = EmployeeModifySerializer
	queryset = Employee.objects.all()

class EmployeeGetWorkingHours(generics.ListAPIView): #The name might change
	serializer_class = EmployeeWorkingHoursSerializer
