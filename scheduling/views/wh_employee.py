from datetime import datetime, timedelta

from django.http import QueryDict
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
		response = []
		# Start from start_date to end_date
		if start_date and end_date:
			start_date = datetime.strptime(start_date, "%Y-%m-%d")
			end_date = datetime.strptime(end_date, "%Y-%m-%d")
			current = start_date

			while current <= end_date:
				week_day = current.weekday()
				data = EmployeeWorkingHour.objects.get(
					employee_id=employee_id,
					week_day=week_day,
				)
				response.append(data)
				current += timedelta(days=1)

		serializer = self.serializer_class(response, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request, *args, **kwargs):
		data = request.data or []

		if not isinstance(data, list):
			data = [data]



		for item in data:
			item = item.dict()
			date = item['date']
			date = datetime.strptime(date, "%Y-%m-%d")

			start = item['start']
			start = datetime.strptime(start, "%Y-%m-%dT%H:%M")

			end = item['end']
			end = datetime.strptime(end, "%Y-%m-%dT%H:%M")

			week_day = date.weekday()
			if item['branch'] is None:
				# Delete if exists
				EmployeeWorkingHour.objects.filter(employee_id=int(item['employee']), week_day=week_day).delete()

			else:
				EmployeeWorkingHour.objects.update_or_create(
					defaults={
						'start': start,
						'end': end,
						'branch_id': int(item['branch']),
					},
					employee_id = int(item['employee']),week_day = week_day )
		return Response(status=status.HTTP_201_CREATED)