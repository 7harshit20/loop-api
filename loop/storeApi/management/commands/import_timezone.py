from django.core.management.base import BaseCommand, CommandError
from storeApi.models import Timing, Timezone, StoreStatus
import csv
from datetime import datetime, timezone

class Command(BaseCommand):
    help = 'Imports data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('path', type= str, help='CSV file to import')

    def handle(self, *args, **options):
        path = options['path']

        # Delete all the data in the StoreStatus table
        Timezone.objects.all().delete()

        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                store_id= int(row['store_id'])
                timezone_str = row['timezone_str']
                ent = Timezone(store_id= store_id, timezone_str=timezone_str)
                ent.save()
                
            
            self.stdout.write(self.style.SUCCESS(f'Successfully imported data from {path}'))


