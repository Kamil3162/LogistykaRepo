from rest_framework import serializers
from ..UserManage.serializers import (UserSerializer,
                                      CustomChatUserSerializer)
from .models import Conversations, Participant, Messages

class ParticipantSerializer(serializers.ModelSerializer):
    user = CustomChatUserSerializer(read_only=True)

    class Meta:
        model = Participant
        fields = ['id', 'user', 'data_sended', 'active']

class ConversationSerializer(serializers.ModelSerializer):

    participants = ParticipantSerializer(many=True, read_only=True, source='participant_set')

    class Meta:
        model = Conversations
        fields = ['id', 'participants', 'updated_at']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'




