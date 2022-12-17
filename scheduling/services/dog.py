from scheduling.models import Customer, Dog


def is_dog_available(owner_id,dog_name):
	customer_instance = Customer.objects.get_or_create(uid=owner_id)
	if type(customer_instance) is tuple:
		customer_instance = customer_instance[0]
	try:
		_ = Dog.objects.get(name=dog_name, owner=customer_instance)
		return True
	except Dog.DoesNotExist:
		return False