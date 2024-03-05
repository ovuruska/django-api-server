import datetime
import random

from django.apps import apps
from django.core.management.base import BaseCommand
from faker import Faker
from time import time
Faker.seed(time())

"""

    Description: Add customer model to the database with the input that is taken from CLI
    Usage: python manage.py add_customer

"""


Appointment = apps.get_model('scheduling', 'Appointment')
Customer = apps.get_model('scheduling', 'Customer')
Dog = apps.get_model('scheduling', 'Dog')
Employee = apps.get_model('scheduling', 'Employee')
Branch = apps.get_model('scheduling', 'Branch')
Product = apps.get_model('scheduling', 'Product')
EmployeeWorkingHour = apps.get_model('scheduling', 'EmployeeWorkingHour')



class Command(BaseCommand):
	help = "Creates appointments for a given customer. Customer is specified by his/her username."

	def handle(self, *args, **kwargs):
		username = input("Enter username: ")

		fake = Faker()


		# Get customer by username
		customer = Customer.objects.get(user__username=username)
		# If not found raise error
		if customer is None:
			raise Exception("Customer not found")

		dogs = Dog.objects.filter(owner=customer)
		# If customer has no dog create one
		if len(dogs) == 0:
			dog = Dog(
				name=fake.name(),
				breed=fake.name(),
				owner=customer
			)
			dog.save()
			dogs = [dog]


		# Get number of appts.
		num_appts = int(input("Enter number of appointments: "))

		for _ in range(num_appts):


			# Get random date from future
			date = fake.date_time_between(start_date="-1w", end_date="+1y")
			# Get random working hour at that date.
			working_hours = EmployeeWorkingHour.objects.filter(week_day=date.weekday())
			random_working_hour = working_hours[fake.random_int(min=0, max=len(working_hours)-1)]
			start = date.replace(hour=random_working_hour.start.hour, minute=random_working_hour.start.minute)
			end = date.replace(hour=random_working_hour.end.hour, minute=random_working_hour.end.minute)
			random_dog = dogs[fake.random_int(min=0, max=len(dogs) - 1)]

			tip = fake.random_int(min=0, max=100)
			cost = fake.random_int(min=50, max=200)

			# start is before now.
			if start < datetime.datetime.now():
				status = random.choice(["Completed","Cancelled"])
			else:
				status = "Pending"

			appt = Appointment(
				start=start,
				end=end,
				customer_notes=fake.text(),
				tip=tip,
				cost=cost,
				branch=random_working_hour.branch,
				employee=random_working_hour.employee,
				customer=customer,
				dog=random_dog,
				status=status
			)
			appt.save()




