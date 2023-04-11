# Generated by Django 4.2 on 2023-04-08 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StoreStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.BigIntegerField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], max_length=8)),
                ('timestamp_utc', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Timezone',
            fields=[
                ('store_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('timezone_str', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Timing',
            fields=[
                ('store_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('day', models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
                ('start_time_local', models.TimeField()),
                ('end_time_local', models.TimeField()),
            ],
        ),
    ]
