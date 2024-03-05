import datetime
import random

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from time import time
from tqdm import trange
from django.utils import timezone

Faker.seed(time())

Appointment = apps.get_model('scheduling', 'Appointment')
Customer = apps.get_model('scheduling', 'Customer')
Dog = apps.get_model('scheduling', 'Dog')
Employee = apps.get_model('scheduling', 'Employee')
Branch = apps.get_model('scheduling', 'Branch')
Product = apps.get_model('scheduling', 'Product')
EmployeeWorkingHour = apps.get_model('scheduling', 'EmployeeWorkingHour')

class Command(BaseCommand):
    help = "Generates random appointments for a given number in batches of 50"

    def add_arguments(self, parser):
        parser.add_argument('appointments', type=int, help='Number of appointments to create')

    def handle(self, *args, **options):
        fake = Faker()

        customers = list(Customer.objects.all())
        dogs = list(Dog.objects.all())
        branches = list(Branch.objects.all())
        employees = list(Employee.objects.all())
        num_appts = options['appointments']

        for i in trange(0, num_appts, 50):
            with transaction.atomic():
                for _ in range(min(50, num_appts - i)):
                    customer = random.choice(customers)
                    dog = random.choice(dogs)
                    branch = random.choice(branches)
                    employee = random.choice(employees)
					# start_date should be in two weeks
                    start_date = timezone.make_aware(fake.date_time_between(start_date="-2w", end_date="+2w"))

                    # Add random minutes between 15 and 210, it should be binned with 15 minutes
                    end_date = start_date + datetime.timedelta(minutes=(fake.random_int(min=2, max=14) * 15))
                    tip = fake.random_int(min=0, max=100)
                    cost = fake.random_int(min=50, max=200)
                    status = random.choice(["Completed", "Cancelled", "Pending"])

                    Appointment.objects.create(
                        customer=customer,
                        dog=dog,
                        branch=branch,
                        employee=employee,
                        start=start_date,
                        end=end_date,
                        tip=tip,
                        cost=cost,
                        status=status,
                        customer_notes=fake.text(max_nb_chars=200)
                    )
