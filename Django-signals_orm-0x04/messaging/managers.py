from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """
        Filters unread messages for the specified user.
        Optimized to fetch only necessary fields.
        """
        return self.filter(receiver=user, read=False).only('id', 'sender', 'content', 'timestamp')