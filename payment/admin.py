from django.contrib import admin

from payment.models.credit_card import CreditCard

# Register your models here.
admin.site.register(CreditCard)