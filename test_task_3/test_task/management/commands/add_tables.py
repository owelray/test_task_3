from django.core.management.base import BaseCommand

from test_task.models import Table

from random import randint


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-n', type=int, help='Amount of tables to create. Default is 5')

    def generate_size(self):
        height = randint(13, 18)
        return height, height + randint(8, 13)

    def handle(self, *args, **options):
        amount_of_tables = options['n'] if options['n'] else 5
        for _ in range(amount_of_tables):
            height, width = self.generate_size()
            Table.objects.create(number_of_seats=randint(2, 8), form=randint(0, 1), height=height, width=width)
