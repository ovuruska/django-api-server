from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import RetrieveAPIView

from analytics.selectors import get_average_service_time

@method_decorator(cache_page(60 * 60 * 24), name='dispatch')
class AverageServiceTimeView(RetrieveAPIView):


	def get(self, request, *args, **kwargs):
		pet_id = self.kwargs['pk']
		average_service_time = get_average_service_time(pet_id)
		response = {
			"average_service_time":average_service_time
		}
		return JsonResponse(response)
