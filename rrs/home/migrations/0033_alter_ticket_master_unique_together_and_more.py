# Generated by Django 4.2.10 on 2024-04-16 08:21

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0032_alter_passenger_master_pass_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='passenger_master',
            name='pnr_no',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.ticket_master'),
        ),
        migrations.AlterField(
            model_name='ticket_master',
            name='PNR_NO',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user_master',
            name='regis_date',
            field=models.DateField(default=datetime.date(2024, 4, 16)),
        ),
        
        migrations.CreateModel(
            name='payment_master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_holdername', models.CharField(max_length=50)),
                ('card_number', models.CharField(max_length=16)),
                ('card_expiry', models.DateField()),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=8)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('payment_status', models.CharField(choices=[('CNF', 'CONFIRMED'), ('PEN', 'PENDING')], max_length=3)),
                ('payment_method', models.CharField(max_length=10)),
                ('pnr_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='home.ticket_master')),
            ],
        ),
        migrations.RemoveField(
            model_name='ticket_master',
            name='pass_id',
        ),
        
    ]
