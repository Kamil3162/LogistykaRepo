from django.contrib.auth.models import Group, Permission
from Applications.UserManage.models import CustomUser
from django.core.management import BaseCommand


# class GroupManagement(BaseCommand):
#     def handle(self, *args, **options):
admin_permissions = CustomUser._meta.permissions

driver_permissions = [
    ('view_own_details', 'Can view own user details'),
    ('update_own_user_details', 'Can update own user details'),
    ('delete_own_account', 'Can delete own account'),
    ('view_truck_details', 'Can view truck details'),
    ('view_semitrailer_details', 'Can view semitrailer details'),
    ('create_receivment', 'Can create receivment'),
]

truck_group, _ = Group.objects.get_or_create(name='Driver')
manager_group, _ = Group.objects.get_or_create(name='Manager')
admin_group, _ = Group.objects.get_or_create(name='Admin')

for code_name, _ in admin_permissions:
    permission = Permission.objects.get(codename=code_name)
    admin_group.permissions.add(permission)

    # we transofrm this t oset because we have bigO equal O(1)
    driver_permission = set(x[0] for x in driver_permissions)
    admin_permission = set(x[0] for x in admin_permissions)
    manager_permission = admin_permission - driver_permission

    if permission.codename in driver_permission:
        truck_group.permissions.add(permission)
    if permission.codename in manager_permission:
        manager_group.permissions.add(permission)

truck_group.save()
manager_group.save()
admin_group.save()
