import datetime
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from scheduling.serializers.Payroll import PayrollSerializer
from scheduling.services.payroll import get_payrolls


class PayrollListRetrieveView(generics.ListAPIView):
	serializer_class = PayrollSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ["start", "end", "branch"]

	def get_queryset(self):
		start = self.request.query_params.get("start", None) or datetime.datetime(datetime.MINYEAR,1,1)
		end = self.request.query_params.get("end", None) or datetime.datetime(datetime.MAXYEAR,1,1)
		branch_id = self.request.query_params.get("branch")

		return get_payrolls(branch_id, start, end)
