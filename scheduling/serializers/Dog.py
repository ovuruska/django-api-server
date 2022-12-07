from rest_framework import serializers
from scheduling.models import Dog


class DogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Dog
		fields = ('id','name', 'breed', 'age', 'weight','owner')
