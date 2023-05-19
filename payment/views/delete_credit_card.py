import os

from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payment.services.clover import CloverService

CreditCard = apps.get_model('payment.CreditCard')

class DeleteCreditCardView(DeleteView):
	permission_classes = [IsAuthenticated()]

	@swagger_auto_schema(
		responses={204: ''}
	)
	def delete(self, request, *args, **kwargs):
		id = kwargs.get('pk')
		user = request.user
		customer = user.customer
		credit_card = CreditCard.objects.get(id=id, owner=customer)
		clover_service = CloverService()
		clover_service.delete_credit_card(credit_card.customer_token, credit_card.card_token)
		credit_card.delete()

		return Response(status=status.HTTP_204_NO_CONTENT)