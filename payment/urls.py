from django.urls import path

from payment.views.delete_credit_card import DeleteCreditCardView
from payment.views.list_customer_cards import ListCustomerCardsView
from payment.views.take_payment import TakePaymentView
from payment.views.create_credit_card import CreateCreditCardView

urlpatterns = [
	path('create-card',CreateCreditCardView.as_view(), name='payment/create-card'),
	path('take-payment',TakePaymentView.as_view(), name='payment/take-payment'),
	path('card/<int:pk>',DeleteCreditCardView.as_view(), name='payment/delete-card'),
	path('cards',ListCustomerCardsView.as_view(),name='payment/list-cards')
]