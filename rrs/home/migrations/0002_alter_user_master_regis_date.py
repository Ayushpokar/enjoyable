# Generated by Django 4.2.10 on 2024-02-20 19:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_master',
            name='regis_date',
            field=models.DateField(default=datetime.date(2024, 2, 21)),
        ),
    ]
