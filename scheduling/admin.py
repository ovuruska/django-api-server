from django.contrib import admin

from .models import Branch, Service, Product, Employee

# Register your models here.
admin.site.register(Branch)
admin.site.register(Employee)
admin.site.register(Service)
admin.site.register(Product)
