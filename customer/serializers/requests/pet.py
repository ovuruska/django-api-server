from rest_framework import serializers

class CreatePetRequestSerializer(serializers.Serializer):

	name = serializers.CharField(max_length=64)
	breed = serializers.CharField(max_length=128)
	weight = serializers.IntegerField()
	age = serializers.IntegerField()
	gender = serializers.CharField(max_length=6)

	def validate(self, data):
		if data["gender"] not in ["Male","Female"]:
			raise serializers.ValidationError("Invalid gender")

		return data
