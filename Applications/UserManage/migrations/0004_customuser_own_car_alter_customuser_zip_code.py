# Generated by Django 4.1.7 on 2023-07-25 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManage', '0003_alter_customuser_apartment_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='own_car',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='zip_code',
            field=models.CharField(max_length=6),
        ),
    ]