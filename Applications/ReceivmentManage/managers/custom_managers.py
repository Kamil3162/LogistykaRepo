from django.db import models
from django.apps import apps

class ReceivmentManager(models.Manager):
    '''
        Manager responsible for searching latest finallize address like receivment
        We start from latest finished location and we will calculate distance to make the most effective
    '''
    def get_queryset(self):
        return models.QuerySet(self.model, using=self._db)

    def get_latest_driver_location(self, driver):
        Receivment = apps.get_model('ReceivmentManage', 'Receivment')
        receivment_statuses = Receivment.get_statuses()
        return self.get_queryset().filter(
            models.Q(status=receivment_statuses.FINISHED) &
            models.Q(destination_user=driver)
        ).order_by('data_finished').latest()

