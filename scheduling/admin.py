from django.contrib import admin
from .models import Dog,  Branch, Appointment, Service, Product, Customer

# Register your models here.
admin.site.register(Dog)
admin.site.register(Customer)
admin.site.register(Branch)
admin.site.register(Appointment)
admin.site.register(Service)
admin.site.register(Product)
