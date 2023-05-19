from django.apps import apps
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from payment.serializers.models.credit_card import CreditCardSerializer

CreditCard = apps.get_model('payment.CreditCard')

class ListCustomerCardsView(APIView):
	permission_classes = [IsAuthenticated]

	@swagger_auto_schema(
		responses={200: CreditCardSerializer(many=True)}
	)
	def get(self, request, *args, **kwargs):
		user = request.user
		customer = user.customer
		cards = CreditCard.objects.filter(owner=customer)
		serializer = CreditCardSerializer(cards, many=True)
		return Response(serializer.data)