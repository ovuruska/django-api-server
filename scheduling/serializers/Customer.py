from rest_framework import serializers

from scheduling.models.customer import Customer
from scheduling.selectors.customer import get_customer_dogs, get_customer_lifetime_tips, \
	get_customer_lifetime_product_invoice, get_customer_lifetime_service_invoice


class CustomerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Customer
		fields = ('id', 'name', 'phone', 'email', 'address', 'uid')


class CustomerDetailsSerializer(serializers.ModelSerializer):
	lifetime_tips = serializers.SerializerMethodField()
	lifetime_product_sales = serializers.SerializerMethodField()
	lifetime_service_sales = serializers.SerializerMethodField()
	dogs = serializers.SerializerMethodField()

	def get_dogs(self, obj):
		from scheduling.serializers.Dog import DogShallowSerializer

		customer_dogs = get_customer_dogs(obj.id)
		serializer = DogShallowSerializer(customer_dogs, many=True)

		return serializer.data

	def get_lifetime_tips(self, obj):
		total_tips = get_customer_lifetime_tips(obj.id)
		return round(total_tips["tip__sum"] or 0,2)

	def get_lifetime_product_sales(self, obj):
		total_product_sales = get_customer_lifetime_product_invoice(obj.id)
		return round(total_product_sales["products__cost__sum"] or 0,2)
	def get_lifetime_service_sales(self, obj):
		total_service_sales = get_customer_lifetime_service_invoice(obj.id)
		return round(total_service_sales["services__cost__sum"] or 0,2)

	class Meta:
		model = Customer
		fields = "__all__"
