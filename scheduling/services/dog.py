from django.apps import apps

Dog = apps.get_model('scheduling', 'Dog')
Customer = apps.get_model('scheduling', 'Customer')

def create_pet_with_name(owner, dog_name):
	dog = Dog(name=dog_name, owner=owner)
	dog.save()
	return dog