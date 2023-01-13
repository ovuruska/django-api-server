from django.contrib import admin

from .models import Branch, Service, Product, Employee, Dog, Customer, Appointment

# Register your models here.
admin.site.register(Branch)
admin.site.register(Employee)
admin.site.register(Service)
admin.site.register(Product)
admin.site.register(Dog)
admin.site.register(Customer)
admin.site.register(Appointment)