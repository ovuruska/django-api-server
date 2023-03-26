from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
import random

from scheduling.models import Appointment, Customer, Dog, Branch, Employee
from scheduling.models import Service, Product  # Import these if you use them in your Appointment model

class Command(BaseCommand):
    help = 'Add given amount of appointments with specific status to the database'

    def add_arguments(self, parser):
        parser.add_argument('amount', type=int, help='The number of appointments to add')
        parser.add_argument('status', type=str, help='The status of the appointments')

    def handle(self, *args, **options):
        amount = options['amount']
        status = options['status']

        if status not in dict(Appointment.Status.choices):
            raise CommandError(f"Invalid status '{status}'. Available statuses: {', '.join(dict(Appointment.Status.choices).keys())}")

        # Modify these queries to match your data
        customers = list(Customer.objects.all())
        dogs = list(Dog.objects.all())
        branches = list(Branch.objects.all())
        employees = list(Employee.objects.all())
        services = list(Service.objects.all())
        products = list(Product.objects.all())

        if not customers or not dogs or not branches or not employees:
            raise CommandError("Required related objects (Customers, Dogs, Branches, or Employees) are missing from the database.")

        for _ in range(amount):
            appointment = Appointment(
                customer=random.choice(customers),
                dog=random.choice(dogs),
                start=timezone.now(),
                end=timezone.now(),
                branch=random.choice(branches),
                employee=random.choice(employees),
                status=status,
            )
            appointment.save()
            appointment.services.set(random.sample(services, k=random.randint(0, len(services))))
            appointment.products.set(random.sample(products, k=random.randint(0, len(products))))
            appointment.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully added {amount} appointments with status "{status}"'))
