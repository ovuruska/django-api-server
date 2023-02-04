from rest_framework import generics
from rest_framework.response import Response

from scheduling.models import EmployeeWorkingHour
from scheduling.models.branch_working_hour import BranchWorkingHour
from scheduling.selectors.working_hours import get_employee_working_hours, set_employee_working_hours
from scheduling.serializers.employee_wh import EmployeeWorkingHourSerializer


class EmployeeWorkingHourView(generics.CreateAPIView, generics.ListAPIView):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = EmployeeWorkingHour.objects.all()
	serializer_class = EmployeeWorkingHourSerializer

	def get(self, request, *args, **kwargs):

		start = request.query_params.get("start", None)
		end = request.query_params.get("end", None)
		employee_id = request.query_params.get("id", None)
		if start == None or end == None or employee_id == None:
			return Response(status=400)
		else:
			working_hours = get_employee_working_hours(start, end, employee_id)
			return Response(data=working_hours, status=200)

	def post(self, request, *args, **kwargs):
		result = set_employee_working_hours(request.data["employee"], request.data["date"], request.data["working_hours"],request.data["branch"])
		return Response(data=result, status=200)
