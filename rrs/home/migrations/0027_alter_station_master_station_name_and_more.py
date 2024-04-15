# Generated by Django 4.2.10 on 2024-03-28 20:29

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_alter_train_master_arrival_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station_master',
            name='station_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='train_master',
            name='arrival_time',
            field=models.TimeField(default=datetime.time(1, 59, 49, 456380)),
        ),
        migrations.AlterField(
            model_name='train_master',
            name='depart_time',
            field=models.TimeField(default=datetime.time(1, 59, 49, 456380)),
        ),
        migrations.AlterField(
            model_name='train_master',
            name='dest_station',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dest_station', to='home.station_master', to_field='station_code'),
        ),
        migrations.AlterField(
            model_name='train_master',
            name='source_station',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='source_station', to='home.station_master', to_field='station_code', verbose_name='Source Station'),
        ),
    ]