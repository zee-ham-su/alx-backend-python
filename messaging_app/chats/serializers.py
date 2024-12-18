from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name',
                  'last_name', 'full_name', 'phone_number', 'role']
        read_only_fields = ['user_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    formatted_sent_at = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body',
                  'sent_at', 'formatted_sent_at']
        read_only_fields = ['message_id', 'sent_at']

    def get_formatted_sent_at(self, obj):
        return obj.sent_at.strftime("%Y-%m-%d %H:%M:%S")


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants',
                  'messages', 'created_at', 'last_message']
        read_only_fields = ['conversation_id', 'created_at']

    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-sent_at').first()
        if last_message:
            return MessageSerializer(last_message).data
        return None


class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True)
    initial_message = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Conversation
        fields = ['participants', 'initial_message']

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        initial_message = validated_data.pop('initial_message', None)
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)

        if initial_message:
            Message.objects.create(
                conversation=conversation,
                sender=self.context['request'].user,
                message_body=initial_message
            )

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
