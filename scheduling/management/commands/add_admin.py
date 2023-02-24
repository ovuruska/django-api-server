from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User

from common.roles import Roles
from scheduling import models
"""

    Description: Add an admin model to the database with the input that is taken from CLI
    Usage: python manage.py add_admin
    
"""


class Command(BaseCommand):
    help = "initializes admin model"

    def handle(self, *args, **kwargs):
        username = input("Enter username: ")
        password = input("Enter password: ")
        email = input("Enter e-mail: ")

        fake = Faker()

        employee = models.Employee(
            name=fake.name(),
            phone=fake.phone_number(),
            role=Roles.ADMIN,
            email=email,
            user=User.objects.create_user(
                username=username,
                password=password,
                email=email
            ),
            uid=fake.uuid4()
        )
        employee.save()

