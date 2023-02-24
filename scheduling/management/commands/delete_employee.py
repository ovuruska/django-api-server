from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from scheduling import models

"""

    Description: deletes the given employee
    Usage: python manage.py delete_employee --username=
    Example: python manage.py delete_employee quicker-employee

"""

class Command(BaseCommand):
    help = "Deletes an employee model"

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the employee to be deleted')

    def handle(self, *args, **kwargs):
        username = kwargs['username']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stderr.write(f"User with username '{username}' does not exist")
            return

        employee = models.Employee.objects.filter(user=user).first()
        if employee:
            employee.delete()

        user.delete()

        self.stdout.write(f"User with username '{username}' has been deleted")

