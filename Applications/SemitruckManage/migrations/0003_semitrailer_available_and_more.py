# Generated by Django 4.1.7 on 2023-08-02 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SemitruckManage', '0002_semitrailer_photo_semitrailerequipment_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='semitrailer',
            name='available',
            field=models.CharField(choices=[('Wolny', 'Wolny'), ('Zajety', 'Zajety'), ('Awaria', 'Awaria')], default='Wolny', max_length=6),
        ),
        migrations.AlterField(
            model_name='semitrailer',
            name='registration_number',
            field=models.CharField(max_length=9, unique=True),
        ),
    ]