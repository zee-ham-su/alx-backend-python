from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name',
                  'last_name', 'phone_number', 'role']
        read_only_fields = ['user_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']


class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True)

    class Meta:
        model = Conversation
        fields = ['participants']

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        return conversation

    def validate_participants(self, participants):
        if len(participants) < 2:
            raise serializers.ValidationError(
                "A conversation must have at least two participants.")
        return participants


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['conversation', 'message_body']

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        conversation = data['conversation']
        sender = self.context['request'].user
        if sender not in conversation.participants.all():
            raise serializers.ValidationError(
                "You must be a participant in the conversation to send a message.")
        return data
