# Generated by Django 4.1.7 on 2023-08-31 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SemitruckManage', '0007_rename_available_semitrailerequipment_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semitrailerequipment',
            name='status',
        ),
    ]
