from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .validators import registration_num_validator
# Create your models here.

class Truck(models.Model):
    CHOICES = (
        ('Wolny', 'Wolny'),
        ('Zajety', 'Zajety'),
        ('Awaria', 'Awaria')
    )
    brand = models.CharField(max_length=20, blank=False)
    model = models.CharField(max_length=40, blank=False)
    power = models.IntegerField(blank=False,
                                validators=[MinValueValidator(300),
                                            MaxValueValidator(999)])
    registration_number = models.CharField(max_length=8,
                                           blank=False,
                                           validators=[
                                               registration_num_validator],
                                           unique=True)
    driven_length = models.IntegerField(blank=False)
    production_date = models.DateField(blank=False)
    avaiable = models.CharField(choices=CHOICES,
                                blank=False,
                                max_length=6,
                                default='Wolny')

    def __str__(self):
        return self.registration_number

    def set_availability(self, state):
        choice_dict = dict(self.CHOICES)
        print(choice_dict)
        try:
            self.avaiable = choice_dict[state]
        except KeyError:
            raise ValueError(f"{state} is not a valid choice for avaiable.")

    def truck_list(self):
        trucks = []


