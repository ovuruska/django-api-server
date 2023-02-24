from django.contrib import admin


from .models.transaction import Transaction

# Register your models here.
admin.site.register(Transaction)