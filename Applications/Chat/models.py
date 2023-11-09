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
    data_created = models.DateTimeField(auto_now_add=True, null=True)

class Participant(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversations, on_delete=models.CASCADE)
    data_sended = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)


class DeletedMessages(models.Model):
    conversation = models.ForeignKey(Conversations, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message_content = models.CharField(max_length=300)
    data_deleted = models.DateTimeField(auto_now_add=True)

class BlackListedConverstations(models.Model):
    class BlockReasons(models.TextChoices):
        VULGAR_WORD = 'VulgarWords'
        RACISM = 'Racism'
        SEXISM = 'Sexism'
        OTHER = 'Other'

    conversation = models.ForeignKey(
        Conversations,
        on_delete=models.CASCADE,
    )
    blocked_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reason = models.CharField(
        choices=BlockReasons.choices,
        default=BlockReasons.VULGAR_WORD,
        max_length=11
    )
    blocked_at = models.DateTimeField(auto_now_add=True)
    is_permanent = models.BooleanField(default=False)

    @classmethod
    def get_block_reasons(cls):
        return cls.BlockReasons