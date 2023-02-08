from rest_framework import generics
from rest_framework.response import Response

from scheduling.models.branch_working_hour import BranchWorkingHour
from scheduling.selectors.working_hours import set_branch_working_hours, get_branch_working_hours
from scheduling.serializers.wh_branch import BranchWorkingHourSerializer


class BranchWorkingHourView(generics.CreateAPIView, generics.ListAPIView):
	queryset = BranchWorkingHour.objects.all()
	serializer_class = BranchWorkingHourSerializer

	def get(self, request, *args, **kwargs):
		start = request.query_params.get("start", None)
		end = request.query_params.get("end", None)
		branch_id = self.kwargs.get("pk", None)
		if start == None or end == None or branch_id == None:
			return Response(status=400)
		else:
			working_hours = get_branch_working_hours(start, end, branch_id)
		return Response(data=working_hours, status=200)


	def post(self, request, *args, **kwargs):
		branch_id = self.kwargs.get("pk", None)
		start = request.data["start"]
		end = request.data["end"]
		result = set_branch_working_hours(branch_id, request.data["date"],
		                                  start, end)
		return Response(data=result, status=200)
