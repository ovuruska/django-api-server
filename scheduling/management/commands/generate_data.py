from django.core.management import BaseCommand

from common import Mock

"""

    Description: Generate data with given scale and appointment interval
    Usage: python manage.py generate_data --scale= --interval=
    Example: python manage.py generate_data 10 --interval=1w
    

"""
class Command(BaseCommand):
    help = "initializes admin model"


    def add_arguments(self, parser):
        parser.add_argument('scale', nargs='?', type=int, default=10, help='Number of times to generate data')
        parser.add_argument('--interval', nargs='?', type=str, default="1y", help="The appointment interval")


    def handle(self, *args, **options):
        scale = options['scale']
        scale = int(scale)
        self.appointment_interval = options['interval']
        self.mock = Mock(
            number_of_appointments = 2000 * scale,
            appointment_interval= self.appointment_interval,
        )
        self.data = self.mock.generate()

