# Generated by Django 4.1.1 on 2022-09-17 08:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking_dev', '0010_alter_priority_date_create_alter_project_date_create_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='priority',
            name='date_create',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 9, 17, 8, 5, 3, 465799, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='project',
            name='date_create',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 9, 17, 8, 5, 3, 464799, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='state',
            name='date_create',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 9, 17, 8, 5, 3, 465799, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='typetask',
            name='date_create',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 9, 17, 8, 5, 3, 465799, tzinfo=datetime.timezone.utc)),
        ),
    ]
