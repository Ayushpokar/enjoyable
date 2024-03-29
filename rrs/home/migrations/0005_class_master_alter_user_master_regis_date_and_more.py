# Generated by Django 4.2.10 on 2024-02-22 18:34

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_passenger_master_station_master_user_feedback_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='class_master',
            fields=[
                ('class_id', models.IntegerField(primary_key=True, serialize=False)),
                ('class_name', models.CharField(max_length=20)),
                ('description', models.TextField(max_length=100)),
                ('features', models.TextField(max_length=100)),
                ('capacity', models.IntegerField()),
                ('price', models.FloatField()),
            ],
            options={
                'db_table': 'class_master',
            },
        ),
        migrations.AlterField(
            model_name='user_master',
            name='regis_date',
            field=models.DateField(default=datetime.date(2024, 2, 23)),
        ),
        migrations.CreateModel(
            name='RouteMaster',
            fields=[
                ('route_id', models.AutoField(primary_key=True, serialize=False)),
                ('distance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('route_name', models.CharField(blank=True, max_length=255, null=True)),
                ('travel_time', models.DurationField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('destination_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_routes', to='home.station_master')),
                ('source_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_routes', to='home.station_master')),
            ],
            options={
                'db_table': 'route_master',
            },
        ),
    ]
