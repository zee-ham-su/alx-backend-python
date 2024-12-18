from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer, ConversationCreateSerializer,
    MessageSerializer, MessageCreateSerializer
)


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
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ConversationFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def add_message(self, request, pk=None):
        conversation = self.get_object()
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save(conversation=conversation)
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
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MessageFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED, headers=headers)
