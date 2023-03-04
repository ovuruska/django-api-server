from django.apps import apps

Customer = apps.get_model('scheduling', 'Customer')

def create_customer_with_name(name,**kwargs) -> Customer:
	customer = Customer(name=name,validated=False,**kwargs)
	customer.save()
	return customer