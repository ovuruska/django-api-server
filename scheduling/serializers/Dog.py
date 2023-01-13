from rest_framework import serializers
from scheduling.models import Dog
from scheduling.serializers.Customer import CustomerSerializer


class DogSerializer(serializers.ModelSerializer):

	owner = CustomerSerializer()
	class Meta:
		model = Dog
		fields = ('id','name', 'breed', 'age', 'weight','owner')
