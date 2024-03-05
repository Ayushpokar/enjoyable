# Generated by Django 4.2.10 on 2024-02-29 08:08

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_rename_train_mastership_train_master_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_master',
            name='regis_date',
            field=models.DateField(default=datetime.date(2024, 2, 29)),
        ),
        migrations.CreateModel(
            name='ScheduleMaster',
            fields=[
                ('schedule_id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('week', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=9)),
                ('route_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.routemaster')),
                ('train_no', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.train_master')),
            ],
        ),
        migrations.CreateModel(
            name='routestation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence_no', models.PositiveSmallIntegerField()),
                ('arrival_time', models.DateTimeField()),
                ('departure_time', models.DateTimeField()),
                ('station_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.station_master')),
                ('train_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.train_master')),
            ],
            options={
                'db_table': 'route_stations',
                'ordering': ['sequence_no'],
            },
        ),
    ]
