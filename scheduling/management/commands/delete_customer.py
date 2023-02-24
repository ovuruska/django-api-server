from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from scheduling import models

"""

    Description: deletes the given customer
    Usage: python manage.py delete_customer --username=
    Example: python manage.py delete_customer quicker-customer
    
"""
class Command(BaseCommand):
    help = "Deletes a customer model"

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the customer to be deleted')

    def handle(self, *args, **kwargs):
        username = kwargs['username']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stderr.write(f"User with username '{username}' does not exist")
            return

        customer = models.Customer.objects.filter(user=user).first()
        if customer:
            customer.delete()

        user.delete()

        self.stdout.write(f"User with username '{username}' has been deleted")
