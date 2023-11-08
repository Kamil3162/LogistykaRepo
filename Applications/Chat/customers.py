from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from ..UserManage.models import CustomUser
from .models import (
    Participant,
    Conversations,
    Messages
)


class ConversationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['conversation_pk']
        self.group_name = 'chat_%s' % self.room_name
        if self.room_name is None:
            pass

        pass

    async def disconnect(self, code):
        pass

    async def send(self, text_data=None, bytes_data=None, close=False):
        pass

    async def accept(self, subprotocol=None):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        pass
    @database_sync_to_async
    def create_conversation_sync(self):
        self.conversation = Conversations.objects.create()
        return self.conversation

    @database_sync_to_async
    def get_conversation(self, pk):
        try:
            return Conversations.objects.get(pk=pk)
        except Conversations.DoesNotExist:
            raise ValueError("The requested conversation does not exist.")
        except Conversations.MultipleObjectsReturned:
            raise ValueError(
                "Multiple conversations found with the given primary key.")
    @database_sync_to_async
    def create_participant(self, user, conversation):
        participant = Participant.objects.create(
            user=user,
            converstation=conversation
        )
        return participant
    @database_sync_to_async
    def get_participants(self, participats):
        return Participant.objects.filter(pk__in=participats)

    @database_sync_to_async
    def get_participant(self, pk):
        """
            Method check and return participant object if doenst exists we will
            create new object participant
        :param pk:
        :return:
        """
        try:
            return Participant.objects.get(pk=pk)
        except Participant.DoesNotExist:
            return None
        except Participant.MultipleObjectsReturned:
            raise ValueError(
                "Multiple participants found with the given primary key.")
