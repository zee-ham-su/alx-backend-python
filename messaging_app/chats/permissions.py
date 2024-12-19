from rest_framework import permissions


class IsParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to view or edit it.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()


class IsMessageSender(permissions.BasePermission):
    """
    Custom permission to only allow the sender of a message to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user
