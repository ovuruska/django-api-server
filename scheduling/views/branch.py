from datetime import datetime

from django.apps import apps
from django.forms import model_to_dict
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.response import Response

from scheduling.models import Branch
from scheduling.selectors.working_hours import get_branch_employees, get_branch_daily_information
from scheduling.serializers.Branch import BranchSerializer


class BranchRetrieveModifyAPIView(RetrieveAPIView,ListAPIView,DestroyAPIView,UpdateAPIView):
	serializer_class = BranchSerializer
	queryset = Branch.objects.all()

	def get(self, request, *args, **kwargs):
		if self.kwargs['pk'] == 'all':
			return self.list(request, *args, **kwargs)
		else:
			return self.retrieve(request, *args, **kwargs)

class BranchCreateAPIView(CreateAPIView):
	serializer_class = BranchSerializer
	queryset = Branch.objects.all()


class BranchEmployeesAPIView(ListAPIView):
	EmployeeWorkingHours = apps.get_model('scheduling', 'EmployeeWorkingHour')

	def get(self, request, *args, **kwargs):
		branch_id = self.kwargs['pk']
		date = request.query_params.get('date', None)

		if date is None:
			return Response(status=400)

		date = datetime.strptime(date, "%Y-%m-%d")
		employees = get_branch_employees(branch_id,date)

		return Response(data=employees, status=200)

class BranchDailyInformationAPIView(RetrieveAPIView):

	def get(self, request, *args, **kwargs):
		branch_id = self.kwargs['pk']
		date = request.query_params.get('date', None)

		if date is None:
			return Response(status=400)

		date = datetime.strptime(date, "%Y-%m-%d")
		result = get_branch_daily_information(branch_id,date)

		return Response(data=result, status=200)