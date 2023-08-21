from django.db import models
from ..TruckManage.models import Truck
from ..UserManage.models import CustomUser
from ..SemitruckManage.models import SemiTrailer

class Receivment(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, blank=True)
    semi_trailer = models.ForeignKey(SemiTrailer, on_delete=models.CASCADE)
    transferring_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                          related_name='transferring_user')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='sender')
    status = models.BooleanField(default=False)
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
