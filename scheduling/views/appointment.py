from datetime import datetime, timedelta,time
from decimal import *

from dateutil.parser import parser
from django.apps import apps
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.signing import Signer
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from common.pagination import pagination
from common.permissions.AppointmentPermissions import CanCreateAppointment, CanUpdateAppointment, \
    CanAppointmentEmployeeRetrieve
from common.roles import Roles
from common.save_transaction import save_transaction
from ..models import Customer, Service, Product, EmployeeWorkingHour, Employee, Branch
from ..selectors import get_last_appointment_by_same_customer
from ..selectors.appointment_slots import get_available_appointment_slots
from ..serializers.Appointment import *
from ..services import create_pet_with_name
from ..services.customer import create_customer_with_name


class AppointmentEmployeeCreateAPIView(generics.CreateAPIView, PermissionRequiredMixin):

	permission_required = [CanCreateAppointment]
	Customer = apps.get_model('scheduling', 'Customer')
	Dog = apps.get_model('scheduling', 'Dog')
	serializer_class = AppointmentEmployeeCreateSerializer

	def post(self, request, *args, **kwargs):
		customer_name = request.data.get("customer_name")
		customer_email = request.data.get("customer_email", "")
		customer_phone = request.data.get("customer_phone", "")
		customer = create_customer_with_name(customer_name, email=customer_email, phone=customer_phone)

		dog_name = request.data.get("dog_name")
		dog_breed = request.data.get("dog_breed", "")
		dog = create_pet_with_name(customer, dog_name, breed=dog_breed)

		cost = Decimal('0.00')
		products = request.data.get('products', [])
		for product_id in products:
			product = Product.objects.get(id=product_id)
			cost += product.cost

		services = request.data.get('services', [])
		for service_id in services:
			service = Service.objects.get(id=service_id)
			cost += service.cost

		tip = Decimal(request.data.get('tip', 0))
		cost += tip

		# Allow mutations for request.data
		try:
			request.data._mutable = True
		except AttributeError:
			pass

		try:

			appointment = Appointment(start=request.data["start"], end=request.data["end"], customer=customer, dog=dog,
				employee_id=request.data["employee_id"], branch_id=request.data["branch_id"],
				status=Appointment.Status.CONFIRMED, cost=cost)
			appointment.save()
			# Return the appointment as JSON
			serializer = AppointmentEmployeeSerializer(appointment)
			return Response(serializer.data)
		except KeyError as e:
			return Response({"error": str(e)}, status=400)



class AppointmentCreateAPIView(generics.CreateAPIView, PermissionRequiredMixin):
    """
	start: Datetime String in ISO 8601 format : https://www.iso.org/iso-8601-date-and-time-format.html
	"""
    permission_classes = [CanCreateAppointment]
    Customer = apps.get_model('scheduling', 'Customer')
    serializer_class = AppointmentCreateSerializer
    queryset = Appointment.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            request.data._mutable = True
        except AttributeError:
            pass

        # get customer object
        if request.data.get("customer__id") is not None:
            customer = Customer.objects.get(id=request.data.get("customer__id"))
        else:
            customer = Customer.objects.get(uid=request.data["customer"])
            request.data["customer__id"] = customer.id
        request.data["customer"] = customer.id

        # calculate cost
        cost = Decimal('0.00')
        products = request.data.get('products', [])
        for product_id in products:
            product = Product.objects.get(id=product_id)
            cost += product.cost

        services = request.data.get('services', [])
        for service_id in services:
            service = Service.objects.get(id=service_id)
            cost += service.cost

        tip = Decimal(request.data.get('tip', 0))
        cost += tip

        request.data["cost"] = cost

        # get last appointment for the same dog and customer
        last_dog_appointment = get_last_appointment_by_same_dog(request.data["dog"], request.data.get("start"))
        last_customer_appointment = get_last_appointment_by_same_customer(customer.id)
        if last_dog_appointment is not None:
            request.data["last_dog_appointment"] = last_dog_appointment.start
        if last_customer_appointment is not None:
            request.data["last_customer_appointment"] = last_customer_appointment.start

        to = customer.email

        title = "Scrubbers - Appointment Confirmation"
        signer = Signer()
        response = self.create(request, *args, **kwargs)
        appointment = response.data
        token = signer.sign(appointment["id"])
        accept_url = f"http://localhost:8000/api/confirmation/{token}/approve"
        cancel_url = f"http://localhost:8000/api/confirmation/{token}/cancel"
        reschedule_url = f"http://localhost:8000/api/confirmation/{token}/reschedule"
        start = appointment["start"]
        datetime_value = datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ")
        date = datetime_value.strftime("%m/%d/%Y")
        hours = datetime_value.strftime("%I:%M %p")

        # body = approval_email(date, hours,accept_url, cancel_url, reschedule_url)
        # send_email(to,title,body)

        return response


