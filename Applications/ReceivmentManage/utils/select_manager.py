import random
import os
import googlemaps
from Applications.UserManage.models import CustomUser
from django.db.models import Q
from django.apps import apps

class ManagerSelect:
    def __init__(self):
        self._managers = CustomUser.objects.filter(groups__name='Manager')
        self.manager = None

    def chose_random_manager(self):
        try:
            manager_user = random.choice(self.managers)
            return manager_user
        except TypeError:
            raise TypeError("Value is null")
        except Exception as e:
            raise Exception(str(e))

    @property
    def managers(self):
        return self._managers
