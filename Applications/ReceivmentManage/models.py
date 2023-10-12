import datetime

from django.db import models
from ..TruckManage.models import Truck
from ..UserManage.models import CustomUser
from ..SemitruckManage.models import SemiTrailer
from django.utils.translation import gettext_lazy as _
from enum import Enum
class Receivment(models.Model):
    class StatusChoices(models.TextChoices):
        ACCIDENT = 'Accident', _('Accident')
        IN_PROGESS = 'Proggres', _('In progess')
        FINISHED = 'Finish', _('Finished')

        # @classmethod
        # def choices(cls):
        #     return [(item.value, item.value) for item in cls]

    class ReceivmentType(models.TextChoices):
        DRIVER = 'from_driver', _('From Driver to Manager')
        MANAGER = 'from_manager', _('From manager to Driver')

        # @classmethod
        # def choices(cls):
        #     return [(item.value, _(item.value)) for item in cls]

    date_create = models.DateTimeField(default=datetime.datetime.now())
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, blank=True)
    semi_trailer = models.ForeignKey(SemiTrailer, on_delete=models.CASCADE)
    destination_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                         related_name='destination_user', default=1)
    source_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                    related_name='source_user', default=2)
    status = models.CharField(
        choices=StatusChoices.choices,
        default=StatusChoices.IN_PROGESS,
        max_length=10
    )
    date_finished = models.DateTimeField(default=datetime.datetime.now(), blank=True)
    receivment_type = models.CharField(choices=ReceivmentType.choices,
                                       default=ReceivmentType.MANAGER,
                                       max_length=12)
    truck_complain = models.CharField(max_length=300, blank=True)
    semi_trailer_complain = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f'RecevimentID:{self.id}'

class TruckReportPhoto(models.Model):
    receivment = models.ForeignKey(Receivment, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='media/')

    def __str__(self):
        return f"TruckPhoto:{self.receivment.id}"

class SemiTrailerReportPhoto(models.Model):
    receivment = models.ForeignKey(Receivment, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='media/')

    def __str__(self):
        return f"SemiTrailerPhoto:{self.receivment.id}"


