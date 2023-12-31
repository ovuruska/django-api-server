from typing import Type, Callable

from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_400_BAD_REQUEST


def validate_request(serializer: Type[Serializer]) -> Callable:
	def decorator(func: Callable) -> Callable:
		def wrapper(*args, **kwargs):
			request = args[1]
			serializer_instance = serializer(data=request.data)
			if serializer_instance.is_valid():
				serialized_data = serializer_instance.validated_data
				return func(*args, serialized_data=serialized_data,**kwargs)
			else:
				return Response(serializer_instance.errors, status=HTTP_400_BAD_REQUEST)
		return wrapper
	return decorator