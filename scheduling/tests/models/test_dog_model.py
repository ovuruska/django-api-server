from django.test import TestCase
from scheduling.models import Dog, Customer

"""
This test suite contains two test cases:

test_dog_creation: Tests whether the Dog instance is created correctly with the given data.
test_dog_related_name: Tests the related name of the owner field in the Dog model.
"""

class DogModelTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name='John Doe',
            uid='1234567890',
            email='john.doe@example.com',
            phone='123-456-7890',
            address='123 Main St'
        )
        self.dog = Dog.objects.create(
            name='Fido',
            breed='Golden Retriever',
            age=2,
            weight=70,
            description='Friendly and playful',
            owner=self.customer,
            coat_type=Dog.CoatType.SMOOTH_LONG
        )

    def test_dog_creation(self):
        self.assertIsNotNone(self.dog)
        self.assertEqual(self.dog.name, 'Fido')
        self.assertEqual(self.dog.breed, 'Golden Retriever')
        self.assertEqual(self.dog.age, 2)
        self.assertEqual(self.dog.weight, 70)
        self.assertEqual(self.dog.description, 'Friendly and playful')
        self.assertEqual(self.dog.owner, self.customer)
        self.assertEqual(self.dog.coat_type, Dog.CoatType.SMOOTH_LONG)

    def test_dog_related_name(self):
        self.assertIn(self.dog, self.customer.dogs.all())
