from django.db import models
from django.core.exceptions import ObjectDoesNotExist
class LocationManager(models.Manager):
    def create_base_location(self, city, street, apartment_number, get_address, final_data):
        # using self.model we create new instance of ReceivmentLocation
        # using self.filter we will search location in all rows in our db

        existing_location = self.get_location_instance(
            city,
            street,
            apartment_number
        )

        if existing_location:
            return existing_location
        else:
            location = self.model(
                city=city,
                street=street,
                apartment_number=apartment_number,
                get_address=get_address,
                final_data=final_data
            )
            location.save(using=self._db)
            return location

    def get_base_location(self):
        try:
            return self.get(city='Jarosław', street='Czarneckiego',
                            apartment_number='16')
        except ObjectDoesNotExist:
            return None  # Return None if no matching record is found

    def get_location_instance(self, city, street, apartment_number):
        existing_location = existing_location = self.filter(
            models.Q(city=city) &
            models.Q(street=street) &
            models.Q(apartment_number=apartment_number)
        ).first()

        if existing_location:
            return existing_location
        else:
            return False
