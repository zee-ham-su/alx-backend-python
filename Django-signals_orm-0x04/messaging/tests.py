from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessagingTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

    def test_message_creation_creates_notification(self):
        message = Message.objects.create(sender=self.user1, receiver=self.user2, content='Hello!')
        notification = Notification.objects.get(user=self.user2)

        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)
