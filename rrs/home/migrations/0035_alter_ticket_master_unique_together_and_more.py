# Generated by Django 4.2.10 on 2024-04-16 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0034_alter_ticket_master_options_and_more'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='ticket_master',
        #     name='coach_typ',
        # ),
         migrations.AlterField(
            model_name='ticket_master',
            name='arrival_station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrival_ticket', to='home.station_master', to_field='station_code'),
        ),
        migrations.AlterField(
            model_name='ticket_master',
            name='depart_station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depart_ticket', to='home.station_master', to_field='station_code'),
        ),
    ]