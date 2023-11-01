from django.db import models
from ..UserManage.models import CustomUser
from enum import Enum
class Conversations(models.Model):
    participants = models.ManyToManyField(CustomUser, through='Participant')
    updated_at = models.DateTimeField(auto_now=True)

class Messages(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    converstation = models.ForeignKey(Conversations,
                                      on_delete=models.CASCADE)
    content = models.CharField(max_length=300)

class Participant(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversations, on_delete=models.CASCADE)
    data_sended = models.DateTimeField(auto_now_add=True)

class DeletedMessages(models.Model):
    conversation = models.ForeignKey(Conversations, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message_content = models.CharField(max_length=300)
    data_deleted = models.DateTimeField(auto_now_add=True)

class BlackListedConverstations(models.Model):
    class BlockReasons(Enum):
        VULGAR_WORD = 'VulgarWords'
        RACISM = 'Racism'
        SEXISM = 'Sexism'
        OTHER = 'Other'

    conversation = models.ForeignKey(Conversations, on_delete=models.CASCADE)
    blocked_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reason = models.CharField(choices=BlockReasons, blank=False, default=None)
    blocked_at = models.DateTimeField(auto_now_add=True)
    is_permanent = models.BooleanField(default=False)
