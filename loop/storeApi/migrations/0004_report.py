# Generated by Django 4.2 on 2023-04-11 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeApi', '0003_timing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_string', models.CharField(max_length=10)),
                ('uptime_last_hour', models.FloatField()),
                ('downtime_last_hour', models.FloatField()),
                ('uptime_last_day', models.FloatField()),
                ('downtime_last_day', models.FloatField()),
                ('uptime_last_week', models.FloatField()),
                ('downtime_last_week', models.FloatField()),
            ],
        ),
    ]
