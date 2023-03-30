from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


class GetMonthlyCapacity(ListAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = MonthlyCapacitySerializer

	def get_queryset(self):
		return MonthlyCapacity.objects.filter(user=self.request.user)