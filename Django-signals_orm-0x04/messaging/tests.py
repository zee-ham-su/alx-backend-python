from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class MessagingTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

    def test_message_creation_creates_notification(self):
        message = Message.objects.create(sender=self.user1, receiver=self.user2, content='Hello!')
        notification = Notification.objects.get(user=self.user2)

        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)

class MessageEditTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.message = Message.objects.create(sender=self.user1, receiver=self.user2, content='Original Content')

    def test_message_edit_logs_history(self):
        # Edit the message
        self.message.content = 'Edited Content'
        self.message.save()

        # Check MessageHistory
        history = MessageHistory.objects.get(message=self.message)
        self.assertEqual(history.old_content, 'Original Content')
        self.assertTrue(self.message.edited)

    def test_no_history_for_new_message(self):
        new_message = Message.objects.create(sender=self.user1, receiver=self.user2, content='New Message')
        self.assertFalse(MessageHistory.objects.filter(message=new_message).exists())