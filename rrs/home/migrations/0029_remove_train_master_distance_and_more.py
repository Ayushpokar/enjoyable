# Generated by Django 4.2.10 on 2024-03-29 18:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_train_master_distance_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='train_master',
            name='distance',
        ),
        migrations.RemoveField(
            model_name='train_schedule',
            name='id',
        ),
        migrations.RemoveField(
            model_name='train_schedule',
            name='platform',
        ),
        migrations.RemoveField(
            model_name='train_schedule',
            name='status',
        ),
        migrations.AddField(
            model_name='train_schedule',
            name='day',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='train_schedule',
            name='distance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='train_schedule',
            name='schedule_id',
            field=models.AutoField(default=None, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='train_schedule',
            name='seq',
            field=models.PositiveSmallIntegerField(default=None),
        ),
        migrations.AddField(
            model_name='train_schedule',
            name='station_code',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.station_master', to_field='station_code'),
        ),
        migrations.AddField(
            model_name='train_schedule',
            name='stop_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='train_schedule',
            name='arrival_time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='train_schedule',
            name='depart_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='train_schedule',
            name='train_no',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.train_master'),
        ),
        migrations.AlterField(
            model_name='user_master',
            name='regis_date',
            field=models.DateField(default=datetime.date(2024, 3, 30)),
        ),
        migrations.AlterModelTable(
            name='train_schedule',
            table='train_schedule',
        ),
    ]
