# Generated by Django 4.2.10 on 2024-02-19 19:41

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user_master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50, verbose_name='First Name')),
                ('lastname', models.CharField(blank=True, max_length=50, verbose_name='Last Name')),
                ('username', models.CharField(max_length=50, verbose_name='Username')),
                ('password', models.CharField(max_length=128, verbose_name='Password')),
                ('dob', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.IntegerField()),
                ('address', models.TextField()),
                ('regis_date', models.DateField(default=datetime.date(2024, 2, 20))),
            ],
        ),
        migrations.CreateModel(
            name='blogs',
            fields=[
                ('user_master_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.user_master')),
                ('title', models.CharField(max_length=200, verbose_name='Blog Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Date Published')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
            bases=('home.user_master',),
        ),
    ]
