# Generated by Django 4.1.7 on 2023-11-04 10:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReceivmentManage', '0003_alter_receivment_date_create_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='receivmentlocations',
            name='final_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='receivment',
            name='date_create',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 4, 11, 58, 50, 964505)),
        ),
        migrations.AlterField(
            model_name='receivment',
            name='date_finished',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 11, 4, 11, 58, 50, 965505)),
        ),
    ]