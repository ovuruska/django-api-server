import datetime

from rest_framework import views
from rest_framework.response import Response

from common.datetime_range import datetime_range

from scheduling.models import Appointment


class ScheduleCustomerListRetrieveView(views.APIView):

	def get(self,request,*args,**kwargs):
		"""
		GET /schedule
		"""

		start = request.query_params.get('date', None)

		if not start:
			return Response(data="Must provide start date",status=422)
		start = datetime.datetime.strptime(start, '%Y-%m-%d')
		end = start + datetime.timedelta(days=1)
		results = Appointment.objects.filter(start__gte=start, end__lte=end)
		intervals = [
			(result.start,result.end)
			for result in results
		]
		pk = kwargs["pk"]

		timetable = []
		for _date in datetime_range(start, end, datetime.timedelta(hours=1)):
			if _date.hour < 9 or _date.hour > 18:
				continue
			timetable.append(0)

		for interval in intervals:
			for _date in datetime_range(interval[0], interval[1], datetime.timedelta(hours=1,minutes=1)):
				if _date.hour < 9 or _date.hour > 18:
					continue
				hour_index = _date.hour - 9
				timetable[hour_index] = 1

		return Response(data=timetable,status=200,headers={"Content-Type": "application/json"})
		# Get all appointments in the given time range

