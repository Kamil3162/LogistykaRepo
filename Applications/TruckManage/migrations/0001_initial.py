# Generated by Django 4.1.7 on 2023-07-25 17:53

import Applications.TruckManage.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=20)),
                ('model', models.CharField(max_length=40)),
                ('power', models.IntegerField(validators=[django.core.validators.MinValueValidator(300), django.core.validators.MaxValueValidator(999)])),
                ('registration_number', models.CharField(max_length=8, unique=True, validators=[Applications.TruckManage.validators.registration_num_validator])),
                ('driven_length', models.IntegerField()),
                ('production_date', models.DateField()),
                ('avaiable', models.CharField(choices=[('Wolny', 'Wolny'), ('Zajety', 'Zajety'), ('Awaria', 'Awaria')], default='Wolny', max_length=6)),
            ],
        ),
    ]
