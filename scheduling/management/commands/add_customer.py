from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User

from common.roles import Roles
from scheduling import models


class Command(BaseCommand):
    help = "initializes admin model"

    def handle(self, *args, **kwargs):
        username = input("Enter username: ")
        password = input("Enter password: ")
        email = input("Enter e-mail: ")

        fake = Faker()

        customer = models.Customer(
            name=fake.name(),
            phone=fake.phone_number(),
            email=email,
            uid=fake.uuid4(),
            address=fake.address(),
            user=User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
        )


        customer.save()




