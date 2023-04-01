

from rest_framework import serializers


class DailyViewResponseSerializer(serializers.Serializer):

	start = serializers.DateTimeField()
	end = serializers.DateTimeField()
	employee = serializers.IntegerField()
	branch = serializers.IntegerField()

	# Invalidate the serializer if the start date is after the end date
	# Invalidate if extra fields are passed.
	# Invalidate if the start or end date is not in the correct format
	# Invalidate if the employee or branch is not an integer
	# Invalidate if the employee or branch is not a positive integer
	def validate(self, data):
		if data['start'] > data['end']:
			raise serializers.ValidationError('The start date must be before the end date.')
		if data['employee'] < 1:
			raise serializers.ValidationError('The employee must be a positive integer.')
		if data['branch'] < 1:
			raise serializers.ValidationError('The branch must be a positive integer.')
		if set(data.keys()) != {'start', 'end', 'employee', 'branch'}:
			raise serializers.ValidationError('The serializer must only have the start, end, employee, and branch fields.')
		return data

