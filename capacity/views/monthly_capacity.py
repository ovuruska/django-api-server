from rest_framework.generics import  CreateAPIView
from rest_framework.permissions import IsAuthenticated


class GetMonthlyCapacity(CreateAPIView):
	permission_classes = (IsAuthenticated,)


	def post(self, request, *args, **kwargs):
		serializer = MonthlyCapacitySerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		return request.data