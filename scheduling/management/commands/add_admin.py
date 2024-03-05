from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
from django.db import transaction

from common.roles import Roles
from scheduling.models import Employee


class Command(BaseCommand):
	help = "Creates an admin user and associated employee record with user input"

	def handle(self, *args, **kwargs):
		username = input("Enter username: ")
		password = input("Enter password: ")
		email = input("Enter e-mail: ")

		fake = Faker()

		try:
			with transaction.atomic():

				user = User.objects.create_user(username=username, password=password, email=email)
				Employee.objects.create(name=fake.name(), phone=fake.phone_number(), role=Roles.ADMIN, email=email,
					user=user, uid=fake.uuid4())
				self.stdout.write(self.style.SUCCESS(f'Successfully created admin user {username}'))
		except Exception as e:
			self.stdout.write(self.style.ERROR(f'Error creating admin user: {e}'))
