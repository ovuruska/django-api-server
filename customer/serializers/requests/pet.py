from rest_framework import serializers

class CreatePetRequestSerializer(serializers.Serializer):

	name = serializers.CharField(max_length=64)
	breed = serializers.CharField(max_length=128)
	weight = serializers.IntegerField()
	gender = serializers.CharField(max_length=6)
	birth_date = serializers.DateField(allow_null=True,input_formats=["%Y-%m-%d","%Y-%m-%d %H:%M:%S","%Y-%m-%dT%H:%M:%S.%fZ"])
	special_handling = serializers.CharField(max_length=1000,default="",allow_blank=True)
	rabies_vaccination = serializers.DateField(allow_null=True,input_formats=["%Y-%m-%d","%Y-%m-%d %H:%M:%S","%Y-%m-%dT%H:%M:%S.%fZ"])
	def validate(self, data):
		if data["gender"] not in ["Male","Female"]:
			raise serializers.ValidationError("Invalid gender")

		return data

