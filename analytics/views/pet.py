from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.generics import RetrieveAPIView

from analytics.selectors import get_average_service_time
from scheduling.views import Appointment


class AverageServiceTimeSerializer(serializers.Serializer):
	average_service_time = serializers.FloatField()

@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class AverageServiceTimeView(RetrieveAPIView):
	queryset= Appointment.objects.all()

	serializer_class = AverageServiceTimeSerializer

	@swagger_auto_schema(
		operation_description="Get average service time for a pet",
		responses={
			200: openapi.Response(
				description="Average service time",
				schema=AverageServiceTimeSerializer,
				examples={
					"application/json": {
						"average_service_time": 42.5,
					}
				}
			)
		}
	)
	def get(self, request, *args, **kwargs):
		pet_id = self.kwargs['pk']
		average_service_time = get_average_service_time(pet_id)
		response = {
			"average_service_time":average_service_time
		}
		return JsonResponse(response)
