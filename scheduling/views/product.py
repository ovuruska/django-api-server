from rest_framework import generics

from scheduling.models import Product
from scheduling.serializers.Product import ProductSerializer


class ProductCreateAPIView(generics.CreateAPIView):
	serializer_class = ProductSerializer
	queryset = Product.objects.all()

class ProductModifyAPIView(generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
	serializer_class = ProductSerializer
	queryset = Product.objects.all()


class ProductListAllAPIView(generics.ListAPIView):
	serializer_class = ProductSerializer
	queryset = Product.objects.all()


