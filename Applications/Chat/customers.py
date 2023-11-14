import json
from asgiref.sync import async_to_sync, sync_to_async
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
from .serializers import ConversationSerializer, ParticipantSerializer

class ConversationConsumer(AsyncWebsocketConsumer):

    # active convarsations
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user_group = None
        self.participants = None
        self.conversations = None
        self.user = None
        self.user_id = None

    async def connect(self):
        try:
            self.user_id = self.scope['url_route']['kwargs']['userId']
            self.user = await self.get_user(
                self.user_id)  # Fetch user asynchronously
            self.conversations = await self.active_conversations(self.user_id)
            self.participants = await self.get_all_participants()  # Corrected spelling
            self.user_group = f'group-{self.user_id}'
            conversations_pks = [con.pk for con in self.conversations]

            participants = self.get_participants(conversations_pks)

            conversations_serialize = await sync_to_async(
                lambda: [ConversationSerializer(conversation).data for
                         conversation in self.conversations]
            )()

            # we connect with each channel to be active and get messages from users
            for conversation in self.conversations:
                await self.channel_layer.group_add(
                    str(conversation.pk),  # Ensure PK is a string
                    self.channel_name
                )

            await self.accept()

            # we send data only for us not for all users this is tottally private
            await self.send(text_data=json.dumps({
                # 'type': 'chat_message',
                'message': 'You are now connected!',
                'user': self.user_id + 'naura',
                'conversations': conversations_serialize
            }))

            await self.change_status_to_online()

        except Exception as e:
            print(f'Error in connect: {str(e)}')

    async def disconnect(self, code):
        """
            Function invoke during exit card chat , for every login we connect
        :param code:
        :return:
        """
        await self.change_status_to_offline()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)

            message = text_data_json.get('message')
            roomid = text_data_json.get('room_id')
            userid = text_data_json.get('user')

            print("Received message:", message)
            print(message, roomid, userid)
            await self.saveMessage(userid, roomid, message)

            await self.send(text_data=json.dumps({
                'type': 'message_received',
                'message': message
            }))

    async def chat_message(self, event):
        """
            Function responsible for sending message
        :param event:
        :return:
        """
        await self.send(text_data=json.dumps({
            'type': 'group_message',
            # 'username': event['username'],
            'message': event['message']
        }))

    # async def websocket_receive(self, message):
    #     print("esssa")
    #     print(message)
    #     pass

    async def send_message(self, content):
        await self.channel_layer.group_send(
            self.user_group,
            {
                "room_id": 'esa',
                "username": self.scope["user"].username,
                "message": 'esa',
            }
        )

    async def change_status_to_offline(self):
        """
            We need to send to entire and each group where we are that we turn off our appliciation
        :return:
        """
        participant = self.changeParticipantStatus(False)
        for conversation in self.conversations:
            await self.channel_layer.group_send(
                str(conversation.pk),
                {
                    'type': 'chat_message',
                    'message': f'{self.user.first_name} is False',
                    'active': False
                }
            )
            await self.channel_layer.group_discard(
                str(conversation.pk),
                self.channel_name
            )

    async def change_status_to_online(self):
        """
            We need to send to entire and each group where we are that we turn off our appliciation
            :return:
        """
        participant = self.changeParticipantStatus(True)
        for conversation in self.conversations:
            await self.channel_layer.group_send(
                str(conversation.pk),
                {
                    'type': 'chat_message',
                    'message': f'{self.user.first_name} is Active',
                    'active': True
                }
            )

    @database_sync_to_async
    def changeParticipantStatus(self, status):
        """
        In status option we have only two posibilities True and False
        True is online, False is offline
        :param status:
        :return:
        """
        try:
            participant = Participant.objects.get(user=self.user)
            participant.active = True
            participant.save()
            return participant
        except Participant.DoesNotExist:
            return False
    @database_sync_to_async
    def saveMessage(self, userid, roomid, content):
        try:
            print("esa esa")
            sender = CustomUser.objects.get(pk=userid)
            conversation = Conversations.objects.get(pk=roomid)
            message = Messages.objects.create(
                sender=sender,
                converstation=conversation,
                content=content
            )
            return {
                'action':'message',
                'user_id': sender.pk,
                'conversation_id': conversation.pk,
                'content': message.data_created
            }

        except Exception as e:
            raise Exception(str(e))

    @database_sync_to_async
    def get_user(self, user_id):
        return CustomUser.objects.get(pk=user_id)

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
        print("participants - exec")
        participants = Participant.objects.filter(
            conversation__id__in=conversations_pk
        ).select_related('user')
        print(participants)
        return list(participants)


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
        return list(conversations)

    @database_sync_to_async
    def get_all_participants(self):
        participants = Participant.objects.all().distinct()
        return list(participants)