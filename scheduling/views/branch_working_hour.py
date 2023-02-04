from rest_framework import generics
from rest_framework.response import Response

from scheduling.models.branch_working_hour import BranchWorkingHour
from scheduling.selectors.working_hours import set_employee_working_hours, get_employee_working_hours, \
	set_branch_working_hours, get_branch_working_hours
from scheduling.serializers.Branch_Working_Hour import BranchWorkingHourSerializer


class BranchWorkingHourView(generics.CreateAPIView, generics.ListAPIView):
	queryset = BranchWorkingHour.objects.all()
	serializer_class = BranchWorkingHourSerializer

	def get(self, request, *args, **kwargs):

		start = request.query_params.get("start", None)
		end = request.query_params.get("end", None)
		branch_id = request.query_params.get("id", None)
		if start == None or end == None or branch_id == None:
			return Response(status=400)
		else:
			working_hours = get_branch_working_hours(start, end, branch_id)
			return Response(data=working_hours, status=200)

	def post(self, request, *args, **kwargs):

		result = set_branch_working_hours( request.data["branch"], request.data["date"],
		                                    request.data["working_hours"],)
		return Response(data=result, status=200)



