from django.db import models
from django.apps import apps
import os
import googlemaps

class ReceivmentManager(models.Manager):
    '''
        Manager responsible for searching latest finallize address like receivment
        We start from latest finished location and we will calculate distance to make the most effective
    '''
    API_KEY = os.environ.get('GOOGLE_API')
    GOOGLE_CLIENT = googlemaps.Client(API_KEY)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.closest_distance = None
        self.closest_object = None
        self.latest_distance = None

    def get_queryset(self):
        return models.QuerySet(self.model, using=self._db)

    def get_latest_driver_location(self, driver):
        Receivment = apps.get_model('ReceivmentManage', 'Receivment')
        receivment_statuses = Receivment.get_statuses()
        result = self.get_queryset().filter(
            models.Q(status=receivment_statuses.FINISHED) &
            models.Q(destination_user=driver)
        ).order_by('date_finished').last()
        return result

    def pick_receivment(self, source_address):
        """
                Fetches the distance and duration from the source address to the destination address.
                :param destination_address: The destination address.
                :return: A tuple of (distance, duration).
                """
        destination_list = self.search_receivment_to_realize()
        for address, recievment_object in destination_list.items():
            destination_matrix = self.GOOGLE_CLIENT.distance_matrix(
                source_address, address
            )['rows'][0]['elements'][0]

            if destination_matrix.get('status') == 'NOT_FOUND':
                continue

            distance = destination_matrix['distance']['value']
            duration = destination_matrix['duration']['value']

            if self.closest_distance is not None:
                if distance < self.latest_distance:
                    self.closest_distance = address
                    self.closest_object = recievment_object
            else:
                self.closest_distance = address
                self.latest_distance = distance
                self.closest_object = recievment_object

        return self.closest_object

    def search_receivment_to_realize(self):
        """
            Function search all possible destination to realize
        :return: dict{'city, street apartment_number':object,}
        """
        ReceivmentLocations = apps.get_model('ReceivmentManage', 'ReceivmentLocations')
        active_locations = ReceivmentLocations.objects.all()
        active_literal_locations = {
            x.concatination_address(): x for x in active_locations
        }
        print(active_literal_locations)
        return active_literal_locations

    def search_active_drivers(self):
        Receivment = apps.get_model('ReceivmentManage', 'Receivment')
        active_locations = Receivment.objects.filter(
            models.Q(status='Finished') & ~models.Q(receivment__type='Proggres')
        ).distinct()
        return active_locations