from datetime import datetime

from django.apps import apps
from django.forms.models import model_to_dict
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response

from scheduling.models import EmployeeWorkingHour
from scheduling.selectors.working_hours import get_employee_working_hours,set_employee_working_hours
from scheduling.serializers.wh_employee import EmployeeWorkingHourSerializer, EmployeeWorkingHourRetrieveSerializer





class EmployeeWorkingHourRetrieveCreateView(generics.ListAPIView,generics.CreateAPIView):
	"""
	API endpoint that allows users to be viewed or edited.
	{
		"start": "2020-01-01",
		"end": "2020-01-31",
		"employee":Employee
		"working_hours":[
			{
				"working_hours":char[24],
				"branch":Branch,
				"date":date
			}
	}

	"""
	Employee = apps.get_model(
		'scheduling',
		'Employee'
	)
	queryset = EmployeeWorkingHour.objects.all()
	serializer_class = EmployeeWorkingHourSerializer

	def post(self, request, *args, **kwargs):
		employee_id = self.kwargs.get("pk", None)

		result = set_employee_working_hours(employee_id, request.data["date"],
		                                       request.data["start"], request.data["end"], request.data["branch"])
		return Response(data=result, status=200)

	def get(self, request, *args, **kwargs):

		start = request.query_params.get("start", None)
		end = request.query_params.get("end", None)
		employee_id = self.kwargs.get("pk", None)

		if start == None or end == None or employee_id == None:
			return Response(status=400)
		else:
			start_date = datetime.strptime(start, "%Y-%m-%d").date()
			end_date = datetime.strptime(end, "%Y-%m-%d").date()
			working_hours = get_employee_working_hours(start_date, end_date, employee_id)
			employee = self.Employee.objects.get(pk=employee_id)
			employee = model_to_dict(employee)

			data = {
				"start": start,
				"end": end,
				"employee": employee,
				"working_hours": working_hours
			}
			return JsonResponse(data)
