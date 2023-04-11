import csv
from datetime import datetime, timezone

from django.core.management.base import BaseCommand
from storeApi.models import StoreStatus

class Command(BaseCommand):
    help = 'Imports store status data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='CSV file to import')

    def handle(self, *args, **options):
        path = options['path']

        # Delete all the data in the StoreStatus table
        StoreStatus.objects.all().delete()


        with open(path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                store_id = int(row['store_id'])
                timestamp_str = row['timestamp_utc'][:-4]
                status = row['status']
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=timezone.utc)
                ent = StoreStatus(store_id=store_id, timestamp_utc=timestamp, status=status)
                ent.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully imported data from {path}'))