class AppointmentModifyAPIView(generics.RetrieveAPIView, generics.UpdateAPIView, PermissionRequiredMixin):
    """
	This view will be used in employee application to update the status of the appointment.
	"""
    permission_classes = [CanUpdateAppointment]
    serializer_class = AppointmentModifySerializer
    queryset = Appointment.objects.all()

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])

    @save_transaction
    def patch(self, request, *args, **kwargs):
        """
		Updates the appointment with the given id
		"""
        pk = self.kwargs.get("pk")
        appointment = Appointment.objects.get(id=pk)

        if not appointment.is_modifiable():
            return Response({"error": "Cannot modify a completed appointment"}, status=400,
                            content_type="application/json")

        # Update the appointment with the new data
        serializer = AppointmentModifySerializer(appointment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        appointment = serializer.save()

        # Recalculate the cost based on the new services and products, as well as the tip
        cost = Decimal('0.00')
        tip = request.data.get('tip', Decimal('0.00'))

        for product in appointment.products.all():
            cost += product.cost

        for service in appointment.services.all():
            cost += service.cost

        # Add cost of new products
        new_products = request.data.get('products', [])
        for product in new_products:
            cost += Decimal(product.get('cost', '0.00'))

        # Add cost of new services
        new_services = request.data.get('services', [])
        for service in new_services:
            cost += Decimal(service.get('cost', '0.00'))

        # Add tip to total cost
        cost += Decimal(tip)

        # Update the appointment with the new cost
        appointment.cost = cost
        appointment.save()

        serializer = AppointmentEmployeeSerializer(appointment)
        return Response(serializer.data)


class AppointmentEmployeeRetrieveAPIView(generics.RetrieveAPIView, PermissionRequiredMixin):
    permission_classes = [CanAppointmentEmployeeRetrieve]
    serializer_class = AppointmentEmployeeSerializer
    queryset = Appointment.objects.all()

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])


class AppointmentCustomerRetrieve(generics.RetrieveAPIView):
    serializer_class = AppointmentCustomerRetrieveSerializer
    queryset = Appointment.objects.all()

    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])


class CustomerGetAppointmentsAPIView(generics.ListAPIView):
    serializer_class = AppointmentModifySerializer

    def get_queryset(self):
        # Get the authenticated user's customer object
        try:
            customer = self.request.user.customer
        except Customer.DoesNotExist:
            return Appointment.objects.none()

        # Get the customer's appointments
        appointments = customer.appointments.all()

        # Apply filters
        start_date = self.request.query_params.get('start__gt')
        if start_date:
            appointments = appointments.filter(start__gt=start_date)

        end_date = self.request.query_params.get('start__lt')
        if end_date:
            appointments = appointments.filter(start__lt=end_date)

        appointments = pagination(self.request, appointments)
        return appointments


class EmployeeFreeTimesAPIView(generics.CreateAPIView, PermissionRequiredMixin):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        branches = request.data.get("branches")
        date_str = request.data.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
        duration = request.data.get("duration")
        service_type = request.data.get("service_type")
        role = Roles.CUSTOMER

        if service_type == "Full Grooming":
            role = Roles.EMPLOYEE_FULL_GROOMING
        elif service_type == "We Wash":
            role = Roles.EMPLOYEE_WE_WASH

        if not branches is False :
            branches = Branch.objects.all()
        else:
            temp = []
            for branch in branches:
                temp.append(Branch.objects.get(id=branch))
            branches = temp

        free_times = []
        slot_num = 40 #it can be changed after. This number will determine the number of free times that will be displayed
        while len(free_times) != slot_num:
            for branch in branches:
                employees = request.data.get("employees")
                if employees:
                    temp = []
                    for employee in employees:
                        temp.append(Employee.objects.get(id=employee))
                    employees = temp
                else:
                    employees = Employee.objects.filter(branch=branch, role=role)

                for employee in employees:
                    working_hours = EmployeeWorkingHour.objects.filter(
                        employee=employee,
                        start__date=date.date()
                    ).first()
                    if not working_hours:
                        continue

                    start_time = datetime.combine(date.date(), working_hours.start.time())
                    end_time = datetime.combine(date.date(), working_hours.end.time())

                    employee_appointments = Appointment.objects.filter(
                        employee=employee, start__date=date.date()
                    ).order_by("start")
                    for appointment in employee_appointments:
                        if start_time.time() < appointment.start.time():
                            end_time = datetime.combine(date.date(), appointment.start.time())
                            while start_time < end_time:
                                time_slot = {"branch": BranchSerializer(branch).data,
                                             "employee": EmployeeSerializer(employee).data,
                                             "start": start_time.strftime("%H:%M:%S"),
                                             "end": (start_time + timedelta(minutes=duration)).strftime("%H:%M:%S"),
                                             "date": date
                                             }
                                free_times.append(time_slot)
                                if len(free_times) == slot_num:
                                    return Response(free_times)
                                start_time += timedelta(minutes=duration)
                        start_time = datetime.combine(date.date(), appointment.end.time())

                    # If there is any remaining free time after the last appointment
                    if start_time.time() < end_time.time():
                        while start_time < end_time:
                            time_slot = {"branch": BranchSerializer(branch).data,
                                         "employee": EmployeeSerializer(employee).data,
                                         "start": start_time.strftime("%H:%M:%S"),
                                         "end": (start_time + timedelta(minutes=duration)).strftime("%H:%M:%S"),
                                         "date": date
                                         }
                            free_times.append(time_slot)
                            if len(free_times) == slot_num:
                                return Response(free_times)
                            start_time += timedelta(minutes=duration)
            new_date = date + timedelta(days=1)
            date = new_date  # assign the new datetime object back to date

        return Response(free_times)







