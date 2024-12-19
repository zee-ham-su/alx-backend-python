from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer, ConversationCreateSerializer,
    MessageSerializer, MessageCreateSerializer
)
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipant, IsMessageSender


class ConversationFilter(filters.FilterSet):
    participant = filters.CharFilter(field_name='participants__user_id')
    created_after = filters.DateTimeFilter(
        field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(
        field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Conversation
        fields = ['participant', 'created_after', 'created_before']


class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsParticipant]
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ConversationFilter

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(ConversationSerializer(serializer.instance).data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def add_message(self, request, pk=None):
        conversation = self.get_object()
        serializer = MessageCreateSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        message = serializer.save(
            conversation=conversation, sender=request.user)
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)


class MessageFilter(filters.FilterSet):
    conversation = filters.CharFilter(
        field_name='conversation__conversation_id')
    sender = filters.CharFilter(field_name='sender__user_id')
    sent_after = filters.DateTimeFilter(
        field_name='sent_at', lookup_expr='gte')
    sent_before = filters.DateTimeFilter(
        field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'sent_after', 'sent_before']


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsMessageSender]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MessageFilter

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(MessageSerializer(serializer.instance).data, status=status.HTTP_201_CREATED, headers=headers)
