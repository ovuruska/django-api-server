from scheduling.models import Customer, Dog


def is_dog_available(owner_id, dog_name):
    try:
        _ = Dog.objects.get(name=dog_name, owner=owner_id)
        return True
    except Dog.DoesNotExist:
        return False