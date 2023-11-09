import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import IntegrityError, OperationalError
from ..UserManage.models import CustomUser
from .models import (
    Participant,
    Conversations,
    Messages,
    BlackListedConverstations
)

class ConversationConsumer(AsyncWebsocketConsumer):

    # active convarsations
    async def connect(self):
        # room zeby przysylac wiadomosci dla wszystkich i przyslac do wszystkich
        self.user_id = self.scope['url_route']['kwargs']['userId']
        self.user = self.scope['user']
        self.conversations = self.active_conversations(self.user_id)
        self.participans = self.get_all_participants()

        # we add each conversation to the same tunnel
        # all will handle using this one channel
        for conversation in self.conversations:
            self.channel_layer.group_add(
                conversation.pk,
                self.channel_name
            )

        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected!',
            'user': self.user_id
        }))


    async def disconnect(self, code):
        pass

    async def send(self, text_data=None, bytes_data=None, close=False):
        pass

    async def accept(self, subprotocol=None):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        pass

    def notifyOnline(self):
        self.channel_layer.send(

        )

    def saveMessage(self, userid, roomid, content):
        sender = CustomUser.objects.get(pk=userid)
        conversation = Conversations.objects.get(pk=roomid)
        message = Messages.objects.create(
            sender=sender,
            conversation=conversation,
            content=content
        )
        return {
            'action':'message',
            'user_id': sender.pk,
            'conversation_id': conversation.pk,
            'content': message.data_created
        }
    @database_sync_to_async
    def changeUserOfline(self, user):
        participant_user = Participant.objects.get(user=user)
        participant_user.active = False
        participant_user.save()
        return participant_user

    @database_sync_to_async
    def block_user(self):
        """
            Function to block user and entire conversation
            using conversation instance
        :return:
        """
        try:
            user = self.user
            blocked_reasons = BlackListedConverstations.get_block_reasons()
            blacklisted_conversation = BlackListedConverstations.objects.create(
                conversation=self.conversation,
                blocked_by=user,
                reason=blocked_reasons.OTHER,
            )
            return blacklisted_conversation
        except IntegrityError as e:
            return {"error": "Integrity error occurred."}
        except OperationalError as e:
            return {"error": "Operational error with the database."}
        except Exception as e:
            return {"error": "An unexpected error occurred."}

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
    def get_participants(self, conversations_pk):
        """
            Function to return QuerySet with all instance participants using pk
        :param participats:
        :return:
        """
        return Participant.objects.filter(
            conversation__id__in=conversations_pk
        ).select_related('user')


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

    @database_sync_to_async
    def active_conversations(self, user_pk):
        """
            Fetch all conversations with my pk
        :param user_pk:
        :return:
        """
        conversations = Conversations.objects.filter(participants=user_pk)
        print(conversations)
        return conversations

    def get_all_participants(self):
        return Participant.objects.all().distinct()