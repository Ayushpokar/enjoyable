# Generated by Django 4.2.11 on 2024-03-08 06:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_user_master_regis_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='train_master',
            name='depart_datetime',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='user_master',
            name='regis_date',
            field=models.DateField(default=datetime.date(2024, 3, 8)),
        ),
    ]
