# Generated by Django 4.1.7 on 2023-07-23 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='avaiable',
            field=models.CharField(choices=[('Dostepny', 'Dostepny'), ('Zajety', 'Zajety'), ('Urlop', 'Urlop'), ('Inne', 'Inne')], default='Dostepny', max_length=8),
        ),
    ]