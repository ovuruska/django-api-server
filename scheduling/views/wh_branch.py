from datetime import datetime, timedelta

from django.http import QueryDict
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from scheduling.models.branch_wh import BranchWorkingHour
from scheduling.serializers.wh_branch import BranchWorkingHourSerializer


class BranchWorkingHourView(generics.CreateAPIView, generics.ListAPIView):
	queryset = BranchWorkingHour.objects.all()
	serializer_class = BranchWorkingHourSerializer
	def get(self, request, *args, **kwargs):
		# branch_id must field

		branch_id = kwargs.get("pk")
		start_date = request.query_params.get("start", None)
		end_date = request.query_params.get("end", None)
		queryset = BranchWorkingHour.objects.filter(branch_id=branch_id)
		response = []
		# Start from start_date to end_date
		if start_date and end_date:
			start_date = datetime.strptime(start_date, "%Y-%m-%d")
			end_date = datetime.strptime(end_date, "%Y-%m-%d")
			current = start_date

			while current < end_date:
				week_day = current.weekday()
				try:
					data = queryset.get(week_day=week_day)
					# Convert start to %H:%M
					start_time = data.start.strftime("%H:%M")
					end_time = data.end.strftime("%H:%M")
					data = {
						"week_day": data.week_day,
						"start": start_time,
						"end": end_time,
						"branch": data.branch_id,

					}
				except BranchWorkingHour.DoesNotExist:
					data = {
						"branch": branch_id,
						"week_day": week_day,
						"start": None,
						"end": None,
					}
				data['date'] = current.strftime("%Y-%m-%d")

				response.append(data)
				current += timedelta(days=1)

		return Response(response, status=HTTP_200_OK)

	def post(self, request, *args, **kwargs):
		# Date is a must field.
		data = request.data or []
		branch_id = kwargs.get("pk")

		if not isinstance(data, list):
			data = [data]

		for item in data:
			if isinstance(item, QueryDict):
				item = item.dict()

			date = item['date']
			date = datetime.strptime(date, "%Y-%m-%d")

			start = item.get('start', None)
			end = item.get('end', None)
			week_day = date.weekday()

			if start is None or end is None:
				BranchWorkingHour.objects.filter(branch_id=branch_id, week_day=week_day).delete()
				continue


			else:
				try:
					start = datetime.strptime(start, "%Y-%m-%dT%H:%M")
					end = datetime.strptime(end, "%Y-%m-%dT%H:%M")
				except ValueError:
					start = datetime.strptime(start, "%Y-%m-%d %H:%M")
					end = datetime.strptime(end, "%Y-%m-%d %H:%M")

				BranchWorkingHour.objects.update_or_create(
					defaults={
						'start': start,
						'end': end,
					},
					branch_id=branch_id, week_day=week_day)
		return Response(status=status.HTTP_201_CREATED)
