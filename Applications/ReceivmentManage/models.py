from django.db import models
from ..TruckManage.models import Truck
from ..UserManage.models import CustomUser
from ..SemitruckManage.models import SemiTrailer

class Receivment:
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, blank=Truck)
    semi_trailer = models.ForeignKey(SemiTrailer, on_delete=models.CASCADE)
    transferring_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'RecevimentID:{self.id}'

