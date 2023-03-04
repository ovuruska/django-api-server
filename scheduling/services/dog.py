from django.apps import apps

Dog = apps.get_model('scheduling', 'Dog')
Customer = apps.get_model('scheduling', 'Customer')

def create_pet_with_name(owner, dog_name,**kwargs):
	dog = Dog(name=dog_name, owner=owner,**kwargs)
	dog.save()
	return dog