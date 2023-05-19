from requests import HTTPError
from django.apps import apps
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from payment.services.clover import CloverService

CreditCard = apps.get_model('payment.CreditCard')

class DeleteCreditCardView(APIView):
	permission_classes = [IsAuthenticated]
	@swagger_auto_schema(
		responses={204: ''}
	)
	def delete(self, request, *args, **kwargs):
		try:
			id = kwargs.get('pk')
			user = request.user
			customer = user.customer
			credit_card = CreditCard.objects.get(id=id, owner=customer)
			assert credit_card is not None
			clover_service = CloverService()
			clover_service.delete_credit_card(credit_card.customer_token, credit_card.card_token)
			credit_card.delete()
		except AssertionError as e:
			return Response(status=status.HTTP_404_NOT_FOUND, data={'detail': f'Credit card with id {id} not found'})
		except HTTPError as e:
			return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE, data={'detail': str(e)})
		except Exception as e:
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'detail': str(e)})
		return Response(status=status.HTTP_204_NO_CONTENT)