# Generated by Django 4.2.10 on 2024-02-22 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_user_master_regis_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='passenger_master',
            fields=[
                ('pass_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('age', models.PositiveSmallIntegerField()),
                ('gender', models.CharField(max_length=6)),
            ],
            options={
                'db_table': 'passenger_master',
            },
        ),
        migrations.CreateModel(
            name='station_master',
            fields=[
                ('station_id', models.IntegerField(primary_key=True, serialize=False)),
                ('station_name', models.CharField(max_length=30)),
                ('station_code', models.CharField(max_length=5)),
                ('location', models.CharField(max_length=50)),
                ('zone', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='user_feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='train_schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('arrival_time', models.TimeField()),
                ('platform', models.CharField(max_length=10)),
                ('status', models.BooleanField(default=False)),
                ('train_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.station_master')),
            ],
            options={
                'verbose_name': 'Train Schedule',
                'verbose_name_plural': 'Trains Schedules',
            },
        ),
        migrations.CreateModel(
            name='train_mastership',
            fields=[
                ('train_no', models.IntegerField(primary_key=True, serialize=False)),
                ('train_name', models.CharField(max_length=50)),
                ('depart_datetime', models.DateTimeField()),
                ('arrival_datetime', models.DateTimeField()),
                ('journey_duration', models.DurationField()),
                ('available_seats', models.PositiveBigIntegerField()),
                ('total_seats', models.PositiveBigIntegerField()),
                ('dest_station', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dest_station', to='home.station_master')),
                ('source_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='home.station_master', verbose_name='Source Station')),
            ],
        ),
    ]