from rest_framework.generics import  ListAPIView

from analytics.models import TopCustomer


class TopCustomerView(ListAPIView):

	def get_queryset(self):
		return TopCustomer.objects.order_by('-total')[:10]


