import unittest
from unittest.mock import Mock

from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_400_BAD_REQUEST

from common.validate_request import validate_request


class ExampleSerializer(Serializer):
    key = serializers.CharField()

class TestValidateRequestDecorator(unittest.TestCase):
    def test_valid_request(self):
        valid_data = {"key": "value"}

        @validate_request(ExampleSerializer)
        def test_func(selfie,request, *args, **kwargs):
            return "Success"

        request = Mock()
        selfie = Mock()
        request.data = valid_data

        result = test_func(selfie,request)
        self.assertEqual(result, "Success")

    def test_invalid_request(self):
        invalid_data = {"invalid_key": "value"}

        @validate_request(ExampleSerializer)
        def test_func(selfie,request, *args, **kwargs):
            return "Success"

        request = Mock()
        selfie = Mock()
        request.data = invalid_data

        response = test_func(selfie,request)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

