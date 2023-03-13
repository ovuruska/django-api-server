import datetime
import random

import pytz
from django.contrib.auth.models import User
from faker import Faker
from tqdm import tqdm, trange

from scheduling import models
#from transactions.models import Transaction

from .breeds import breeds
from .roles import Roles


class Mock:

    def generate_unique_names(self, generator, number_of_items) -> list:
        names = set()
        while len(names) <= number_of_items:
            names.add(generator())

        return list(names)

    def __init__(self,

                 number_of_branches: int = 1,
                 number_of_employees: int = 5,
                 number_of_customers: int = 20,
                 number_of_dogs: int = 50,
                 number_of_appointments: int = 100,
                 number_of_services: int = 10,
                 number_of_products: int = 10,
                 number_of_categories: int = 4,
                 appointment_interval: str = "1y",
                 number_of_transactions: int = 100

                 ):
        self.number_of_branches = number_of_branches
        self.number_of_employees = number_of_employees
        self.number_of_customers = number_of_customers
        self.number_of_dogs = number_of_dogs
        self.number_of_services = number_of_services
        self.number_of_products = number_of_products
        self.number_of_appointments = number_of_appointments
        self.appointment_interval = appointment_interval
        self.number_of_transactions = number_of_transactions

    def generate(
            self
    ):
        """
			Generates mock data for testing purposes
			:returns: {
				'branches': [Branch, Branch, ...],
				'employees': [Employee, Employee, ...],
				'customers': [Customer, Customer, ...],
				'dogs': [Dog, Dog, ...],
				'services': [Service, Service, ...],
				'products': [Product, Product, ...],
				'appointments': [Appointment, Appointment, ...],
			}
		"""
        branches = []
        employees = []
        customers = []
        dogs = []
        services = []
        transactions = []
        products = []
        appointments = []
        categories = [
            "Treats",
            "Special services",
            "Conditioners",
            "Shampoos"
        ]

        fake = Faker()
        usernames = self.generate_unique_names(fake.user_name, self.number_of_employees + self.number_of_customers)

        current = 0

        for ind in trange(self.number_of_branches, desc="Generating branches"):
            branch = models.Branch(
                name=fake.company(),
                address=fake.address(),
                description=fake.text(),
                tubs=fake.random_int(min=1, max=10),
            )
            branch.save()
            branches.append(branch)

        for ind in trange(self.number_of_employees, desc="Generating employees"):
            email = fake.email()
            password = fake.password()
            if ind < self.number_of_employees / 2 or self.number_of_employees <= 6:
                employee = models.Employee(
                    name=fake.name(),
                    branch=branches[fake.random_int(min=0, max=self.number_of_branches - 1)],
                    phone=fake.phone_number(),
                    email=email,
                    user=User.objects.create_user(
                        username=usernames.pop(),
                        password=password,
                        email=email
                    ),
                    uid=fake.uuid4()
                )
                #Generate employee working hours

                positive = "+" + self.appointment_interval
                negative = "-" + self.appointment_interval

                date = fake.date_between(start_date=negative, end_date=positive)

                # Generate a random start time for an hour between 9am and 5pm
                hour = random.randint(9, 16)
                start_time = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=hour, minute=0)
                # Calculate the end time by adding 8 hours to the start time
                end_time = start_time + datetime.timedelta(hours=8)

                weekday = start_time.weekday()
                branch = branches[random.randint(0, self.number_of_branches - 1)]
                weekday = date.weekday()
                branch = branches[fake.random_int(min=0, max=self.number_of_branches - 1)]
                employee_wh = models.EmployeeWorkingHour(
                    start=start_time,
                    week_day=weekday,
                    employee=employee,
                    branch=branch,
                    end=end_time
                )



            else:
                if ind == self.number_of_employees / 2 and self.number_of_employees > 6:
                    employee = models.Employee(
                        name=fake.name(),
                        branch=branches[fake.random_int(min=0, max=self.number_of_branches - 1)],
                        phone=fake.phone_number(),
                        email=email,
                        role=Roles.ADMIN,
                        user=User.objects.create_user(
                            username=usernames.pop(),
                            password=password,
                            email=email
                        ),
                        uid=fake.uuid4()
                    )

                elif (ind == self.number_of_employees / 2 + 1) and self.number_of_employees > 6:
                    employee = models.Employee(
                        name=fake.name(),
                        branch=branches[fake.random_int(min=0, max=self.number_of_branches - 1)],
                        phone=fake.phone_number(),
                        email=email,
                        role=Roles.ACCOUNTANT,
                        user=User.objects.create_user(
                            username=usernames.pop(),
                            password=password,
                            email=email
                        ),
                        uid=fake.uuid4()
                    )


                elif ind == self.number_of_employees / 2 + 2 and self.number_of_employees > 6:
                    employee = models.Employee(
                        name=fake.name(),
                        branch=branches[fake.random_int(min=0, max=self.number_of_branches - 1)],
                        phone=fake.phone_number(),
                        email=email,
                        role=Roles.MANAGER,
                        user=User.objects.create_user(
                            username=usernames.pop(),
                            password=password,
                            email=email
                        ),
                        uid=fake.uuid4()
                    )
                else:
                    employee = models.Employee(
                        name=fake.name(),
                        branch=branches[fake.random_int(min=0, max=self.number_of_branches - 1)],
                        phone=fake.phone_number(),
                        email=email,
                        role=Roles.EMPLOYEE_FULL_GROOMING,
                        user=User.objects.create_user(
                            username=usernames.pop(),
                            password=password,
                            email=email
                        ),
                        uid=fake.uuid4()
                    )

                    # Generate employee working hours
                    hour = random.randint(9, 16)
                    start_time = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=hour, minute=0)

                    # Calculate the end time by adding 8 hours to the start time
                    end_time = start_time + datetime.timedelta(hours=8)

                    weekday = start_time.weekday()
                    branch = branches[random.randint(0, self.number_of_branches - 1)]
                    weekday = date.weekday()
                    branch = branches[fake.random_int(min=0, max=self.number_of_branches - 1)]
                    employee_wh = models.EmployeeWorkingHour(
                        start=start_time,
                        week_day=weekday,
                        employee=employee,
                        branch=branch,
                        end=end_time
                    )

            employee.save()
            employee_wh.save()
            employees.append(employee)

        for ind in trange(self.number_of_customers, desc="Generating customers"):
            email = fake.email()
            password = fake.password()
            customer = models.Customer(
                name=fake.name(),
                phone=fake.phone_number(),
                email=email,
                uid=fake.uuid4(),
                address=fake.address(),
                user=User.objects.create_user(
                    username=usernames.pop(),
                    password=password,
                    email=email
                )
            )

            current += 1

            customer.save()
            customers.append(customer)

        for ind in trange(self.number_of_dogs, desc="Generating dogs"):
            dog = models.Dog(
                name=fake.name(),
                owner=customers[fake.random_int(min=0, max=self.number_of_customers - 1)],
                breed=fake.random.choice(breeds),
                weight=fake.random.normalvariate(80, 20),
                employee_notes=fake.text(),
                customer_notes=fake.text(),
                special_handling=fake.random.choice(5 * [True] + 95 * [False]),
                rabies_vaccination=fake.date_time_between(start_date="-3m", end_date="+2y", tzinfo=pytz.utc),
                age=fake.random_int(min=1, max=20),
                coat_type=fake.random.choice(models.Dog.CoatType.choices),
            )
            dog.save()
            dogs.append(
                dog
            )

        for ind in trange(self.number_of_services, desc="Generating services"):
            service = models.Service(
                name=fake.company(),
                description=fake.bs(),
                cost=fake.pyfloat(positive=True, min_value=1, max_value=100),
                duration=fake.time_delta(),
            )
            service.save()
            services.append(service)

        for ind in trange(self.number_of_products, desc="Generating products"):
            product = models.Product(
                name=fake.company(),
                description=fake.bs(),
                category=fake.random.choice(categories),
                cost=fake.pyfloat(positive=True, min_value=1, max_value=100),
            )
            product.save()
            products.append(product)

        for ind in trange(self.number_of_appointments, desc='Generating Appointments'):
            positive = "+" + self.appointment_interval
            negative = "-" + self.appointment_interval

            start = fake.date_between(start_date=negative, end_date=positive)
            start = datetime.datetime.combine(start, datetime.time(fake.random_int(min=8, max=18),
                                                                   fake.random.choice([0, 15, 30, 45])))
            start = pytz.utc.localize(start)
            end = start + datetime.timedelta(
                minutes=fake.random.choice([15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180]))

            status = models.Appointment.Status.choices[
                fake.random_int(min=0, max=len(models.Appointment.Status.choices) - 1)][0]

            employee = fake.random.choice(employees)
            branch = employee.branch
            appointment_type = fake.random.choice(models.Appointment.AppointmentType.choices)[0]

            pet = fake.random.choice(dogs)
            customer = pet.owner

            appointment = models.Appointment(
                branch=branch,
                employee=employee,
                dog=dogs[fake.random_int(min=0, max=self.number_of_dogs - 1)],
                start=start,
                end=end,
                customer=customer,
                customer_notes=fake.text(),
                employee_notes=fake.text(),
                cost=fake.pydecimal(positive=True, min_value=1, max_value=250),
                tip=fake.pydecimal(positive=True, min_value=1, max_value=100),
                status=status,
                appointment_type=appointment_type,

            )

            appointment_services = fake.random.choices(services, k=fake.random_int(min=0, max=4))
            appointment.save()

            for appointment_service in appointment_services:
                appointment.services.add(appointment_service)
            appointment_products = fake.random.choices(products, k=fake.random_int(min=0, max=4))
            for appointment_product in appointment_products:
                appointment.products.add(appointment_product)
            appointment.save()

            appointments.append(appointment)
        """for ind in trange(self.number_of_transactions, desc="Generating transactions"):
            appointment = random.choice(appointments)
            employee = random.choice(employees) if random.random() > 0.5 else None
            customer = random.choice(customers) if random.random() > 0.5 or employee is None else None
            date = fake.date_time_between(start_date="-1y", end_date="now", tzinfo=None)
            action = "modified appointment"
            description = fake.text()
            transaction = Transaction(
                appointment=appointment,
                employee=employee,
                customer=customer,
                date=date,
                action=action,
                description=description,
            )
            transaction.save()
            transactions.append(transaction)

            return transactions"""

        return {
            'branches': branches,
            'employees': employees,
            'customers': customers,
            'dogs': dogs,
            'services': services,
            'appointments': appointments,
            'products': products,
            'transactions': transactions,

        }

    def remove(self, generated_data):
        """
			Removes all data from the database
		"""
        for appointment in tqdm(generated_data['appointments'], desc="Deleting appointments"):
            appointment.delete()
        for product in tqdm(generated_data['products'], desc="Deleting products"):
            product.delete()
        for service in tqdm(generated_data['services'], desc="Deleting services"):
            service.delete()
        for dog in tqdm(generated_data['dogs'], desc="Deleting dogs"):
            dog.delete()
        for customer in tqdm(generated_data['customers'], desc="Deleting customers"):
            customer.delete()
        for employee in tqdm(generated_data['employees'], desc="Deleting employees"):
            employee.delete()
        for branch in tqdm(generated_data['branches'], desc="Deleting branches"):
            branch.delete()
        for transaction in tqdm(generated_data['transactions'], desc="Deleting transactions"):
            transaction.delete()
