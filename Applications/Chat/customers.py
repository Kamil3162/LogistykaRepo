import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from django.db.models import Q
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import IntegrityError, OperationalError
from ..UserManage.models import CustomUser
from ..UserManage.serializers import CustomChatUserSerializer
from .models import (
    Participant,
    Conversations,
    Messages,
    BlackListedConverstations
)
from .serializers import (
    ConversationSerializer,
    ParticipantSerializer,
    MessageSerializer
)


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

            print(conversations_pks)

            participants = await self.get_participants(conversations_pks)

            conversations_serialize = await sync_to_async(
                lambda: [ConversationSerializer(conversation).data for
                         conversation in self.conversations]
            )()

            print(len(conversations_serialize))

            # we connect with each channel to be active and get messages from users
            for conversation in self.conversations:
                await self.channel_layer.group_add(
                    str(conversation.pk),  # Ensure PK is a string
                    self.channel_name
                )

            await self.accept()

            users_not_participants = await self.get_all_users()

            users_serializer = await sync_to_async(
                lambda : [CustomChatUserSerializer(user).data for
                user in users_not_participants]
            )()


            # we send data only for us not for all users this is tottally private
            await self.send(text_data=json.dumps({
                # 'type': 'chat_message',
                'message': 'You are now connected!',
                'user': self.user_id + 'naura',
                'conversations': conversations_serialize,
                'users': users_serializer
            }))
            # await self.change_status_to_online()
            await self.change_user_status(True)

        except Exception as e:
            print(f'Error in connect: {str(e)}')

    async def disconnect(self, code):
        """
            Function invoke during exit card chat , for every login we connect
        :param code:
        :return:
        """
        await self.change_user_status(False)
        # await self.change_status_to_offline()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            import datetime

            print("otrzymano wiadomosc")
            print(datetime.datetime.now())
            text_data_json = json.loads(text_data)
            print(text_data_json)

            message_type = text_data_json.get('type')
            message = text_data_json.get('message')
            roomid = text_data_json.get('room_id')
            userid = text_data_json.get('user')

            user_to_start_conversation_id = text_data_json.get(
                'user_to_conversation'
            )

            flaga = text_data_json.get(
                'flaga'
            )

            if message_type == 'get_messages':
                await self.generate_messages(roomid)
            else:
                if user_to_start_conversation_id:
                    conversation = await self.create_conversation_sync()
                    user_to_start_conversation = await self.get_user(
                        user_to_start_conversation_id
                    )

                    participant = await self.create_participant(
                        user=self.user,
                        conversation=conversation
                    )

                    new_user_participant = await self.create_participant(
                        user=user_to_start_conversation,
                        conversation=conversation
                    )

                    print("utworzono nowych frajerow")
                    await self.send_message(message, roomid)

                elif roomid:
                    print('esa testowanie')

                    await self.send_message(message, roomid)

                    await self.saveMessage(userid, roomid, message)

                    await self.send(text_data=json.dumps({
                        'type': 'new_message',
                        'message': message
                    }))
                else:
                    print("testowanie naura")

    async def generate_messages(self, conversation_id):
        """
            During click on our chat we should send a message that we
        :return:
        """
        serializer_data = await self.get_messages_sync(conversation_id)
        await self.send(text_data=json.dumps({
            'type': 'all_messages',
            'room_id': conversation_id,
            'messages': serializer_data
        }))

    @sync_to_async
    def get_messages_sync(self, conversation_id):
        all_messages = Messages.objects.filter(converstation_id=conversation_id)
        serializer = MessageSerializer(instance=all_messages, many=True)
        return serializer.data

    async def chat_message(self, event):
        """
            Function responsible for sending message
        :param event:
        :return:
        """
        room_id = event.get('room_id')
        message = event.get('message')
        user_id = event.get('user_id')

        await self.send(text_data=json.dumps({
            'type': 'group_message',
            'room_id': room_id,
            'message': event['message'],
            'user_id': user_id,
        }))

    async def send_message(self, content, conversation_pk):
        await self.channel_layer.group_send(
            str(conversation_pk),
            {
                'type': 'chat_message',
                'room_id':conversation_pk,
                'user_id': self.user_id,
                'message': content,
            }
        )



    async def change_status_to_offline(self):
        """
            We need to send to entire and each group where we are that we turn off our appliciation
        :return:
        """
        participant = await self.changeParticipantStatus(False)
        for conversation in self.conversations:
            await self.channel_layer.group_send(
                str(conversation.pk),
                {
                    'type': 'chat_message',
                    'message': f'{self.user.first_name} is False',
                    'active': False,
                }
            )
            await self.channel_layer.group_discard(
                str(conversation.pk),
                self.channel_name
            )

    async def change_user_status(self, online:bool):
        """
            Change user status to active during login and clicking
            a chat dashboard.

            :param is_active: A boolean indicating if the user is active.
            :param is_online: A boolean indicating if the user is online.
            :return: None
        :return:
        """
        async def conversation_join(status:bool):
            for conversation in self.conversations:
                await self.channel_layer.group_send(
                    str(conversation.pk),
                    {
                        'type': 'chat_message',
                        'message': f'{self.user.first_name} is {status}',
                        'active': status,
                    }
                )
                if status is False:
                    await self.channel_layer.group_discard(
                        str(conversation.pk),
                        self.channel_name
                    )

        participant = await self.changeParticipantStatus(online)

        if online is False:
            await conversation_join(False)
        else:
            await conversation_join(True)


    async def change_status_to_online(self):
        """
            We need to send to entire and each group where we are that we turn off our appliciation
            :return:
        """
        participant = await self.changeParticipantStatus(True)
        for conversation in self.conversations:
            await self.channel_layer.group_send(
                str(conversation.pk),
                {
                    'type': 'chat_message',
                    'message': f'{self.user.first_name} is Active',
                    'active': True,
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
        print(f'wykonywanie change status {status}')
        try:
            participants = Participant.objects.filter(user=self.user).distinct()
            for participant in participants:
                print(participant)
                participant.active = status
                participant.save()
            return participants
        except Participant.DoesNotExist:
            return False

    @database_sync_to_async
    def saveMessage(self, userid, roomid, content):
        try:
            sender = CustomUser.objects.get(pk=userid)
            conversation = Conversations.objects.get(pk=roomid)
            print(conversation)

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
            conversation=conversation
        )
        return participant

    @database_sync_to_async
    def get_participants(self, conversations_pk):
        """
            Function to return QuerySet with all instance participants using pk
        :param participats:
        :return:
        """
        print("PARTICIPANTS get alll -esa")
        participants = Participant.objects.filter(
            conversation__id__in=conversations_pk,
        ).select_related('user').exclude(user_id=self.user.pk).distinct()


        unique_participants = []
        seen_user_ids = set()

        for participant in participants:
            if participant.user_id not in seen_user_ids:
                unique_participants.append(participant)
                seen_user_ids.add(participant.user_id)


        return unique_participants

    @database_sync_to_async
    def get_all_users(self):
        """
            This function we will use to return all users to potencially start a conversations
            1 FIrst step to make an get to check doest we have a conversation or
            2 Divide this on two types of messages
                Active conversations
                Not active conversations
        :return:
        """
        # return those where users arent in participants ids
        all_participants_ids = Participant.objects.all().distinct().values_list(
            'user_id', flat=True
        )

        participant_not_users = CustomUser.objects.exclude(
            id__in=all_participants_ids
        )

        return participant_not_users



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