# Generated by Django 4.2.10 on 2024-03-28 20:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_ticket_master_rename_price_class_master_fare_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='train_master',
            name='arrival_time',
            field=models.TimeField(default=datetime.time(1, 58, 5, 605633)),
        ),
        migrations.AlterField(
            model_name='train_master',
            name='depart_time',
            field=models.TimeField(default=datetime.time(1, 58, 5, 605633)),
        ),
    ]