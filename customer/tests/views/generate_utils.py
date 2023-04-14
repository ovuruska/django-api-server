import datetime
from random import choice
from django.apps import apps

Appointment = apps.get_model("scheduling","Appointment")
Customer = apps.get_model("scheduling","Customer")
Branch = apps.get_model("scheduling","Branch")
Employee = apps.get_model("scheduling","Employee")
EmployeeWorkingHour = apps.get_model("scheduling","EmployeeWorkingHour")
Dog = apps.get_model("scheduling","Dog")


def generate_customer_dogs(customer,N):
	dogs = []
	for i in range(N):
		dog = Dog.objects.create(owner=customer, name="test_pet_{}".format(i))
		dogs.append(dog)
	return dogs
def generate_customer_dogs_with_appointments(customer,number_of_appts=100,number_of_dogs=5):
	dogs = generate_customer_dogs(customer,number_of_dogs)

	branch = Branch.objects.create()
	employee = Employee.objects.create( branch=branch)
	for week_day in range(7):
		EmployeeWorkingHour.objects.create(employee=employee, branch=branch,
		                                                                week_day=week_day, start="0:00",
		                                                                end="23:00")

	for i in range(number_of_appts):
		pet = choice(dogs)
		appointment_type = choice(["Full Grooming","We Wash"])
		Appointment.objects.create(customer=customer, branch=branch, employee=employee,start="2020-01-01 00:00:00",end="2020-01-01 00:00:00",dog=pet,appointment_type=appointment_type)



def generate_customer_appts(customer,N,pet = None):
	if pet is None:
		pet = Dog.objects.create(owner=customer, name="test_pet")
	branch = Branch.objects.create()
	employee = Employee.objects.create( branch=branch)
	for week_day in range(7):
		EmployeeWorkingHour.objects.create(employee=employee, branch=branch,
		                                                                week_day=week_day, start="0:00",
		                                                                end="23:00")

	for i in range(N):
		Appointment.objects.create(customer=customer, branch=branch, employee=employee,start="2020-01-01 00:00:00",end="2020-01-01 00:00:00",dog=pet)


def generate_past_appts(customer,N):
	pet = Dog.objects.create(owner=customer, name="test_pet")
	branch = Branch.objects.create()
	employee = Employee.objects.create( branch=branch)
	for week_day in range(7):
		EmployeeWorkingHour.objects.create(employee=employee, branch=branch,
		                                                                week_day=week_day, start="0:00",
		                                                                end="23:00")

	for i in range(N):
		appointment = Appointment.objects.create(customer=customer, branch=branch, employee=employee,start="2019-01-01 00:00:00",end="2019-01-01 00:00:00",dog=pet)
		appointment.save()

def generate_upcoming_appts(customer,N):
	pet = Dog.objects.create(owner=customer, name="test_pet")
	branch = Branch.objects.create()
	employee = Employee.objects.create( branch=branch)
	for week_day in range(7):
		EmployeeWorkingHour.objects.create(employee=employee, branch=branch,
		                                                                week_day=week_day, start="0:00",
		                                                                end="23:00")


	for i in range(N):
		future_start = datetime.datetime.now() + datetime.timedelta(days=1)
		future_end = datetime.datetime.now() + datetime.timedelta(days=1)
		appointment = Appointment.objects.create(customer=customer, branch=branch, employee=employee,start=future_start,end=future_end,dog=pet)
		appointment.save()