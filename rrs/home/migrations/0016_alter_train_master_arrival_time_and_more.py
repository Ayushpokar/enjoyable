# Generated by Django 4.2.10 on 2024-03-08 13:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_train_master_arrival_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='train_master',
            name='arrival_time',
            field=models.TimeField(default=datetime.time(18, 55, 21, 88489)),
        ),
        migrations.AlterField(
            model_name='train_master',
            name='depart_time',
            field=models.TimeField(default=datetime.time(18, 55, 21, 88489)),
        ),
    ]
