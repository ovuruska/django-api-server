from rest_framework import serializers




class CustomerPetDetailsResponseSerializer(serializers.Serializer):

	id = serializers.IntegerField()
	name = serializers.CharField()
	breed = serializers.CharField()
	age = serializers.IntegerField()
	weight = serializers.IntegerField()
	description = serializers.CharField()
	rabies_vaccination = serializers.DateTimeField()
	employee_notes = serializers.CharField()
	customer_notes = serializers.CharField()
	special_handling = serializers.BooleanField()
	coat_type = serializers.CharField()
	owner = serializers.IntegerField()
	number_of_groomings = serializers.IntegerField()
	number_of_wewashes = serializers.IntegerField()
	total_grooming_cost = serializers.IntegerField(default=0)
	total_wewash_cost = serializers.IntegerField(default=0)