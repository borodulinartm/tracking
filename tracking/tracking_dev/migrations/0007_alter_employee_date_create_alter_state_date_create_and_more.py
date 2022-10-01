# Generated by Django 4.1.1 on 2022-10-01 08:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking_dev', '0006_alter_employee_date_create_alter_state_date_create_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='date_create',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 10, 1, 8, 24, 16, 567027, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='state',
            name='date_create',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 10, 1, 8, 24, 16, 566027, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='task',
            name='date_change',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 10, 1, 8, 24, 16, 567027, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='task',
            name='date_create',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 10, 1, 8, 24, 16, 567027, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='task',
            name='date_deadline',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 10, 1, 8, 24, 16, 567027, tzinfo=datetime.timezone.utc)),
        ),
    ]
