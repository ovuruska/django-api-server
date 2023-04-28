from rest_framework import serializers




class CustomerPetDetailsResponseSerializer(serializers.Serializer):

	id = serializers.IntegerField()
	name = serializers.CharField()
	breed = serializers.CharField()
	age = serializers.IntegerField()
	weight = serializers.IntegerField()
	description = serializers.CharField()
	rabies_vaccination = serializers.DateField(format="%Y-%m-%d",input_formats=["%Y-%m-%d","%Y-%m-%dT%H:%M:%SZ"],required=False)
	birth_date = serializers.DateField(format="%Y-%m-%d",input_formats=["%Y-%m-%d","%Y-%m-%dT%H:%M:%SZ"],required=False)
	customer_notes = serializers.CharField()
	special_handling = serializers.BooleanField()
	coat_type = serializers.CharField()
	owner = serializers.IntegerField()
	gender = serializers.CharField(default="Male")
	number_of_groomings = serializers.IntegerField()
	number_of_wewashes = serializers.IntegerField()
	total_grooming_cost = serializers.IntegerField(default=0)
	total_wewash_cost = serializers.IntegerField(default=0)
