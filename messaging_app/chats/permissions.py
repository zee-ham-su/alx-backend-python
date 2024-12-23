from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of a message or conversation to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user


class IsParticipant(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()
