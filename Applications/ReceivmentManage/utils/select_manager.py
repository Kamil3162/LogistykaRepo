from Applications.UserManage.models import CustomUser
from ..models import Receivment, ReceivmentLocations
import random
import os

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

class SelectDistanceManager:
    API_KEY = os.environ.get('GOOGLE_API')

    def __init__(self, source, destination):
        self.source_address = source
        self.destination_address = destination
        self.active_drivers =

    def calculate_distance(self):
        pass

    def search_active_drivers(self):
        active_locations = ReceivmentLocations.objects.all()
        active_drivers =

