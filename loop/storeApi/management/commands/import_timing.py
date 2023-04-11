from django.core.management.base import BaseCommand, CommandError
from storeApi.models import Timing, Timezone, StoreStatus
import csv
from datetime import datetime, timezone

class Command(BaseCommand):
    help = 'Imports timing data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('path', type= str, help='CSV file to import')

    def handle(self, *args, **options):
        path = options['path']

        # Delete all the data in the StoreStatus table
        Timing.objects.all().delete()

        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                store_id= int(row['store_id'])
                day= int(row['day'])
                start_time_local_str = row['start_time_local']
                end_time_local_str = row['end_time_local']
                start_time_local = datetime.strptime(start_time_local_str, '%H:%M:%S').time()
                end_time_local = datetime.strptime(end_time_local_str, '%H:%M:%S').time()
                ent = Timing(store_id= store_id, day= day, start_time_local= start_time_local, end_time_local= end_time_local)
                ent.save()
                
        self.stdout.write(self.style.SUCCESS(f'Successfully imported data from {path}'))


