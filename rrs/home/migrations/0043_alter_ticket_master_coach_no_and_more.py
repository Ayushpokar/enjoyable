# Generated by Django 4.2.10 on 2024-04-19 19:44

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0042_ticket_master_arrival_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket_master',
            name='coach_no',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.coach', to_field='coach_no'),
        ),
        migrations.AlterField(
            model_name='user_master',
            name='regis_date',
            field=models.DateField(default=datetime.date(2024, 4, 20)),
        ),
    ]