from django.core.management import BaseCommand

from common import Mock


class Command(BaseCommand):
    help = "initializes admin model"

    def add_arguments(self, parser):
        parser.add_argument('scale', default=None)

    def handle(self, *args, **options):
        scale = options['scale']
        scale = int(scale)
        self.mock = Mock(
            number_of_branches = scale,
            number_of_employees = scale,
            number_of_customers = scale,
            number_of_dogs = scale,
            number_of_appointments = scale,
            number_of_services = scale,
            number_of_products = scale,
            number_of_categories = scale
        )
        self.data = self.mock.generate()

