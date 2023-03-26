from datetime import datetime

from rest_framework import generics, status
from rest_framework.response import Response

from scheduling.models import EmployeeWorkingHour
from scheduling.serializers.wh_employee import EmployeeWorkingHourSerializer


class EmployeeWorkingHourRetrieveAPIView(generics.RetrieveAPIView, generics.CreateAPIView):
	queryset = EmployeeWorkingHour.objects.all()
	serializer_class = EmployeeWorkingHourSerializer

	def get(self, request, *args, **kwargs):
		employee_id = kwargs.get("pk")
		start_date = request.query_params.get("start", None)
		end_date = request.query_params.get("end", None)
		queryset = EmployeeWorkingHour.objects.filter(employee_id=employee_id)

		if start_date is not None and end_date is not None:
			queryset = queryset.filter(start__gte=start_date, end__lte=end_date)

		serializer = self.serializer_class(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request, *args, **kwargs):
		data = request.data or []
		for item in data:
			date = item['date']
			date = datetime.strptime(date, "%Y-%m-%d")

			start = item['start']
			start = datetime.strptime(start, "%Y-%m-%d %H:%M")

			end = item['end']
			end = datetime.strptime(end, "%Y-%m-%d %H:%M")

			week_day = date.weekday()
			if item['branch'] is None:
				# Delete if exists
				EmployeeWorkingHour.objects.filter(employee_id=item['employee'], week_day=item['week_day']).delete()

			else:
				EmployeeWorkingHour.objects.update_or_create(
					defaults={
						'start': start,
						'end': end,
						'branch_id': item['branch'],
					},
					employee_id = item['employee'],week_day = week_day )
		return Response(status=status.HTTP_200_OK)