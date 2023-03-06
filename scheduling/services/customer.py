from django.apps import apps

Customer = apps.get_model('scheduling', 'Customer')


def create_customer_with_name(name, **kwargs) -> Customer:
	customer = Customer.objects.filter(name=name).first()
	if customer is None:
		customer = Customer(name=name, validated=False, **kwargs)
		customer.save()

	return customer
