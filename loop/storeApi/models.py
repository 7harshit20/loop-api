from django.db import models

# Create your models here.
class Timing(models.Model):
    store_id = models.BigIntegerField()
    day = models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

    def __str__(self):
        return f"Store {self.store_id} - {self.day} {self.start_time_local} - {self.end_time_local}"

class Timezone(models.Model):
    store_id = models.BigIntegerField(primary_key=True)
    timezone_str = models.CharField(max_length=50)

    def __str__(self):
        return f"Store {self.store_id} - {self.timezone_str}"

class StoreStatus(models.Model):
    store_id = models.BigIntegerField()
    status = models.CharField(max_length=8, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    timestamp_utc = models.DateTimeField()

    def __str__(self):
        return f"Store {self.store_id} - {self.timestamp_utc} - {self.status}"
    
class Report(models.Model):
    report_string = models.CharField(max_length=10)
    uptime_last_hour = models.FloatField()
    downtime_last_hour = models.FloatField()
    uptime_last_day = models.FloatField()
    downtime_last_day = models.FloatField()
    uptime_last_week = models.FloatField()
    downtime_last_week = models.FloatField()

    def __str__(self):
        return f"Report {self.report_string} - {self.uptime_last_hour} - {self.downtime_last_hour} - {self.uptime_last_day} - {self.downtime_last_day} - {self.uptime_last_week} - {self.downtime_last_week}"