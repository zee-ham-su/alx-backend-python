from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')

    objects = models.Manager()
    unread_messages = UnreadMessagesManager()

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"

    def get_threaded_replies(self):
        # Recursive query to fetch all replies for the current message
        replies = self.replies.select_related('sender', 'receiver').prefetch_related('replies')
        threaded_replies = []
        for reply in replies:
            threaded_replies.append({
                'message': reply,
                'replies': reply.get_threaded_replies()  # Recursive call
            })
        return threaded_replies


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='edited_messages')

    def __str__(self):
        return f"Message history for message {self.message.id} edited at {self.edited_at}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user} about message {self.message.id}"
