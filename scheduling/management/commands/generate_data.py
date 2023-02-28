from django.core.management import BaseCommand

from common import Mock

"""

    Description: Generate data with given scale and appointment interval
    Usage: python manage.py generate_data --scale= --interval=
    Example: python manage.py generate_data 10 --interval=1w
    

"""
class Command(BaseCommand):
    help = "initializes admin model"

    def __init__(self,

                 number_of_branches: int = 1,
                 number_of_employees: int = 5,
                 number_of_customers: int = 25,
                 number_of_dogs: int = 50,
                 number_of_appointments: int = 200,
                 number_of_services: int = 10,
                 number_of_products: int = 10,
                 number_of_categories: int = 4,
                 appointment_interval: str = "1w"

                 ):
        self.number_of_branches = number_of_branches
        self.number_of_employees = number_of_employees
        self.number_of_customers = number_of_customers
        self.number_of_dogs = number_of_dogs
        self.number_of_services = number_of_services
        self.number_of_products = number_of_products
        self.number_of_appointments = number_of_appointments
        self.appointment_interval = appointment_interval

    def add_arguments(self, parser):
        parser.add_argument('scale', nargs='?', type=int, default=10, help='Number of times to generate data')
        parser.add_argument('--interval', nargs='?', type=str, default="1y", help="The appointment interval")


    def handle(self, *args, **options):
        scale = options['scale']
        scale = int(scale)
        self.appointment_interval = options['interval']
        self.mock = Mock(
            number_of_branches = self.number_of_branches * scale,
            number_of_employees = self.number_of_employees * scale,
            number_of_customers = self.number_of_customers * scale,
            number_of_dogs = self.number_of_dogs * scale,
            number_of_appointments = self.number_of_appointments * scale,
            number_of_services = self.number_of_services,
            number_of_products = self.number_of_products,
            appointment_interval= self.appointment_interval,
        )
        self.data = self.mock.generate()

