from django.core.signing import Signer
from django.shortcuts import render
from rest_framework.views import APIView

from scheduling.models import Appointment
from scheduling.selectors import get_appointment_by_id


class SignedUrlRescheduleAPIView(APIView):

	def get(self, request, *args, **kwargs):
		try:
			signer = Signer()
			result = signer.unsign(kwargs["token"])
			appointment = get_appointment_by_id(result)
			if appointment.is_available():
				appointment.status = Appointment.Status.RESCHEDULING
				appointment.save()
				return render(request, "web/reschedule.html")
			else:
				request.status_code = 404
				return render(request,"web/404.html")
		except:
			request.status_code = 404
			return render(request,"web/404.html")

class SignedUrlApproveAPIView(APIView):

	def get(self, request, *args, **kwargs):
		try:
			signer = Signer()
			result = signer.unsign(kwargs["token"])
			appointment = get_appointment_by_id(result)
			if appointment.is_available():
				appointment.status = Appointment.Status.CONFIRMED
				appointment.save()

				return render(request, "web/approve.html")
			else:
				request.status_code = 404

				return render(request,"web/404.html")
		except:
			request.status_code = 404

			return render(request,"web/404.html")



class SignedUrlCancelAPIView(APIView):
	def get(self, request, *args, **kwargs):
		try:
			signer = Signer()
			result = signer.unsign(kwargs["token"])
			appointment = get_appointment_by_id(result)
			if appointment.is_available():
				appointment.status = Appointment.Status.CANCELLED
				appointment.save()

				return render(request, "web/decline.html")
			else:
				request.status_code = 404
				return render(request,"web/404.html")
		except:
			request.status_code = 404
			return render(request,"web/404.html")
