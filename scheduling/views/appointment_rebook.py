from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView

from scheduling.serializers.Appointment import AppointmentEmployeeSerializer

Appointment = apps.get_model('scheduling', 'Appointment')
Customer = apps.get_model('scheduling', 'Customer')
Dog = apps.get_model('scheduling', 'Dog')
Branch = apps.get_model('scheduling', 'Branch')
Employee = apps.get_model('scheduling', 'Employee')
Product = apps.get_model('scheduling', 'Product')


class EmployeeCreateAppointmentView(APIView):
	def post(self, request, *args, **kwargs):
		customer_id = request.data.get('customer')
		dog_id = request.data.get('dog')
		branch_id = request.data.get('branch')
		employee_id = request.data.get('employee')
		start = request.data.get('start')
		end = request.data.get('end')
		product_ids = request.data.get('products', [])
		service = request.data.get('service')

		customer = get_object_or_404(Customer,  id=customer_id)
		dog = get_object_or_404(Dog, id=dog_id)
		branch = get_object_or_404(Branch, id=branch_id)
		employee = get_object_or_404(Employee, id=employee_id)

		products = []
		for product_id in product_ids:
			product = get_object_or_404(Product, id=product_id)
			products.append(product)

		appointment = Appointment(
			customer=customer,
			dog=dog,
			start=start,
			end=end,
			branch=branch,
			employee=employee,
			appointment_type=service,
			status=Appointment.Status.PENDING
		)
		appointment.save()
		appointment.products.set(products)
		appointment.save()

		serialized_appointment = AppointmentEmployeeSerializer(appointment)

		return JsonResponse(serialized_appointment.data, status=status.HTTP_201_CREATED)
