from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.validate_request import validate_request
from payment.models.credit_card import CreditCard
from payment.serializers.models.credit_card import CreditCardSerializer
from payment.serializers.requests.create_credit_card import CreateCreditCardRequestSerializer
from dotenv import load_dotenv, find_dotenv
import os

from payment.services.clover import CloverService

_ = load_dotenv(find_dotenv())

API_ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')



class CreateCreditCardView(APIView):
	"""Create view for CreditCard model."""
	permission_classes = [IsAuthenticated]

	@swagger_auto_schema(
		request_body=CreateCreditCardRequestSerializer,
		responses={201: CreditCardSerializer}
	)
	@validate_request(CreateCreditCardRequestSerializer)
	def post(self, request, *args, **kwargs):

		user = request.user
		customer = user.customer
		card_number = request.data.get('card_number')
		cvv = request.data.get('cvv')
		exp_date = request.data.get('exp_date')
		brand = request.data.get('brand')
		cardholder_name = request.data.get('cardholder_name')
		address = request.data.get('address')
		address["country"] = "US"
		clover_service = CloverService(API_ACCESS_TOKEN)
		email = customer.email
		exp_month = exp_date[:2]
		exp_year = exp_date[3:]
		clover_response = clover_service.create_credit_card(card_number, brand, exp_month,exp_year, cvv, cardholder_name.split(' ')[0], cardholder_name.split(' ')[1],email, address)
		first6 = clover_response['first6']
		last4 = clover_response['last4']
		customer_token = clover_response['customer_token']
		card_token = clover_response['card_token']
		credit_card = CreditCard.objects.create(
			exp_month=exp_month,
			exp_year=exp_year,
			first6=first6,
			last4=last4,
			brand=brand,
			owner=customer,
			customer_token=customer_token,
			card_token=card_token
		)
		credit_card_serializer = CreditCardSerializer(credit_card)
		return Response(credit_card_serializer.data, status=status.HTTP_201_CREATED)