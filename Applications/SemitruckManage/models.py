from django.db import models
from .validators import registration_num_validator
from django.core.validators import MinValueValidator, MaxValueValidator


class SemiTrailer(models.Model):
    CHOICES = (
        ('Wolny', 'Wolny'),
        ('Zajety', 'Zajety'),
        ('Awaria', 'Awaria')
    )

    brand = models.CharField(max_length=20, blank=False)
    model = models.CharField(max_length=40, blank=False)
    production_year = models.DateField()
    registration_number = models.CharField(max_length=9,
                                           blank=False,
                                           unique=True)

    semi_note = models.BooleanField(default=True, blank=False)
    photo = models.ImageField(upload_to='media',
                              blank=True,
                              null=True)
    available = models.CharField(choices=CHOICES,
                                 blank=False,
                                 default='Wolny',
                                 max_length=6)

    def __str__(self):
        return self.registration_number

    def update_state(self, key):
        try:
            self.available = dict(self.CHOICES)[key]
            self.save()
        except KeyError:
            raise KeyError("Invalid key of state")

    @property
    def is_available(self):
        return self.available == 'Wolny'

    @is_available.setter
    def is_available(self, value):
        try:
            state = self.CHOICES[value]
            self.available = state
            self.save()
        except KeyError:
            raise KeyError("Invalid key data")

class SemiTrailerEquipment(models.Model):
    semi_trailer = models.OneToOneField(SemiTrailer,
                                        on_delete=models.CASCADE,
                                        blank=False)
    belts = models.IntegerField(default=6,
                                validators=[MinValueValidator(6),
                                            MaxValueValidator(12)])
    corners = models.IntegerField(default=8,
                                  validators=[MinValueValidator(8),
                                              MaxValueValidator(16)])
    aluminium_stick = models.IntegerField(default=12,
                                          validators=[MinValueValidator(12),
                                                      MaxValueValidator(20)])
    wide_stick = models.IntegerField(default=2,
                                     validators=[MinValueValidator(2),
                                                 MaxValueValidator(6)])
    ladder = models.BooleanField(default=True, blank=False)
    roof_stick = models.BooleanField(default=True, blank=False)
    dimenstion_board = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return str(self.semi_trailer.id)