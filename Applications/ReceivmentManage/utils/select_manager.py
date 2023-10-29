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


class SelectDistanceManager:
    API_KEY = os.environ.get('GOOGLE_API')
    GOOGLE_CLIENT = googlemaps.Client(API_KEY)

    def __init__(self, start_address, driver):
        self.source_address = start_address
        self.destination_list = self.search_receivment_to_realize()
        self.active_driver = driver
        self.closest_distance = None
        self.latest_distance = None

    def pick_receivment(self):
        """
                Fetches the distance and duration from the source address to the destination address.
                :param destination_address: The destination address.
                :return: A tuple of (distance, duration).
                """
        for final_address in self.destination_list:
            destination_matrix = self.GOOGLE_CLIENT.distance_matrix(
                self.source_address, final_address
            )['rows'][0]['elements'][0]

            distance = destination_matrix['distance']['value']
            duration = destination_matrix['duration']['value']

            if self.closest_distance is not None:
                if distance < self.latest_distance:
                    self.closest_distance = distance
                    self.closest_distance = final_address
            else:
                self.closest_distance = final_address
                self.latest_distance = distance

        return self.closest_distance

    def search_receivment_to_realize(self):
        """
            Function search all possible destination to realize
        :return: dict{'city, street apartment_number':object,}
        """
        ReceivmentLocations = apps.get_model('ReceivmentManage', 'ReceivmentLocations')
        active_locations = ReceivmentLocations.objects.all()
        active_literal_locations = {
            x.concatination_address():x for x in active_locations
        }
        return active_literal_locations

    def search_active_drivers(self):
        Receivment = apps.get_model('ReceivmentManage', 'Receivment')
        active_locations = Receivment.objects.filter(
            Q(status='Finished') & ~Q(receivment__type='Proggres')
        ).distinct()
        return active_locations

