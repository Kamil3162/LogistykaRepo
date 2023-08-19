# Generated by Django 4.1.7 on 2023-08-19 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserManage', '0005_alter_customuser_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': [('view_user_details', 'Can view user details'), ('view_own_details', 'Can view own user details'), ('update_user_details', 'Can update user details'), ('update_own_user_details', 'Can update own user details'), ('delete_own_account', 'Can delete own account'), ('delete_user_account', 'Can delete user account'), ('create_user_account', 'Can create user account'), ('view_truck_details', 'Can view truck details'), ('update_truck_details', 'Can update truck details'), ('delete_truck_details', 'Can delete truck'), ('create_truck', 'Can delete truck'), ('view_semitrailer_details', 'Can view semitrailer details'), ('update_semitrailer_details', 'Can update semitrailer details'), ('delete_semitrailer_details', 'Can delete semitrailer'), ('create_semitrailer', 'Can create semitrailer'), ('create_receivment', 'Can create receivment'), ('view_receivment', 'Can view receivment'), ('delete_receivment', 'Can delete receivment')]},
        ),
    ]
